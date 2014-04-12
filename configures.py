class Configures():
	siteToSearchList = []
	searchParamsList = []
	pagesToSearch = None

	def __init__(self, sites, params, pagesToSearch):
		self.siteToSearchList = sites
		self.searchParamsList = params
		self.pagesToSearch = pagesToSearch