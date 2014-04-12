class Configure():
	siteToSearchList = []
	searchParamsList = []
	pagesToSearch = None

	def __init__(self):
		pass

	def setParams(self, sites, params, pagesToSearch):
		self.siteToSearchList = sites
		self.searchParamsList = params
		self.pagesToSearch = pagesToSearch