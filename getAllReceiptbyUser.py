import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import decimal

def get_all_receipts(event, context):
    dynamodb = boto3.resource('dynamodb')
    userId = event['queryStringParameters']['userId']
    table = dynamodb.Table('itemize-receiptdb')
    response = table.scan(
        FilterExpression=Attr('userId').contains(userId)
    )
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response, indent=4, cls=DecimalEncoder),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            'Access-Control-Allow-Credentials': True
        }
    }
    

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)