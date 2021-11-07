import boto3   
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

def delete_all_receipt(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    if 'userId' not in event['queryStringParameters']:
        return returnResponse(400, "Bad request, please correct the Query Strings to userId")
    userId = event['queryStringParameters']['userId']
    table = dynamodb.Table('itemize-receiptdb')
    if(userId == None or len(userId) == 0):
        return returnResponse(400, "invalid userId, try again")
        
    response = table.scan(
        FilterExpression=Attr('userId').contains(userId)
    )
    
    print(response)
    scan = table.scan()
    with table.batch_writer() as batch:
        for filepaths in response['Items']:
            batch.delete_item(
                Key={
                    'filePath': filepaths['filePath'],
                }
            )

    print(response)
    return returnResponse(200, "successfully deleted all reciepts in DynamoDB!")
    
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
# delete_all_receipt is invoked by API GATEWAY, delete data from DynamoDB
# delete_all_receipt sends a response back to the front-end
