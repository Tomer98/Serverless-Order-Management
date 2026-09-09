import json
import boto3
import os

sns = boto3.client('sns')
TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']

    subs = sns.list_subscriptions_by_topic(TopicArn=TOPIC_ARN)
    sub_arn = None
    for sub in subs['Subscriptions']:
        if sub['Endpoint'] == email:
            sub_arn = sub['SubscriptionArn']
            break

    if not sub_arn or sub_arn == 'PendingConfirmation':
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Subscription not found or pending confirmation'})
        }

    sns.unsubscribe(SubscriptionArn=sub_arn)

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': f'{email} unsubscribed successfully'})
    }
