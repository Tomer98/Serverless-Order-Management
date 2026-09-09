import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')
events = boto3.client('events')

def lambda_handler(event, context):
    order_id = event['pathParameters']['orderId']

    result = table.get_item(Key={'orderId': order_id})
    if 'Item' not in result:
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Order not found'})
        }

    order = result['Item']
    table.delete_item(Key={'orderId': order_id})

    events.put_events(Entries=[{
        'Source': 'myapp.orders',
        'DetailType': 'OrderDeleted',
        'Detail': json.dumps(order, default=lambda x: float(x) if isinstance(x, Decimal) else str(x)),
        'EventBusName': 'default'
    }])

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'Order deleted', 'orderId': order_id})
    }
