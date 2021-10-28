import boto3
import json

def user_signup_db(event, context):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName = 'UserServiceDB',
        Item={
            'userId':{'S': event['userId']},
            'name': {'S': event['name']},
            'agi': {'S': event['agi']},
            'tax_filing_status': {'BOOL': event['tax_filing_status']},
            'number_of_blind_filers': {'S': event['number_of_blind_filers']},
            'number_of_filers_over_65': {'S': event['number_of_filers_over_65']},
            'properties': {'S': event['properties']}
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
# An user is registered to Cognito
# Cognito sends a response to the front-end
# front-end sends a request to API GATEWAY
# user_signup_db is invoked by API GATEWAY, save data to DynamoDB
# user_signup_db sends a response back to the front-end
