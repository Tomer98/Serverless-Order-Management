import json
import boto3
import os

sns = boto3.client('sns')
TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']

    sns.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol='email',
        Endpoint=email
    )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': f'Confirmation email sent to {email}'})
    }
