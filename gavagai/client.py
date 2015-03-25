import os

class GavagaiClient(object):
    """Client for Gavagai Rest API"""
    
    def __init__(self, apikey=None, host='https://api.gavagai.se', api_version='v3'):
        super(GavagaiClient, self).__init__()
        self.apikey = apikey or os.environ['GAVAGAI_APIKEY']
        self.host = host
        self.api_version = api_version

    def base_url(self):
        return self.host + '/' + self.api_version
        