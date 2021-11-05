import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def user_signup_db(event, context):    
    logger.debug('[EVENT] event: {}'.format(event))
    body = None
    try:
        if ("body" not in event.keys()):
            if "newUser" not in event.keys():
                raise Exception("newUser not in event")
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

    newUser = body['newUser']
    logger.debug('[EVENT] body: {}'.format(str(body)))
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName = 'UserServiceDB',
        Item={
            'userId':{'S': newUser['cognitoUserId']},
            'first_name': {'S': newUser['first_name']},
            'last_name': {'S': newUser['last_name']},
            'agi': {'N': newUser['agi']},
            'filing_status': {'S': newUser['filing_status']},
            'filers_blind': {'N': newUser['filers_blind']},
            'filers_sixtyfive': {'N': newUser['filers_sixtyfive']},
            'properties': {'N': newUser['properties']}
        }
    )
    print(response)
    return returnResponse(200, "successfully saved the user to DynamoDB!")
    
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
# After user is registered on Cognito
# Cognito sends a response to the front-end
# front-end sends a request to API GATEWAY
# user_signup_db is invoked by API GATEWAY, save data to DynamoDB
# user_signup_db sends a response back to the front-end
