import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def user_signup_db(event, context):    
    logger.debug('[EVENT] event: {}'.format(event))
    logger.debug('[EVENT] body: {}'.format(event['body']))
    body = event['body']
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
    return {
        'statusCode': 200,
        'body': "successfully saved the user to DynamoDB!",
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
