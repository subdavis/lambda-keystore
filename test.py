from kvtoken import post_handler as kvtoken_post_handler
from keystore import post_handler as keystore_post_handler
from keystore import get_handler as keystore_get_handler
from keystore import delete_handler as keystore_delete_handler

class mockTable:
    def __init__(self):
        self.items = []

    def put_item(self, **kwargs):
        self.items.append(kwargs['Item'])
        print("Item put: " + str(self.items))

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
    a = kvtoken_post_handler.post({ "requestContext": { "identity": {
        "sourceIp": "1.2.3.4",
        "userAgent": "Foobar"
        }}},{})
    assert a['statusCode'] == 201

def test_keystore_post():
    keystore_post_handler.dynamodb = mockDynamo()
    a = keystore_post_handler.post({
        'body':'{"ttl": "IDK", "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert a['statusCode'] == 400
    b = keystore_post_handler.post({
        'body':'{"ttl": 123456789, "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert b['statusCode'] == 201

def test_keystore_get():
    keystore_get_handler.dynamodb = mockDynamo()
    a = keystore_get_handler.get({
        'pathParameters': { 'key':'foo'},
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert a['statusCode'] == 200

def test_keystore_delete():
    keystore_delete_handler.dynamodb = mockDynamo()
    a = keystore_delete_handler.delete({
        'pathParameters': { 'key':'foo'},
        'headers':{
            'Authorization': "Bearer: foobar"
        }},{})
    assert a['statusCode'] == 200

if __name__ == "__main__":

    test_kvtoken_post()
    test_keystore_post()
    test_keystore_get()
    test_keystore_delete()