import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):
    body = json.loads(event['body'])

    order_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    order = {
        'orderId': order_id,
        'description': body['description'],
        'price': str(body['price']),
        'createdAt': now,
        'lastModifiedAt': now,
        'status': 'pending'
    }

    table.put_item(Item=order)

    return {
        'statusCode': 201,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'orderId': order_id, 'message': 'Order created'})
    }
