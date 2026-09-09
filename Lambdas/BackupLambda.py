import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['S3_BUCKET_NAME']

def lambda_handler(event, context):
    order = event['detail']
    order_id = order.get('orderId')

    content = f"""Order Backup
============
Order ID:    {order.get('orderId')}
Description: {order.get('description')}
Price:       ${order.get('price')}
Status:      {order.get('status')}
Created At:  {order.get('createdAt')}
Deleted At:  {datetime.utcnow().isoformat()}
"""

    key = f"deleted-orders/{order_id}.txt"
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=content)

    return {'statusCode': 200}
