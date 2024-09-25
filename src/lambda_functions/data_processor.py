import json
import boto3
import os
import logging
from utils import setup_logging, DecimalEncoder
from jsonschema import validate, ValidationError

logger = setup_logging()
dynamodb = boto3.resource('dynamodb')
kinesis = boto3.client('kinesis')
table_name = os.environ.get('DYNAMODB_TABLE')
kinesis_stream_name = os.environ.get('KINESIS_STREAM_NAME')
table = dynamodb.Table(table_name)

# Define JSON schema for input validation
schema = {
    "type": "object",
    "properties": {
        "device_id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "temperature": {"type": ["number", "null"]},
        "humidity": {"type": ["number", "null"]},
        # Add other sensor fields
    },
    "required": ["device_id", "timestamp"],
    "additionalProperties": False
}

def lambda_handler(event, context):
    """
    Process incoming sensor data and store it in DynamoDB.
    """
    try:
        payload = json.loads(event.get('body', '{}'))

        # Validate payload
        validate(instance=payload, schema=schema)

        # Store in DynamoDB
        table.put_item(Item=payload)
        logger.info(f"Data stored in DynamoDB: {payload}")

        # Publish to Kinesis
        kinesis.put_record(
            StreamName=kinesis_stream_name,
            Data=json.dumps(payload),
            PartitionKey=payload['device_id']
        )
        logger.info(f"Data published to Kinesis: {payload}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data stored successfully'})
        }
    except ValidationError as ve:
        logger.error(f"Validation error: {ve.message}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Invalid input: {ve.message}'})
        }
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }