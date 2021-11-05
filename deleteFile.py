import boto3   
import json

def delete_file(event, context):
    s3 = boto3.client('s3')
    lam = boto3.client('lambda')
    filePath = event['queryStringParameters']['filePath']
    if(filePath == None or len(filePath) == 0):
        return {
            'statusCode': 500,
            'body': "please enter valid filePath",
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                'Access-Control-Allow-Credentials': True
            }
        }
    s3.delete_object(Bucket="itemize-receipts-bucket", Key=filePath)
    response = lam.invoke(FunctionName='itemize-deletefileinDB',
                InvocationType='Event',
                Payload=json.dumps({'filePath': filePath})
                )
    if response not in range(200,299):
        return {
                'statusCode':200,
                'body': "Successfully deleted file in s3 and DynamoDB",
                'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    'Access-Control-Allow-Credentials': True
                }
        }
    else:
        return {
                'statusCode':500,
                'body': "bad operation",
                'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    'Access-Control-Allow-Credentials': True
                }
        }

# front-end sends a request to API GATEWAY
# delete_file is invoked by API GATEWAY, delete the file in S3
# delete_file_DB is invoked by delete_file, delete the file in DynamoDB
# delete_file sends a response back to the front-end
