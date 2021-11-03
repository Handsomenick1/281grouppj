import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def reciept_upload_db(event, context):
    logger.debug('[EVENT] event: {}'.format(event))
    logger.debug('[EVENT] body: {}'.format(event['body']))
    body = event['body']
    newReciept = body['newReceipt']
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName = 'itemize-receiptdb',
        Item={
            'filePath':{'S': newReciept['filePath']},
            'userId':{'S': newReciept['userId']},
            'merchant': {'S': newReciept['merchant']},
            'description': {'S': newReciept['description']},
            'date': {'S': newReciept['date']},
            'taxamount': {'N': newReciept['taxamount']},
            'amount': {'N': newReciept['amount']},
            'category': {'S': newReciept['category']},
        }
    )
    print(response)
    return {
        'statusCode': 200,
        'body': "successfully uploaded the reciept to DynamoDB!"
    }

# Flow
# front-end sends a request to API GATEWAY
# reciept_upload_db is invoked by API GATEWAY, save data to DynamoDB
# reciept_upload_db sends a response back to the front-end