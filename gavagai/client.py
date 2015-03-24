class GavagaiClient(object):
	"""Client for Gavagai Rest API"""
	def __init__(self, apikey):
		super(GavagaiClient, self).__init__()
		self.apikey = apikey
		