import pytest
import httpretty
from requests import ConnectionError
from gavagai.client import GavagaiClient
from gavagai.exceptions import GavagaiHttpException


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
    
    client = GavagaiClient('foo')
    client.request('test')
    assert httpretty.last_request().method == 'POST'


@httpretty.activate
def test_empty_response():
    httpretty.register_uri(httpretty.GET, 'https://api.gavagai.se/v3/test', status=204)
    
    client = GavagaiClient('foo')
    response = client.request('test', method='get')
    assert response.status_code == 204


@httpretty.activate
def test_default_exception_value_if_no_error_message_from_api():
    httpretty.register_uri(httpretty.GET, 'https://api.gavagai.se/v3/test', status=500, body=None)

    client = GavagaiClient('foo')
    with pytest.raises(GavagaiHttpException) as ex:
        client.request('test', method='get')
    assert 'Unable to complete HTTP request' in ex.value


@httpretty.activate
def test_connection_error_exception_on_host_unreachable():
    client = GavagaiClient('x', host='http://unreachablehost')
    with pytest.raises(ConnectionError):
        client.request('test', method='get')

#it('should return error on host unreachable', function (done) {
#       nock(client.host).get('/unreachable_path');

#       client.request({method: 'GET', url: '/test'}, function (err, data) {
#           assert.match(err.message, /Unable to reach host:/);
#           done();
#       });
#   });

