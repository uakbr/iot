#!/bin/bash

set -e  # Exit on error

STACK_NAME="iot-sensor-platform"
TEMPLATE_FILE="../infrastructure/template.yaml"
PARAMETERS_FILE="../infrastructure/parameters.json"
CODE_S3_BUCKET="${STACK_NAME}-code-$(aws sts get-caller-identity --query Account --output text)"

# Package Lambda functions
echo "Packaging Lambda functions..."
cd ../src/lambda_functions
zip -r lambda_functions.zip ./*.py

# Upload Lambda package to S3
echo "Uploading Lambda package to S3..."
if ! aws s3 ls "s3://${CODE_S3_BUCKET}" > /dev/null 2>&1; then
    echo "Creating S3 bucket: ${CODE_S3_BUCKET}"
    aws s3 mb s3://"${CODE_S3_BUCKET}"
fi
aws s3 cp lambda_functions.zip s3://"${CODE_S3_BUCKET}"/

cd ../../scripts

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --stack-name "${STACK_NAME}" \
    --template-file "${TEMPLATE_FILE}" \
    --parameter-overrides $(cat "${PARAMETERS_FILE}" | jq -r '.[] | "\(.ParameterKey)=\(.ParameterValue)"') \
    --capabilities CAPABILITY_NAMED_IAM

echo "Deployment complete."