import json
import boto3

translate = boto3.client('translate')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text = body['text']
    target_language = body.get('targetLanguage', 'es')

    result = translate.translate_text(
        Text=text,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language
    )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'translatedText': result['TranslatedText'],
            'sourceLanguage': result['SourceLanguageCode'],
            'targetLanguage': target_language
        })
    }
