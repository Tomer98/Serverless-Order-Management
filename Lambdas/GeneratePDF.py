import json
import boto3
import os
from fpdf import FPDF
from datetime import datetime
import tempfile

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['S3_BUCKET_NAME']

def lambda_handler(event, context):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='deleted-orders/')

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'No deleted orders found'})
        }

    orders = []
    for obj in response['Contents']:
        file = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
        orders.append(file['Body'].read().decode('utf-8'))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'Deleted Orders Summary', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Generated: {datetime.utcnow().isoformat()}', ln=True)
    pdf.ln(5)

    for order_text in orders:
        for line in order_text.strip().split('\n'):
            pdf.cell(0, 6, line, ln=True)
        pdf.ln(4)

    tmp_path = tempfile.mktemp(suffix='.pdf')
    pdf.output(tmp_path)

    pdf_key = f'summaries/orders-summary-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.pdf'
    s3.upload_file(tmp_path, BUCKET_NAME, pdf_key)

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': pdf_key},
        ExpiresIn=3600
    )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'url': url})
    }
