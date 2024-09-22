#!/bin/bash

STACK_NAME="iot-sensor-platform"
BUCKET_NAME="${STACK_NAME}-code-$(aws sts get-caller-identity --query Account --output text)"

echo "Deleting CloudFormation stack..."
aws cloudformation delete-stack --stack-name $STACK_NAME

echo "Waiting for stack to be deleted..."
aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME

echo "Deleting S3 bucket..."
aws s3 rm s3://$BUCKET_NAME --recursive
aws s3 rb s3://$BUCKET_NAME

echo "Cleanup complete."