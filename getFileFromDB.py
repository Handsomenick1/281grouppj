import boto3
import json

def get_file(event, context):
    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName = 'FileServiceDB',
        Key={
            "fileId": {'S' : event['fileId']}
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            "Access-Control-Allow-Origin": "*", 
            "Content-type": "application/json"
        }
    }
    
# front-end sends a request to API GATEWAY
# get_file is invoked by API GATEWAY, get data from DynamoDB
# get_file sends a response back to the front-end