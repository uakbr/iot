import json
import boto3
import os
import logging
from utils import setup_logging, DecimalEncoder  # Import DecimalEncoder

# Set up logging
logger = setup_logging()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    """
    Lambda function to process incoming sensor data and store it in DynamoDB.
    
    Parameters:
        event (dict): AWS event data containing sensor records.
        context: Runtime information of the Lambda function.
    
    Returns:
        None
    """
    try:
        payload = json.loads(event['body'])
        item = {
            'device_id': payload['device_id'],
            'timestamp': payload['timestamp'],
            'temperature': float(payload['temperature']),
            'humidity': float(payload['humidity']),
            'air_quality_index': float(payload.get('air_quality_index', 0)),
            'light_intensity': float(payload.get('light_intensity', 0)),
            'sound_level': float(payload.get('sound_level', 0)),
            'pressure': float(payload.get('pressure', 0)),
            'co2_level': float(payload.get('co2_level', 0)),
            'uv_index': float(payload.get('uv_index', 0)),
            'wind_speed': float(payload.get('wind_speed', 0)),
            'wind_direction': payload.get('wind_direction', 'Unknown'),
            'battery_level': float(payload.get('battery_level', 100)),
            'signal_strength': float(payload.get('signal_strength', -100)),
            'latitude': float(payload.get('latitude', 0.0)),
            'longitude': float(payload.get('longitude', 0.0)),
            'orientation': payload.get('orientation', 'Unknown'),
            'motion_detected': payload.get('motion_detected', False),
            # ... existing fields ...
        }
        table.put_item(Item=item)
        logger.info(f"Data stored in DynamoDB: {item}")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data stored successfully'}, cls=DecimalEncoder)
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }