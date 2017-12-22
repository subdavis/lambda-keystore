import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import uuid
import json
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def delete(event, context):
    owner_token = event.get('headers').get('Authorization', -1)
    if owner_token == -1:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Unauthorized"})
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
    
    try:
        query_result = keyStoreTable.delete_item(Key={
            'owner': owner_token,
            'key': key
        })
    except ClientError as e:
        return {
            'statusCode': 500,
            "body": json.dumps({'error':'unknown'})
        }
    else:
        print("DeleteItem succeeded:")
        return {
            "statusCode": 200,
            "body": json.dumps({"key": key})
        }