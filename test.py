import boto3
from kvtoken import post_handler as kvtoken_post_handler
from keystore import post_handler as keystore_post_handler

class mockTable:
    def __init__(self):
        self.items = []

    def put_item(self, **kwargs):
        self.items.append(kwargs['Item'])
        print("Items are now: " + str(self.items))

    def query(self, **kwargs):
        return 'foobar'

class mockDynamo:
    def Table(self, token):
        return mockTable()

def test_kvtoken_post():
    kvtoken_post_handler.dynamodb = mockDynamo()
    kvtoken_post_handler.post({ "requestContext": { "identity": {
        "sourceIp": "1.2.3.4",
        "userAgent": "Foobar"
    }}},{})

def test_keystore_post():
    keystore_post_handler.dynamodb = mockDynamo()
    keystore_post_handler.post({
        'body':'{"ttl": "IDK", "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})

if __name__ == "__main__":

    test_kvtoken_post()
    test_keystore_post()