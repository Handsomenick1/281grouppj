import boto3
import json
from botocore.exceptions import ClientError

def get_file(event, context):
    client = boto3.client('dynamodb')
    try:
        response = client.get_item(
            TableName = 'FileServiceDB',
            Key={
                "fileId": {'S' : event['fileId']}
            }
        )
    except ClientError as e:
        return{
            'statusCode': 400,
            'body': json.dumps(e.response['Error']['Message']),
            'headers': {
                "Access-Control-Allow-Origin": "*", 
                "Content-type": "application/json"
            }
        }
    else:
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