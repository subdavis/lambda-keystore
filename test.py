import boto3
from kvtoken import post_handler as kvtoken_post_handler
from keystore import post_handler as keystore_post_handler
from keystore import get_handler as keystore_get_handler
from keystore import delete_handler as keystore_delete_handler

class mockTable:
    def __init__(self):
        self.items = []

    def put_item(self, **kwargs):
        self.items.append(kwargs['Item'])
        print("Items are now: " + str(self.items))

    def delete_item(self, **kwargs):
        print("Deleting item")

    def query(self, **kwargs):
        print("Ran query")
        return {'Items': [{"key":"foo"}]}

class mockDynamo:
    def Table(self, token):
        return mockTable()

def test_kvtoken_post():
    kvtoken_post_handler.dynamodb = mockDynamo()
    return kvtoken_post_handler.post({ "requestContext": { "identity": {
        "sourceIp": "1.2.3.4",
        "userAgent": "Foobar"
        }}},{})

def test_keystore_post():
    keystore_post_handler.dynamodb = mockDynamo()
    return keystore_post_handler.post({
        'body':'{"ttl": "IDK", "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})

def test_keystore_get():
    keystore_get_handler.dynamodb = mockDynamo()
    return keystore_get_handler.get({
        'pathParameters': { 'key':'foo'},
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})

def test_keystore_delete():
    keystore_delete_handler.dynamodb = mockDynamo()
    return keystore_delete_handler.delete({
        'pathParameters': { 'key':'foo'},
        'headers':{
            'Authorization': "Bearer: foobar"
        }},{})

if __name__ == "__main__":

    print(test_kvtoken_post())
    print(test_keystore_post())
    print(test_keystore_get())
    print(test_keystore_delete())