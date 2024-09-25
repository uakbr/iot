import json
import boto3
import os
import logging
from utils import setup_logging, DecimalEncoder
from jsonschema import validate, ValidationError  # New import

# Set up logging
logger = setup_logging()

# Initialize DynamoDB table
table_name = os.environ.get('DYNAMODB_TABLE')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

# Define the expected schema
sensor_data_schema = {
    "type": "object",
    "properties": {
        "device_id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "temperature": {"type": "number"},
        "humidity": {"type": "number"},
        # ... add other fields ...
    },
    "required": ["device_id", "timestamp"],
}

def lambda_handler(event, context):
    """
    Lambda function to process incoming sensor data and store it in DynamoDB.

    Parameters:
        event (dict): AWS event data containing sensor records.
        context: Runtime information of the Lambda function.

    Returns:
        dict: Response with status code and message.
    """
    try:
        payload = json.loads(event['body'])

        # Validate payload against the schema
        validate(instance=payload, schema=sensor_data_schema)

        # Convert and sanitize data
        item = {
            'device_id': payload['device_id'],
            'timestamp': payload['timestamp'],
            'temperature': float(payload.get('temperature', 0)),
            'humidity': float(payload.get('humidity', 0)),
            # ... process other fields ...
        }

        # Store item in DynamoDB
        table.put_item(Item=item)
        logger.info(f"Data stored in DynamoDB: {item}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data stored successfully'}, cls=DecimalEncoder)
        }
    except ValidationError as ve:
        logger.error(f"Payload validation error: {ve.message}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Invalid payload: {ve.message}'})
        }
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }