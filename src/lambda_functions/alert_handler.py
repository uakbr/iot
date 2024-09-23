import json
import boto3
import os
import logging
from utils import setup_logging, load_config

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
        config = load_config(CONFIG_BUCKET, CONFIG_KEY)
        # Existing thresholds
        temperature_threshold = config.get('temperature_threshold', 30)
        humidity_threshold = config.get('humidity_threshold', 70)
        # New thresholds
        aqi_threshold = config.get('aqi_threshold', 100)
        co2_threshold = config.get('co2_threshold', 1000)
        noise_level_threshold = config.get('noise_level_threshold', 85)
        battery_level_threshold = config.get('battery_level_threshold', 20)
        # ... add more as needed ...

        for record in event['Records']:
            payload = json.loads(record['body'])
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
    except Exception as e:
        logger.error(f"Error in alert handler: {e}")
        raise e