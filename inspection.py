class Inspection(object):
	"""docstring for Inspection"""
	link = None
	score = None
	url = None
	fil = None
	ID = None
	
	def __init__(self, link, score, url, fil, ID = None):
		self.link = link
		self.score = score
		self.url = url
		self.fil = fil
		self.ID = ID