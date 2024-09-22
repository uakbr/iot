#!/bin/bash

STACK_NAME="iot-sensor-platform"
TEMPLATE_FILE="../infrastructure/template.yaml"
PARAMETERS_FILE="../infrastructure/parameters.json"

# Package Lambda functions
echo "Packaging Lambda functions..."
cd ../src/lambda_functions
zip -r lambda_functions.zip ./*.py
echo "Uploading Lambda package to S3..."
aws s3 mb s3://"${STACK_NAME}-code-$(aws sts get-caller-identity --query Account --output text)"
aws s3 cp lambda_functions.zip s3://"${STACK_NAME}-code-$(aws sts get-caller-identity --query Account --output text)"/
cd ../../scripts

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file $TEMPLATE_FILE \
    --stack-name $STACK_NAME \
    --parameter-overrides file://$PARAMETERS_FILE \
    --capabilities CAPABILITY_NAMED_IAM

echo "Deployment complete."