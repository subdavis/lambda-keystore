import boto3
from boto3.dynamodb.conditions import Key
import json
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def post(event, context):

    owner_token = event.get('headers').get('Authorization', -1)
    if owner_token == -1:
        return {
            "statusCode": 401,
            "body": "Unauthorized"
        }
    else:
        owner_token = owner_token.split(' ')[-1] # Last word in the string

    tokenTable = dynamodb.Table('token')
    query_result = tokenTable.query(KeyConditionExpression=Key('id').eq(owner_token))
    
    response = None
    if (len(query_result.get('Items', [])) != 1):
        response = {
            "statusCode": 401, 
            "body": str({"error": "token not found"})
        }
    else:
        body = json.loads(event.get('body'))
        item = {
            'key': body.get('key'),
            'value': body.get('value'),
            'owner': owner_token,
            'ttl': body.get('ttl')
        }

        # write the todo to the database
        keystoreTable = dynamodb.Table('keystore')
        keystoreTable.put_item(Item=item)

        response = {
            "statusCode": 201,
            "body": str(item)
        }

    return response