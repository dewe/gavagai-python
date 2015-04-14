import os
import types
import requests
from exceptions import GavagaiException, GavagaiHttpException


class GavagaiClient(object):
    """Client for Gavagai Rest API"""
    
    def __init__(self, apikey=None, host='https://api.gavagai.se', api_version='v3'):
        super(GavagaiClient, self).__init__()

        self.apikey = apikey
        self.host = host
        self.api_version = api_version

        if not self.apikey:
            try:
                self.apikey = os.environ['GAVAGAI_APIKEY']
            except KeyError:
                raise GavagaiException('GavagaiClient requires an apikey set explicitly \
                                        or via the GAVAGAI_APIKEY environment variable')

    def base_url(self):
        return self.host + '/' + self.api_version

    def request(self, path, method='post', body=None, allow_redirects=False):
        path = path.strip('/')
        url = self.base_url() + '/' + path + '?apiKey=' + self.apikey

        res = requests.request(method, url, json=body, allow_redirects=allow_redirects)
        if res.status_code < 200 or res.status_code > 206:
            message = res.text or 'Unable to complete HTTP request'
            raise GavagaiHttpException(res.status_code, message)
        
        return res
    
    def keywords(self, texts, **kwargs):
        if not isinstance(texts, list):
            raise ValueError('Argument texts is expected to be a list.')
        body = dict(language='en') 
        body.update(kwargs)
        body['texts'] = ensure_text_objects(texts)
        return self.request('keywords', 'post', body)

    def tonality(self, texts, **kwargs):
        if not isinstance(texts, list):
            raise ValueError('Argument texts is expected to be a list.')
        body = dict(language='en') 
        body.update(kwargs)
        body['texts'] = ensure_text_objects(texts)

        response = self.request('tonality', 'post', body)
        response.simple_list = types.MethodType(map_text_tonalities, response) # monkey patch this instance
        return response


def ensure_text_objects(texts):
    text_objects = texts[:]
    for i in range(len(text_objects)):
        text = text_objects[i]
        if isinstance(text, unicode) or isinstance(text, basestring):
            text_objects[i] = { 'id': unicode(i), 'body': unicode(text) }
    return text_objects


def map_text_tonalities(self):
    data = self.json()
    return [map_tonality_to_dict(text) for text in data['texts']]


def map_tonality_to_dict(text):
    scores = lambda t: {'score':t['score'], 'normalized_score':t['normalizedScore']}
    tonality = {t['tone']:scores(t) for t in text['tonality']}
    return dict(id=text['id'], tonality=tonality)


