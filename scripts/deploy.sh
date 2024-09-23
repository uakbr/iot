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

echo "Deployment complete."