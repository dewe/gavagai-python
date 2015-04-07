import os
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

    def request(self, path, method='post', body=None):
        url = self.base_url() + '/' + path + '?apiKey=' + self.apikey
        res = requests.request(method, url, json=body)
        
        if res.status_code < 200 or res.status_code > 206:
            raise GavagaiHttpException('Unable to complete HTTP request')
        
        return res
        