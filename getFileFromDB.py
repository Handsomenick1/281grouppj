import json
import boto3
import decimal
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')
def get_file(event, context):
    # TODO implement
    if 'filePath' not in event['queryStringParameters']:
        return returnResponse(404, "Bad request, please correct the Query Strings to filePath")
    try:
        response = client.get_item(
            TableName = 'itemize-filedb',
            Key={
                "filePath": {'S' : event['queryStringParameters']['filePath']}
            }
        )
    except ClientError as e:
        return returnResponse(400, json.dumps(e.response['Error']['Message']))
    else:
        if 'Item' not in response:
            return returnResponse(404, "File not exist!")
        
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

# front-end sends a request to API GATEWAY
# get_file is invoked by API GATEWAY, get the file from S3
# get_file sends a response back to the front-end
