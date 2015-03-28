import requests
import httpretty
from gavagai.client import GavagaiClient


@httpretty.activate
def test_post_request():
	httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/test',
						   body='{"hello": "world"}', 
						   content_type='application/json')
	
	client = GavagaiClient('foo')
	response = client.request('test', method='POST', body={'test':'value'})

	assert response.json() == {'hello': 'world'}
	assert httpretty.last_request().method == 'POST'
	assert httpretty.last_request().headers['content-type'] == 'application/json'
	assert httpretty.last_request().path == '/v3/test?apiKey=foo'



@httpretty.activate
def test_default_method_post():
	httpretty.register_uri(httpretty.POST, 'https://api.gavagai.se/v3/test', body={})
	
	client = GavagaiClient('x')
	response = client.request('test')
	assert httpretty.last_request().method == 'POST'


@httpretty.activate
def test_empty_response():
	httpretty.register_uri(httpretty.GET, 'https://api.gavagai.se/v3/test', status=204)
	
	client = GavagaiClient('x')
	response = client.request('test', method='get')
	assert response.status_code == 204



