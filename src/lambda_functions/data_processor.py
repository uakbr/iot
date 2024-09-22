import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        # Additional processing can be added here
        table.put_item(Item=payload)
    return {
        'statusCode': 200,
        'body': json.dumps('Data processed successfully')
    }