import boto3
import json

def file_upload_db(event, context):
    client = boto3.client('dynamodb', region_name="us-west-2")
    response = client.put_item(
        TableName = 'FileServiceDB',
        Item={
            'fileId':{'S': event['fileId']},
            'merchant': {'S': event['merchant']},
            'description': {'S': event['description']},
            'date': {'S': event['date']},
            'amount': {'S': event['amount']},
            'category': {'S': event['category']},
        }
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            "Access-Control-Allow-Origin": "*", "Content-type": "application/json"
        }
    }

# Flow
# front-end sends a request to API GATEWAY
# file_upload_db is invoked by API GATEWAY, save data to DynamoDB
# file_upload_db sends a response back to the front-end