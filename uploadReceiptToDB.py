import boto3
import json

client = boto3.client('dynamodb')

def reciept_upload_db(event, context):
    response = client.put_item(
        TableName = 'itemize-receiptdb',
        Item={
            'filePath':{'S': event['filePath']},
            'fileId':{'S': event['fileId']},
            'userId':{'S': event['userId']},
            'merchant': {'S': event['merchant']},
            'description': {'S': event['description']},
            'date': {'S': event['date']},
            'taxamount': {'N': event['taxamount']},
            'amount': {'N': event['amount']},
            'category': {'S': event['category']},
            'url':{'S': event['url']}
        }
    )
    print(response)
    return {
        'statusCode': 200,
        'body': "successfully uploaded the reciept to DynamoDB!",
        'headers': {
            "Access-Control-Allow-Origin": "*", "Content-type": "application/json"
        }
    }

# Flow
# front-end sends a request to API GATEWAY
# reciept_upload_db is invoked by API GATEWAY, save data to DynamoDB
# reciept_upload_db sends a response back to the front-end