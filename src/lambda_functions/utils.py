# This file contains utility functions used across various Lambda functions, such as logging or data transformations. It promotes code reusability and modularity.

# Utility functions for Lambda functions
import logging
import json
import decimal
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch all supported libraries
patch_all()

def setup_logging():
    """
    Set up the logger with desired settings.
    """
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class DecimalEncoder(json.JSONEncoder):
    """
    Helper class to convert a DynamoDB item to JSON.
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def load_config(bucket_name, key):
    """Load configuration from an S3 bucket"""
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        config_content = response['Body'].read().decode('utf-8')
        return json.loads(config_content)
    except Exception as e:
        logging.error(f"Error loading configuration from S3: {e}")
        raise e