import boto3
import json

client = boto3.client('dynamodb')

def file_upload_db(event, context):
	bucket = event['Records'][0]['s3']['bucket']['name']
	date = event['Records'][0]['eventTime']
	filepath = event['Records'][0]['s3']['object']['key']
	region = 'us-west-2'
	url = 'https://'+bucket+'.s3'+region+'amazonaws.com/'+filepath
	response = client.put_item(
        TableName = 'itemize-filedb',
        Item={
            'filePath':{'S': filepath},
            'url':{'S': url},
            'date': {'S': date},
            'bucket':{'S': bucket}
        }
    )
	print(response)
	return {
        'statusCode': 200,
        'body': "successfully uploaded the file to DynamoDB!"
    }

# Flow
# file_upload_db is invoked by S3 as long as an object created in S3
# file_upload_db sends a response to the front-end