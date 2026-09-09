import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text = body['text']

    result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = result['Sentiment']
    scores = result['SentimentScore']

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'sentiment': sentiment,
            'scores': {
                'positive': round(scores['Positive'], 3),
                'negative': round(scores['Negative'], 3),
                'neutral': round(scores['Neutral'], 3),
                'mixed': round(scores['Mixed'], 3)
            }
        })
    }
