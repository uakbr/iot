import json
import boto3
import os
import logging
from utils import setup_logging

# Set up logging
logger = setup_logging()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        item = {
            'device_id': payload['device_id'],
            'timestamp': payload['timestamp'],
            'temperature': str(payload['temperature']),
            'humidity': str(payload['humidity']),
        }
        try:
            table.put_item(Item=item)
            logger.info(f"Data stored in DynamoDB: {item}")
        except Exception as e:
            logger.error(f"Error storing data in DynamoDB: {e}")
            raise e