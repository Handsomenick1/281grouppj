import boto3
import json

client = boto3.client('dynamodb')

def user_signup_db(event, context):    
    response = client.put_item(
        TableName = 'UserServiceDB',
        Item={
            'userId':{'S': event['userId']},
            'name': {'S': event['name']},
            'agi': {'N': event['agi']},
            'filing_status': {'S': event['filing_status']},
            'filers_blind': {'N': event['filers_blind']},
            'filers_sixtyfive': {'N': event['filers_sixtyfive']},
            'properties': {'S': event['properties']}
        }
    )
    print(response)
    return {
        'statusCode': 200,
        'body': "successfully saved the user to DynamoDB!",
        'headers': {
            "Access-Control-Allow-Origin": "*", "Content-type": "application/json"
        }
    }

# Flow
# After user is registered on Cognito
# Cognito sends a response to the front-end
# front-end sends a request to API GATEWAY
# user_signup_db is invoked by API GATEWAY, save data to DynamoDB
# user_signup_db sends a response back to the front-end
