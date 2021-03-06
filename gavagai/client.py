from __future__ import absolute_import
import os
import types
import requests
import six
from .exceptions import GavagaiException, GavagaiHttpException


class GavagaiClient(object):
    """Client for Gavagai Rest API"""

    def __init__(self, apikey=None, host='https://api.gavagai.se',
                 api_version='v3', **kwargs):
        super(GavagaiClient, self).__init__()
        self.apikey = apikey
        self.host = host
        self.api_version = api_version
        self.default_request_options = kwargs
        if not self.apikey:
            try:
                self.apikey = os.environ['GAVAGAI_APIKEY']
            except KeyError:
                raise GavagaiException(
                    'GavagaiClient requires an apikey set explicitly \
                    or via the GAVAGAI_APIKEY environment variable'
                )

    def base_url(self):
        return self.host + '/' + self.api_version

    def request(self, path, method='post', body=None, allow_redirects=False):
        path = path.strip('/')
        url = self.base_url() + '/' + path + '?apiKey=' + self.apikey

        res = requests.request(method, url, json=body,
                               allow_redirects=allow_redirects,
                               **self.default_request_options)
        if res.status_code < 200 or res.status_code > 206:
            message = res.text or 'Unable to complete HTTP request'
            raise GavagaiHttpException(res.status_code, message)
        return res

    def _byod_request(self, resource_name, texts, **kwargs):
        if not isinstance(texts, list):
            raise ValueError('Argument texts is expected to be a list.')
        body = dict(language='en')
        body.update(kwargs)
        body['texts'] = ensure_text_objects(texts)
        return self.request(resource_name, 'post', body)

    def lexicon(self, term, language='en'):
        if not isinstance(term, str):
            raise ValueError('Argument term is expected to be a string.')
        path = '/lexicon/{0}/{1}'.format(language, term)
        return self.request(path, 'get')

    def keywords(self, texts, **kwargs):
        return self._byod_request('/keywords', texts, **kwargs)

    def stories(self, texts, **kwargs):
        return self._byod_request('/stories', texts, **kwargs)

    def topics(self, texts, **kwargs):
        return self._byod_request('/topics', texts, **kwargs)

    def tonality(self, texts, **kwargs):
        response = self._byod_request('/tonality', texts, **kwargs)
        # monkey patch this instance
        response.simple_list = types.MethodType(map_text_tonalities, response)
        return response


def ensure_text_objects(texts):
    text_objects = texts[:]
    for i, text in enumerate(text_objects):
        if isinstance(text, six.text_type) or isinstance(text, six.string_types):
            text_objects[i] = {'id': six.text_type(i), 'body': six.text_type(text)}
    return text_objects


def map_text_tonalities(response):
    data = response.json()
    return [map_tonality_to_dict(text) for text in data['texts']]


def map_tonality_to_dict(text):
    scores = lambda x: dict(score=x['score'],
                            normalized_score=x['normalizedScore'])
    name = lambda x: x['tone']
    tonality = {name(t): scores(t) for t in text['tonality']}
    return dict(id=text['id'], tonality=tonality)
