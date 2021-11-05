import boto3   
import json

def delete_file(event, context):
    s3 = boto3.client('s3')
    filePath = event['queryStringParameters']['filePath']
    response = s3.delete_object(Bucket="itemize-receipts-bucket", Key=filePath)
    return {
        'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                'Access-Control-Allow-Credentials': True
            }
    }

# Delete file flow
# front-end sends a request to API GATEWAY
# delete_file is invoked by API GATEWAY, delete the file from S3
# delete_file sends a response back to the front-end
