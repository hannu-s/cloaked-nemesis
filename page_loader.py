from xml_rw import XMLReader

class PageLoader():
	"""docstring for PageLoader"""
	path = None
	linkWords = []
	titleWords = []
	headerWords = []
	specialWords = []
	normalWords = []
	def __init__(self, path):
		self.path = path
		
	def isReadable(self):
		xr = XMLReader()
		return xr.checkIfExists(self.path)

	def read(self):
		content = list()
		with open(self.path) as f:
			content = f.readlines()
		if len(content) < 5:
			print('Abort. File has less than 5 lines.')
			return
		self.linkWords = content[0].replace("\n","").split(" ")
		self.titleWords = content[1].replace("\n","").split(" ")
		self.headerWords = content[2].replace("\n","").split(" ")
		self.specialWords = content[3].replace("\n","").split(" ")
		self.normalWords = content[4].replace("\n","").split(" ")