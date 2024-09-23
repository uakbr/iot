This file contains utility functions used across various Lambda functions, such as logging or data transformations. It promotes code reusability and modularity.

# Utility functions for Lambda functions
import logging
import json
import decimal
import boto3
from hardware_interface import I2CInterface  # If needed

def setup_logging(level=logging.INFO):
    """Set up logging configuration"""
    logger = logging.getLogger()
    if not logger.handlers:
        logging.basicConfig(level=level)
    else:
        for handler in logger.handlers:
            handler.setLevel(level)
    return logger

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for decimal.Decimal objects"""
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

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