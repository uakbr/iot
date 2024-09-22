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
    try:
        config = load_config(CONFIG_BUCKET, CONFIG_KEY)
        temperature_threshold = config.get('temperature_threshold', 30)
        humidity_threshold = config.get('humidity_threshold', 70)

        for record in event['Records']:
            payload = json.loads(record['body'])
            alerts = []

            if payload.get('temperature') > temperature_threshold:
                alerts.append(f"High temperature alert: {payload['temperature']}°C from {payload['device_id']}")

            if payload.get('humidity') > humidity_threshold:
                alerts.append(f"High humidity alert: {payload['humidity']}% from {payload['device_id']}")

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