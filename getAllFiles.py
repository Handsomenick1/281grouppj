import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import decimal

def get_all_file(event, context):
    dynamodb = boto3.resource('dynamodb')
    if 'userId' not in event['queryStringParameters']:
        return returnResponse(404, "Bad request, please correct the Query Strings to userId")
    
    userId = event['queryStringParameters']['userId']
    table = dynamodb.Table('itemize-filedb')
    response = table.scan(
        FilterExpression=Attr('userId').contains(userId)
    )
    data = response['Items']
    res = []
    for item in data:
        res.append('{' + item['url'] + '}')
    
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
# get_all_file is invoked by API GATEWAY, get files from S3
# get_all_file sends a response back to the front-end
