import json
import boto3
import os
import logging
from utils import setup_logging, load_config
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Set up logging
logger = setup_logging()

sns = boto3.client('sns')

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
CONFIG_BUCKET = os.environ.get('CONFIG_BUCKET')
CONFIG_KEY = os.environ.get('CONFIG_KEY')

def lambda_handler(event, context):
    """
    Lambda function to handle sensor data alerts based on configurable thresholds.
    
    Parameters:
        event (dict): AWS event data containing sensor records.
        context: Runtime information of the Lambda function.
    
    Returns:
        None
    """
    try:
        ssm = boto3.client('ssm')

        # Fetch thresholds from Parameter Store
        temperature_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/temperature_threshold")['Parameter']['Value'])
        humidity_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/humidity_threshold")['Parameter']['Value'])
        aqi_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/aqi_threshold")['Parameter']['Value'])
        co2_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/co2_threshold")['Parameter']['Value'])
        noise_level_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/noise_level_threshold")['Parameter']['Value'])
        battery_level_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/battery_level_threshold")['Parameter']['Value'])

        for record in event['Records']:
            if 'dynamodb' in record:
                new_image = record['dynamodb'].get('NewImage', {})
                # Convert DynamoDB data types to standard types
                payload = {k: list(v.values())[0] for k, v in new_image.items()}
            else:
                continue  # Skip records without DynamoDB data

            alerts = []

            # Existing checks
            if payload.get('temperature') > temperature_threshold:
                alerts.append(f"High temperature alert: {payload['temperature']}°C from {payload['device_id']}")

            if payload.get('humidity') > humidity_threshold:
                alerts.append(f"High humidity alert: {payload['humidity']}% from {payload['device_id']}")

            # New checks
            if payload.get('air_quality_index') > aqi_threshold:
                alerts.append(f"Poor air quality alert: AQI {payload['air_quality_index']} from {payload['device_id']}")

            if payload.get('co2_level') > co2_threshold:
                alerts.append(f"High CO₂ level alert: {payload['co2_level']} ppm from {payload['device_id']}")

            if payload.get('sound_level') > noise_level_threshold:
                alerts.append(f"High noise level alert: {payload['sound_level']} dB from {payload['device_id']}")

            if payload.get('battery_level') < battery_level_threshold:
                alerts.append(f"Low battery alert: {payload['battery_level']}% on {payload['device_id']}")

            # ... additional checks ...

            for alert in alerts:
                response = sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=alert,
                    Subject='Sensor Alert'
                )
                logger.info(f"Alert sent: {alert}, SNS Message ID: {response['MessageId']}")
    except ClientError as e:
        logger.error(f"Error fetching configuration from Parameter Store: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error in alert handler: {e}")
        raise e