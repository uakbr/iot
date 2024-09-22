import json
import boto3
import os

sns = boto3.client('sns')
sns_topic_arn = os.environ['SNS_TOPIC_ARN']
config_bucket = os.environ['CONFIG_BUCKET']
config_key = os.environ['CONFIG_KEY']

def get_config():
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=config_bucket, Key=config_key)
    config_content = response['Body'].read().decode('utf-8')
    return json.loads(config_content)

def lambda_handler(event, context):
    config = get_config()
    temperature_threshold = config['temperature_threshold']
    humidity_threshold = config['humidity_threshold']

    for record in event['Records']:
        payload = json.loads(record['body'])
        alerts = []

        if payload['temperature'] > temperature_threshold:
            alerts.append(f"High temperature alert: {payload['temperature']}°C from {payload['device_id']}")
        if payload['humidity'] > humidity_threshold:
            alerts.append(f"High humidity alert: {payload['humidity']}% from {payload['device_id']}")

        for alert in alerts:
            sns.publish(
                TopicArn=sns_topic_arn,
                Message=alert,
                Subject='IoT Sensor Alert'
            )
    return {
        'statusCode': 200,
        'body': json.dumps('Alerts processed successfully')
    }