import json
import boto3
import os
import logging
from utils import setup_logging
from botocore.exceptions import ClientError

# Set up logging
logger = setup_logging()

# Initialize AWS clients
sns = boto3.client('sns')
ssm = boto3.client('ssm')

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
STACK_NAME = os.environ.get('STACK_NAME')

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
        # Fetch thresholds from Parameter Store
        temperature_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/temperature_threshold")['Parameter']['Value'])
        humidity_threshold = float(ssm.get_parameter(Name=f"/{STACK_NAME}/humidity_threshold")['Parameter']['Value'])
        # ... fetch other thresholds ...

        for record in event['Records']:
            # Parse the new data from DynamoDB Stream
            if 'NewImage' in record['dynamodb']:
                payload = {
                    key: value.get('S') or float(value.get('N'))
                    for key, value in record['dynamodb']['NewImage'].items()
                }

                alerts = []

                if payload.get('temperature') > temperature_threshold:
                    alerts.append(f"High temperature alert: {payload['temperature']}°C from {payload['device_id']}")

                if payload.get('humidity') > humidity_threshold:
                    alerts.append(f"High humidity alert: {payload['humidity']}% from {payload['device_id']}")

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