#!/bin/bash

set -e  # Exit on error

STACK_NAME="iot-sensor-platform"
CODE_S3_BUCKET="${STACK_NAME}-code-$(aws sts get-caller-identity --query Account --output text)"
CONFIG_S3_BUCKET="${STACK_NAME}-config-$(aws sts get-caller-identity --query Account --output text)"

read -p "Are you sure you want to delete the CloudFormation stack '$STACK_NAME' and all associated resources? (yes/no) " confirm
if [[ $confirm != "yes" ]]; then
    echo "Cleanup aborted."
    exit 0
fi

echo "Deleting CloudFormation stack..."
aws cloudformation delete-stack --stack-name "${STACK_NAME}"
aws cloudformation wait stack-delete-complete --stack-name "${STACK_NAME}"
echo "CloudFormation stack deleted."

echo "Deleting S3 buckets..."
aws s3 rm s3://"${CODE_S3_BUCKET}" --recursive || true
aws s3 rb s3://"${CODE_S3_BUCKET}" --force || true

aws s3 rm s3://"${CONFIG_S3_BUCKET}" --recursive || true
aws s3 rb s3://"${CONFIG_S3_BUCKET}" --force || true

echo "Cleanup complete."