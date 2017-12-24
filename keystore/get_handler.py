import boto3
from boto3.dynamodb.conditions import Key
import uuid
import json
import time
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get(event, context):
    owner_token = event.get('headers').get('Authorization', -1)
    if owner_token == -1:
        return {
            "statusCode": 401,
            "body": str({"error": "Unauthorized"})
        }
    else:
        owner_token = owner_token.split(' ')[-1] # Last word in the string

    tokenTable = dynamodb.Table('token')
    query_result = tokenTable.query(KeyConditionExpression=Key('id').eq(owner_token))

    if (len(query_result.get('Items', [])) != 1):
        return {
            "statusCode": 401, 
            "body": json.dumps({"error": "Unauthorized"})
        }

    key = event.get('pathParameters').get('key')

    keyStoreTable = dynamodb.Table('keystore')
    query_result = keyStoreTable.query(KeyConditionExpression=Key('owner').eq(owner_token) & Key('key').eq(key))
    items = query_result.get('Items', [])

    if (len(items) >= 1):

        item = items[0]
        now = int(time.time()) # Seconds
        order_of_magnitude = now / item['ttl']

        if (int(order_of_magnitude) in range(0, 10) and item['ttl'] > now):
            
            return {
                "statusCode": 200,
                "body": json.dumps(item)
            }

        return {
            "statusCode": 410,
            "body": json.dumps({"error": key + " expired"})
        }

    return {
        "statusCode": 404,
        "body": json.dumps({"error": key + " not found"})
    }