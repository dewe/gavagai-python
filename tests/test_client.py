from gavagai.client import GavagaiClient

def test_constructor_apikey():
	client = GavagaiClient("this_is_a_fake_apikey")
	assert client.apikey == "this_is_a_fake_apikey"
