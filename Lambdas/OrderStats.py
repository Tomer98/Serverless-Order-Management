import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):
    result = table.scan()
    orders = result['Items']

    total_orders = len(orders)
    total_revenue = sum(float(o.get('price', 0)) for o in orders)
    by_status = {}
    for o in orders:
        status = o.get('status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'totalOrders': total_orders,
            'totalRevenue': round(total_revenue, 2),
            'byStatus': by_status
        })
    }
