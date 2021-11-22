import json
import boto3
import decimal
from decimal import Decimal
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def update_user(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('itemize-userdb')
    logger.debug('[EVENT] event: {}'.format(event))
    body = None
    try:
        if "body" not in event.keys():
            if "updateUser" not in event.keys():
                raise Exception("updateUser not in event")
            body = event
        else:
            body = event['body']
    except Exception as e:
        logger.debug('[EVENT BODY] reading : {}'.format(event))
        return returnResponse(406, "Event input is not formatted correctly")
    
    logger.debug('[BODY] body: {}'.format(body))
    logger.debug('[BODY] body type: {}'.format(type(body)))
    if type(body) == str:
        body = json.loads(body)
    
    logger.debug('[EVENT] body: {}'.format(str(body)))
    updateUser = body['updateUser']
    
    response = table.update_item(
        Key={
            'userId': updateUser['cognitoUserId'],
            
        },
        UpdateExpression="set first_name=:fi, agi=:ag, last_name=:la, filing_status=:st, filers_blind=:bi, filers_sixtyfive=:si, properties=:pr",
        
        ExpressionAttributeValues={
            ":fi": updateUser['first_name'],
            ":ag": Decimal(str(updateUser['agi'])),
            ":la": updateUser['last_name'],
            ":st": updateUser['filing_status'],
            ":bi": Decimal(str(updateUser['filers_blind'])),
            ":si": Decimal(str(updateUser['filers_sixtyfive'])),
            ":pr": Decimal(str(updateUser['properties']))
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
# update_user is invoked by API GATEWAY, modify data from DynamoDB
# update_user sends a response back to the front-end
