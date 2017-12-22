import boto3
import hashlib
import uuid
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def post(event, context):
    # Gather what we need about the client.
    # Never store ip or user agent in the clear to preserve my users' privacy
    # TODO: salt these!
    ip = event.get('requestContext').get('identity').get('sourceIp').encode('utf-8')
    ipHash = hashlib.sha224(ip).hexdigest()
    
    userAgent = event.get('requestContext').get('identity').get('userAgent').encode('utf-8')
    userAgentHash = hashlib.sha224(userAgent).hexdigest()

    tokenTable = dynamodb.Table('token')

    tokenItem = {
        'id': str(uuid.uuid1()),
        'ipHash': ipHash,
        'ipHash_salt': "foo",
        'userAgentHash': userAgentHash,
        'userAgentHash_salt' : "foo"
    }

    # write the todo to the database
    tokenTable.put_item(Item=tokenItem,ReturnValues='NONE')

    response = {
        "statusCode": 201,
        "body": json.dumps({
            'id': tokenItem.get('id')
        })
    }

    return response