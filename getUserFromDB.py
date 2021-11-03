import boto3
import json
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def get_user(event, context):
    try:
        response = client.get_item(
            TableName = 'itemize-userdb',
            Key={
                "userId": {'S' : event['userId']}
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
            'body': json.dumps(response)
        }

# front-end sends a request to API GATEWAY
# get_user is invoked by API GATEWAY, get data from DynamoDB
# get_user sends a response back to the front-end