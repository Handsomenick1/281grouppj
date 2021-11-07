import json
import boto3
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def delete_receipt(event, context):
    # TODO implement
    client = boto3.client('dynamodb')
    if 'filePath' not in event['queryStringParameters']:
        return returnResponse(400, "Bad request, please correct the Query Strings to filePath")
        
    filePath = event['queryStringParameters']['filePath']
    if(filePath == None or len(filePath) == 0):
        return returnResponse(400, "please enter valid filePath")
    try:
        response = client.delete_item(
            TableName = 'itemize-receiptdb',
            Key={
                'filePath':{'S': filePath},
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return returnResponse(400, json.dumps(e.response['Error']['Message']))
        else:
            return returnResponse(400, "error")
            
    else:
        print(response)
        return returnResponse(200, json.dumps(response))
        
def returnResponse(statusCode, message):
    return {
        'statusCode': statusCode,
        'body': message,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            'Access-Control-Allow-Credentials': True
        }
    }

# front-end sends a request to API GATEWAY
# delete_receipt is invoked by API GATEWAY, delete data from DynamoDB
# delete_receipt sends a response back to the front-end
