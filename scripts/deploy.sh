#!/bin/bash

set -e  # Exit on error

STACK_NAME="iot-sensor-platform"
TEMPLATE_FILE="../infrastructure/template.yaml"

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file "$TEMPLATE_FILE" \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ProjectName="$STACK_NAME"

echo "Deployment complete."