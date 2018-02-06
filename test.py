from kvtoken import post_handler as kvtoken_post_handler
from keystore import post_handler as keystore_post_handler
from keystore import get_handler as keystore_get_handler
from keystore import delete_handler as keystore_delete_handler
import time 

class mockTable:
    def __init__(self, expiry):
        self.items = []
        self.expiry = expiry

    def put_item(self, **kwargs):
        self.items.append(kwargs['Item'])
        print("Item put: " + str(self.items))

    def delete_item(self, **kwargs):
        pass

    def query(self, **kwargs):
        return {'Items': [{
            "key":"foo", 
            "value": "bar", 
            "ttl": self.expiry }]}

class mockDynamo:
    def __init__(self, expiry):
        self.table = mockTable(expiry)
    def Table(self, token):
        return self.table

def test_kvtoken_post():
    kvtoken_post_handler.dynamodb = mockDynamo(time.time())
    a = kvtoken_post_handler.post({ "requestContext": { "identity": {
        "sourceIp": "1.2.3.4",
        "userAgent": "Foobar"
        }}},{})
    assert a['statusCode'] == 201

def test_keystore_post():
    keystore_post_handler.dynamodb = mockDynamo(time.time())
    a = keystore_post_handler.post({
        'body':'{"ttl": "IDK", "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert a['statusCode'] == 400
    b = keystore_post_handler.post({
        'body':'{"ttl": 12345, "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert b['statusCode'] == 400
    c = keystore_post_handler.post({
        'body':'{"ttl": 9999999999, "key": "foo", "value": "bar"}',
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert c['statusCode'] == 201

def test_keystore_get():
    now = time.time()
    keystore_get_handler.dynamodb = mockDynamo(now + 100) # expires in the future
    a = keystore_get_handler.get({
        'pathParameters': { 'key':'foo'},
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert a['statusCode'] == 200
    keystore_get_handler.dynamodb = mockDynamo(now - 100) # expires in the past
    b = keystore_get_handler.get({
        'pathParameters': { 'key':'foo'},
        'headers':{
            'Authorization': "Bearer: foobar"
        }}, {})
    assert  b['statusCode'] == 410 # Gone

def test_keystore_delete():
    keystore_delete_handler.dynamodb = mockDynamo(time.time())
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