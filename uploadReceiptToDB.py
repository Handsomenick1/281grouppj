import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def receipt_upload(event, context):
    logger.debug('[EVENT] event: {}'.format(event))
    body = None
    try:
        if "body" not in event.keys():
            raise 
        elif "newReceipt" not in event['body']:
            return returnResponse(400, "newReceipt not in the request")
        else:
            body = event['body']
    except Exception as e:
        logger.debug('[EVENT BODY] reading : {}'.format(event))
        return returnResponse(406, "Event input is not formatted correctly")
    
    logger.debug('[BODY] body: {}'.format(body))
    logger.debug('[BODY] body type: {}'.format(type(body)))
    if type(body) == str:
        body = json.loads(body)
        
    newReceipt = body['newReceipt']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('itemize-receiptdb')
    response = table.put_item(
       Item={
            'filePath': newReceipt['filePath'],
            'userId': newReceipt['userId'],
            'merchant': newReceipt['merchant'],
            'description': newReceipt['description'],
            'date': newReceipt['date'],
            'taxamount': newReceipt['taxamount'],
            'amount': newReceipt['amount'],
            'category': newReceipt['category']
            
        }
    )
    print(response)
    return returnResponse(200, "successfully saved the receipt to DynamoDB!")

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

# Flow
# front-end sends a request to API GATEWAY
# reciept_upload_db is invoked by API GATEWAY, save data to DynamoDB
# reciept_upload_db sends a response back to the front-end