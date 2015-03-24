from gavagai.client import GavagaiClient

def test_constructor_apikey():
	client = GavagaiClient("this_is_a_fake_apikey")
	assert client.apikey == "this_is_a_fake_apikey"

def test_default_host():
	client = GavagaiClient("fake_apikey")
	assert client.host == "https://api.gavagai.se"