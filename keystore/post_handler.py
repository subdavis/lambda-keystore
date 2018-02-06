import boto3
from boto3.dynamodb.conditions import Key
import json
import uuid
import time

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
    

    if (len(query_result.get('Items', [])) != 1):
        return {
            "statusCode": 401, 
            "body": json.dumps({"error": "token not found"})
        }

    body = json.loads(event.get('body'))

    def verify():
        if type(body.get('key')) not in [str, unicode]:
            return False
        if type(body.get('value')) not in [str, unicode]:
            return False
        if type(body.get('ttl')) is not int:
            return False
        now = int(time.time()) # Seconds
        order_of_magnitude = body.get('ttl') / now # assert ttl > now
        if not int(order_of_magnitude) in range(1, 9):
            return False
        return True
    
    if verify() == False:
        return {
            "statusCode": 400,
            "body": json.dumps({"error":"bad body payload"})
        }

    item = {
        'id': str(uuid.uuid1()),
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
        "body": json.dumps(item)
    }

    return response