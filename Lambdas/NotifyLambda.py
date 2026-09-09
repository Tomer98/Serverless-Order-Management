import json
import boto3
import os

sns = boto3.client('sns')
TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    order = event['detail']

    message = f"""An order has been deleted:

Order ID: {order.get('orderId')}
Customer: {order.get('customerName')}
Item: {order.get('item')}
Quantity: {order.get('quantity')}
Status: {order.get('status')}
Created At: {order.get('createdAt')}
"""

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject='Order Deleted Notification',
        Message=message
    )

    return {'statusCode': 200}
