import os
import json
import httpretty
from gavagai.client import GavagaiClient

# TODO: put this in fixture
dir = os.path.dirname(__file__)
with open(os.path.join(dir, 'data/texts.json')) as json_file:
    texts = json.load(json_file)

@httpretty.activate
def test_default_language():
    httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/keywords',
                           body='{"foo": "bar"}', 
                           content_type='application/json')
    client = GavagaiClient('foo')
    client.keywords(texts)
    request = httpretty.last_request()
    assert '"language": "en"' in request.body


@httpretty.activate
def test_input_list_of_text_objects():
    httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/keywords',
                           body='{"foo": "bar"}', 
                           content_type='application/json')
    client = GavagaiClient('foo')
    client.keywords(texts)
    body = json.loads(httpretty.last_request().body)
    text_objects = body['texts']
    assert isinstance(text_objects, list)
    assert 'id' in text_objects[0]
    assert 'body' in text_objects[0]


@httpretty.activate
def test_input_list_of_strings():
    httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/keywords',
                           body='{"foo": "bar"}', 
                           content_type='application/json')
    client = GavagaiClient('foo')
    client.keywords(['this is a text', 'this is text 2', 'this is the third text'])
    body = json.loads(httpretty.last_request().body)
    assert body['texts'][2]['body'] == 'this is the third text'


@httpretty.activate
def test_custom_options_as_arguments():
    httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/keywords',
                           body='{"foo": "bar"}', 
                           content_type='application/json')
    client = GavagaiClient('foo')
    client.keywords(texts, language='sv', myCustomOption='optionally optional')    
    body = json.loads(httpretty.last_request().body)
    assert body['language'] == 'sv'
    assert body['myCustomOption'] == 'optionally optional' 


@httpretty.activate
def test_custom_options_as_dictionary():
    httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/keywords',
                           body='{"foo": "bar"}', 
                           content_type='application/json')
    options = {
        'anotherOption': 4711
        'language': 'no'
    }
    client = GavagaiClient('foo')
    client.keywords(texts, language='sv', myCustomOption='optionally optional')    
    body = json.loads(httpretty.last_request().body)
    assert body['language'] == 'no'
    assert body['anotherOption'] == 4711 


#    it('should handle custom options', function (done) {
#        var options = {
#            language: 'sv',
#            myCustomOption: 'optionally optional'
#        };
#
#        validateApiRequest(function (body) {
#            assert(body.language === 'sv', 'body language');
#            assert(body.myCustomOption === 'optionally optional', 'body customOption');
#            return requiredValues(body);
#        });
#
#        client.keywords(texts, options, function () {
#            assert(api.isDone() === true, "Matching API call.");
#            done();
#        });
#    });
