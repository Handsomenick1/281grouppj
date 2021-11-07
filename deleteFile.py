import boto3
import json

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    lam = boto3.client('lambda')
    if "filePath" not in event['queryStringParameters']:
        return returnResponse(500, "please enter valid filePath")
    filePath = event['queryStringParameters']['filePath']
    s3.delete_object(Bucket="itemize-receipts-bucket", Key=filePath)
    response = lam.invoke(FunctionName='itemize-deletefileinDB',
                InvocationType='Event',
                Payload=json.dumps({'filePath': filePath})
                )
    print(response['ResponseMetadata']['HTTPStatusCode'])
    if response['ResponseMetadata']['HTTPStatusCode'] in range(200,299):
        return returnResponse(200, "Successfully deleted file in s3 and DynamoDB")
        
    else:
        return returnResponse(400, "error")
        
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
# delete_file is invoked by API GATEWAY, delete the file in S3
# delete_file_DB is invoked by delete_file, delete the file in DynamoDB
# delete_file sends a response back to the front-end
