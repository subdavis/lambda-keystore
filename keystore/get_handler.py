import boto3
import uuid
import json
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get(event, context):
    key = event.get('pathParameters')
    keystoreTable = dynamodb.Table('keystore')

    item = {
        'id': str(uuid.uuid1()),
        'foo': 'bar'
    }

    # write the todo to the database
    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": "Iguess"
    }

    return response