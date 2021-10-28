import boto3
import json

def get_user(event, context):
    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName = 'UserServiceDB',
        Key={
            "userId": {'S' : event['userId']}
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            "Access-Control-Allow-Origin": "*", 
            "Content-type": "application/json"
        },
    }

# front-end sends a request to API GATEWAY
# get_user is invoked by API GATEWAY, get data from DynamoDB
# get_user sends a response back to the front-end