import boto3
import json
import decimal

from botocore.exceptions import ClientError

def get_recepit(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('itemize-receiptdb')
    if 'filePath' not in event['queryStringParameters']:
        return returnResponse(400, "Bad request, please correct the Query Strings to filePath")
        
    if event['queryStringParameters']['filePath'] == None or len(event['queryStringParameters']['filePath']) == 0:
        return returnResponse(400, "invalid input, try again!")
    
    response = table.get_item(
        Key={
            "filePath": event['queryStringParameters']['filePath']
        }
    )
    
    print(response)
    if 'Item' not in response:
        return returnResponse(400, "receipt not exsit")
    return returnResponse(200, json.dumps(response['Item'], indent=4, cls=DecimalEncoder))
    
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