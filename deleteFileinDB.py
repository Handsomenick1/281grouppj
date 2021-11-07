import boto3   
import json
from botocore.exceptions import ClientError

def delete_file_DB(event, context):
    # TODO implement
    client = boto3.client('dynamodb')
    filePath = event['filePath']
    if "filePath" not in event:
        return returnResponse(500, "bad request")
    try:
        response = client.delete_item(
            TableName = 'itemize-filedb',
            Key={
                'filePath':{'S': filePath},
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return returnResponse(500, json.dumps(e.response['Error']['Message']))
        else:
            raise
    else:
        print(response)
        return returnResponse(200, response)

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