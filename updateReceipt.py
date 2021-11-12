import json
import boto3
import decimal
from decimal import Decimal
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def update_receipt(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('itemize-receiptdb')
    logger.debug('[EVENT] event: {}'.format(event))
    body = None
    try:
        if "body" not in event.keys():
            body = event
        elif "updateReceipt" not in event['body']:
            raise Exception("updateReceipt not in event")
        else:
            body = event['body']
    except Exception as e:
        logger.debug('[EVENT BODY] reading : {}'.format(event))
        return returnResponse(406, "Event input is not formatted correctly")
    
    logger.debug('[BODY] body: {}'.format(body))
    logger.debug('[BODY] body type: {}'.format(type(body)))
    if type(body) == str:
        body = json.loads(body)
    updateReceipt = body['updateReceipt']
    response = table.update_item(
        Key={
            'filePath': updateReceipt['filePath']
            
        },
        UpdateExpression="set merchant=:me, #date=:da, taxamount=:ta, amount=:am, category=:ca, description=:de",
        ExpressionAttributeNames={
            "#date": "date",
            
        },
        ExpressionAttributeValues={
            ":me": updateReceipt['merchant'],
            ":da": updateReceipt['date'],
            ":ta": Decimal(str(updateReceipt['taxamount'])),
            ":am": Decimal(str(updateReceipt['amount'])),
            ":ca": updateReceipt['category'],
            ":de": updateReceipt['description'],
            
        })
    return returnResponse(200, json.dumps(response, indent=4, cls=DecimalEncoder))
    
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

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
# reciept_update is invoked by API GATEWAY, save data to DynamoDB
# reciept_update sends a response back to the front-end
