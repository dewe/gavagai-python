import json
import requests
from gavagai.client import GavagaiClient


def test_keywords():
    client = GavagaiClient()
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/keywords.json')

    r = client.keywords(texts)
    
    assert r.status_code == 200
    assert 'keywords' in r.json()
    assert len(r.json()['keywords']) > 0


def test_stories():
    client = GavagaiClient()
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/topics.json')
    
    r = client.stories(texts)
    
    assert r.status_code == 200
    assert 'stories' in r.json()
    assert len(r.json()['stories']) > 0


def test_tonality():
    client = GavagaiClient()
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/tonality.json')
    
    r = client.tonality(texts)
    
    assert r.status_code == 200
    assert 'texts' in r.json()
    assert len(r.json()['texts']) > 0


def test_topics():
    client = GavagaiClient()
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/topics.json')
    
    r = client.topics(texts)
    
    assert r.status_code == 200
    assert 'topics' in r.json()
    assert len(r.json()['topics']) > 0


def get_swagger_json(prop, url):
    res = requests.get(url)
    assert res.status_code == 200

    swagger = res.json()
    swagger_parameters = swagger['apis'][0]['operations'][0]['parameters']
    body_params = filter(lambda p: p['paramType'] == 'body', swagger_parameters)
    sample_body = body_params[0]['defaultValue']
    
    result = json.loads(sample_body)[prop]
    assert isinstance(result, list)
    assert len(result) > 0
    return result
