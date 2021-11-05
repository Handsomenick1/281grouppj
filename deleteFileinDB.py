import boto3   
import json
from botocore.exceptions import ClientError

def delete_file_DB(event, context):
    # TODO implement
    client = boto3.client('dynamodb')
    filePath = event['filePath']
    if(filePath == None or len(filePath) == 0):
        return {
            'statusCode': 500,
            'body': "Bad request",
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                'Access-Control-Allow-Credentials': True
            }
        }
    try:
        response = client.delete_item(
            TableName = 'itemize-filedb',
            Key={
                'filePath':{'S': filePath},
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {
                'statusCode': 500,
                'body': json.dumps(e.response['Error']['Message']),
                'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    'Access-Control-Allow-Credentials': True
                }
            }
        else:
            raise
    else:
        print(response)
        return {
            'statusCode': 200,
            'body': response,
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                'Access-Control-Allow-Credentials': True
            }
        }
