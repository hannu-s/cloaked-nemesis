class XMLParser():
	"""docstring for XMLParser"""
	def getSearchParams(self, confT):
		li = []
		for sp in confT.findall('params/search_param'):
			li.append(sp.text)
		return li
	
	def getSearchSites(self, confT):
		li = []
		for si in confT.findall('sites/site'):
			li.append(si.text)
		return li	

	def getPagesToSearch(self, confT):
		return int(confT.find('pages').text)

	def getFKeys(self, tree):
		li = []
		for k in tree.findall('word'):
			li.append(k.text)
		return li	

	def getKeywords(self, tree):
		li = []
		for k in tree.findall('keywords/word'):
			num = int(k.get('occured'))
			val = k.text
			li.append([val,num])
		return li	

	def getAvoids(self, tree):
		li = []
		for k in tree.findall('avoids/word'):
			num = int(k.get('occured'))
			val = k.text
			li.append([val,num])
		return li	

	def getSites(self, tree):
		li = []
		for s in tree.findall('site'):
			li.append(s.text)
		return li