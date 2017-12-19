import boto3
import uuid
dynamodb = boto3.resource('dynamodb')

def get(event, context):
    table = dynamodb.Table('keystore')

    item = {
        'id': str(uuid.uuid1()),
        'foo': 'bar'
    }

    # write the todo to the database
    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response