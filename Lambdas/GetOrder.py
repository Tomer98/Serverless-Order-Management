import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):
    order_id = event['pathParameters']['orderId']
    result = table.get_item(Key={'orderId': order_id})

    if 'Item' not in result:
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Order not found'})
        }

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(result['Item'], default=lambda x: float(x) if isinstance(x, Decimal) else str(x))
    }
