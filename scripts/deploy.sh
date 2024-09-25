#!/bin/bash

set -e  # Exit on error

STACK_NAME="iot-sensor-platform"
TEMPLATE_FILE="../infrastructure/template.yaml"
PARAMETERS_FILE="../infrastructure/parameters.json"
CODE_S3_BUCKET="${STACK_NAME}-code-$(aws sts get-caller-identity --query Account --output text)"

# Package Lambda functions
echo "Packaging Lambda functions..."
cd ../src/lambda_functions
rm -f lambda_functions.zip
zip -r lambda_functions.zip ./*.py

# Upload Lambda package to S3
echo "Uploading Lambda package to S3..."
if ! aws s3 ls "s3://${CODE_S3_BUCKET}" > /dev/null 2>&1; then
    echo "Creating S3 bucket: ${CODE_S3_BUCKET}"
    aws s3 mb s3://"${CODE_S3_BUCKET}"
fi
aws s3 cp lambda_functions.zip s3://"${CODE_S3_BUCKET}"/

cd ../../scripts

# Check for jq
if ! command -v jq &> /dev/null; then
    echo "jq is required but not installed. Please install jq and try again."
    exit 1
fi

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
PARAMETERS=$(jq -r '.[] | "--parameter-overrides \(.ParameterKey)=\(.ParameterValue)"' "${PARAMETERS_FILE}" | xargs)
aws cloudformation deploy \
    --stack-name "${STACK_NAME}" \
    --template-file "${TEMPLATE_FILE}" \
    $PARAMETERS \
    --capabilities CAPABILITY_NAMED_IAM

# Fetch AWS Region
AWS_REGION=$(aws configure get region)

echo "Fetching API Key..."
API_KEY_ID=$(aws apigateway get-api-keys --name-query "${STACK_NAME}-ApiKey" --include-values --region "${AWS_REGION}" --query 'items[0].id' --output text)
API_KEY_VALUE=$(aws apigateway get-api-key --api-key "${API_KEY_ID}" --include-value --region "${AWS_REGION}" --query 'value' --output text)

echo "API Key: ${API_KEY_VALUE}"

echo "Storing configuration parameters in Parameter Store..."
aws ssm put-parameter --name "/${STACK_NAME}/temperature_threshold" --type "String" --value "30" --overwrite
aws ssm put-parameter --name "/${STACK_NAME}/humidity_threshold" --type "String" --value "70" --overwrite
# ... add more parameters as needed ...

echo "Retrieving IoT Core endpoint..."
IOT_ENDPOINT=$(aws iot describe-endpoint --endpoint-type iot:Data-ATS --query 'endpointAddress' --output text)
echo "IoT Endpoint: ${IOT_ENDPOINT}"

echo "Retrieving IoT Certificate and Keys..."
CERTIFICATES_DIR="../certs"
mkdir -p "${CERTIFICATES_DIR}"

aws iot describe-certificate --certificate-id "$(basename $(aws cloudformation describe-stack-resource --stack-name "${STACK_NAME}" --logical-resource-id IoTCertificate --query 'StackResourceDetail.PhysicalResourceId' --output text))" --query 'certificateDescription.certificatePem' --output text > "${CERTIFICATES_DIR}/device.pem.crt"

aws iot create-keys-and-certificate --set-as-active \
    --public-key-outfile "${CERTIFICATES_DIR}/public.pem.key" \
    --private-key-outfile "${CERTIFICATES_DIR}/private.pem.key" \
    --certificate-pem-outfile "${CERTIFICATES_DIR}/device.pem.crt" > /dev/null

# Download Root CA
curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > "${CERTIFICATES_DIR}/AmazonRootCA1.pem"

echo "Certificates and keys stored in ${CERTIFICATES_DIR}"

echo "Uploading analytics SQL script to S3..."
aws s3 cp ../analytics/real_time_metrics.sql s3://"${CODE_S3_BUCKET}"/

echo "Starting Kinesis Analytics application..."
aws kinesisanalytics update-application \
    --application-name "${STACK_NAME}-AnalyticsApp" \
    --application-update \
        '{
            "ApplicationCodeUpdate": "'"$(cat ../analytics/real_time_metrics.sql)"'"
        }'

echo "Deployment complete."