import boto3
import hashlib
import uuid

dynamodb = boto3.resource('dynamodb')

def post(event, context):
    # Gather what we need about the client.
    # Never store ip or user agent in the clear to preserve my users' privacy
    # TODO: salt these!
    ip = event.requestContext.identity.sourceIp
    ipHash = hashlib.sha224(ip).hexdigest()
    
    userAgent = event.requestContext.identity.userAgent
    userAgentHash = hashlib.sha224(userAgent).hexdigest

    tokenTable = dynamodb.Table('token')

    tokenItem = {
        'id': str(uuid.uuid1()),
        'ipHash': ipHash,
        'ipHash_salt': "",
        'userAgentHash': userAgentHash,
        'userAgentHash_salt' : ""
    }

    # write the todo to the database
    table.put_item(Item=tokenItem)

    response = {
        "statusCode": 200,
        "body": {
            'id': tokenItem.id,
        }
    }

    return response