import json
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):
    order_id = event['pathParameters']['orderId']
    body = json.loads(event['body'])

    result = table.update_item(
        Key={'orderId': order_id},
        UpdateExpression='SET #s = :s, lastModifiedAt = :lm',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={
            ':s': body['status'],
            ':lm': datetime.utcnow().isoformat()
        },
        ReturnValues='ALL_NEW'
    )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(result['Attributes'], default=lambda x: float(x) if isinstance(x, Decimal) else str(x))
    }
