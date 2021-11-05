import boto3
import json
import decimal
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def get_file(event, context):
    try:
        response = client.get_item(
            TableName = 'itemize-filedb',
            Key={
                "filePath": {'S' : event['queryStringParameters']['filePath']}
            }
        )
    except ClientError as e:
        return{
            'statusCode': 400,
            'body': json.dumps(e.response['Error']['Message']),
            'headers': {
                "Access-Control-Allow-Origin": "*", 
                "Content-type": "application/json"
            }
        }
    else:
        return {
            'statusCode': 200,
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

# front-end sends a request to API GATEWAY
# get_file is invoked by API GATEWAY, get data from DynamoDB
# get_file sends a response back to the front-end