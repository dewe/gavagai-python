import os
import json
import httpretty
from gavagai.client import GavagaiClient


texts = []

def setup_module(module):
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, 'data/texts.json')) as json_file:
        module.texts = json.load(json_file)


def setup_function(function):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/keywords',
                           body='{"foo": "bar"}', 
                           content_type='application/json')


def teardown_function(function):
    httpretty.disable()
    httpretty.reset()


def test_default_language():
    client = GavagaiClient('foo')
    client.keywords(texts)
    request = httpretty.last_request()
    assert '"language": "en"' in request.body


def test_input_list_of_text_objects():
    client = GavagaiClient('foo')
    client.keywords(texts)
    body = json.loads(httpretty.last_request().body)
    text_objects = body['texts']
    assert isinstance(text_objects, list)
    assert 'id' in text_objects[0]
    assert 'body' in text_objects[0]


def test_input_list_of_strings():
    client = GavagaiClient('foo')
    client.keywords(['this is a text', 'this is text 2', 'this is the third text'])
    body = json.loads(httpretty.last_request().body)
    assert body['texts'][2]['body'] == 'this is the third text'


def test_custom_options_as_arguments():
    client = GavagaiClient('foo')
    client.keywords(texts, language='sv', myCustomOption='optionally optional')    
    body = json.loads(httpretty.last_request().body)
    assert body['language'] == 'sv'
    assert body['myCustomOption'] == 'optionally optional' 


def test_custom_options_as_dictionary():
    client = GavagaiClient('foo')
    options = {
        'anotherOption': 4711,
        'language': 'no'
    }
    client.keywords(texts, **options)    
    body = json.loads(httpretty.last_request().body)
    assert body['language'] == 'no'
    assert body['anotherOption'] == 4711 
