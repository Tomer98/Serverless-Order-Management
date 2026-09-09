import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):
    result = table.scan()
    orders = result['Items']
    orders.sort(key=lambda x: x.get('createdAt', ''), reverse=True)

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(orders, default=lambda x: float(x) if isinstance(x, Decimal) else str(x))
    }
