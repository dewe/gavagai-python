import requests
import httpretty
from gavagai.client import GavagaiClient


@httpretty.activate
def test_yipit_api_returning_deals():
    httpretty.register_uri(httpretty.GET, "http://api.yipit.com/v1/deals/",
                           body='[{"title": "Test Deal"}]',
                           content_type="application/json")

    response = requests.get('http://api.yipit.com/v1/deals/')
    assert response.json() == [{'title': 'Test Deal'}]


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


#        client.request({method: 'POST', url: '/test', body: {}}, function (err, data) {
#            assert(data.apiClientResponse.statusCode === 200, 'statusCode 200');
#            assert.deepEqual(data, {hello: 'world'});
#            done();
#        });
