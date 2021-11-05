import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def get_all_files(event, context):
    dynamodb = boto3.resource('dynamodb')
    userId = event['queryStringParameters']['userId']
    table = dynamodb.Table('itemize-filedb')
    response = table.scan(
        FilterExpression=Attr('userId').contains(userId)
    )
    data = response['Items']
    res = []
    for item in data:
        res.append('{' + item['url'] + '}')
    
    return {
        'statusCode': 200,
        'body': json.dumps(res, indent=4),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            'Access-Control-Allow-Credentials': True
        }
    }
    
