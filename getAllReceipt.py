import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import decimal

def get_all_receipt(event, context):
    dynamodb = boto3.resource('dynamodb')
    if 'userId' not in event['queryStringParameters']:
        return returnResponse(205, "Bad request, please correct the Query Strings to userId")

    userId = event['queryStringParameters']['userId']
    table = dynamodb.Table('itemize-receiptdb')
    response = table.scan(
        FilterExpression=Attr('userId').contains(userId)
    )
    print(response)
    if response['Items'] == None or len(response['Items']) == 0:
        return returnResponse(204, "No receipt!")
    return returnResponse(200, json.dumps(response['Items'], indent=4, cls=DecimalEncoder))
    
    

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