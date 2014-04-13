class Inspection(object):
	"""docstring for Inspection"""
	link = None
	score = None
	url = None
	fil = None
	
	def __init__(self, link, score, url, fil):
		self.link = link
		self.score = score
		self.url = url
		self.fil = fil
		