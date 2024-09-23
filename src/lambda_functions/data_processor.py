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
            # Add new data fields
            'air_quality_index': str(payload.get('air_quality_index')),
            'light_intensity': str(payload.get('light_intensity')),
            'sound_level': str(payload.get('sound_level')),
            'pressure': str(payload.get('pressure')),
            'co2_level': str(payload.get('co2_level')),
            'uv_index': str(payload.get('uv_index')),
            'wind_speed': str(payload.get('wind_speed')),
            'wind_direction': payload.get('wind_direction'),
            'battery_level': str(payload.get('battery_level')),
            'signal_strength': str(payload.get('signal_strength')),
            'latitude': str(payload.get('latitude')),
            'longitude': str(payload.get('longitude')),
            'orientation': payload.get('orientation'),
            'motion_detected': str(payload.get('motion_detected')),
            # ... existing code ...
        }
        try:
            table.put_item(Item=item)
            logger.info(f"Data stored in DynamoDB: {item}")
        except Exception as e:
            logger.error(f"Error storing data in DynamoDB: {e}")
            raise e