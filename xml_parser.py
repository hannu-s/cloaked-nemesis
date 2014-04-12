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

	def getKeys(self, tree):
		li = []
		for k in tree.findall('word'):
			num = k.get('occured')
			val = k.text
			li.append([val,num])
		return li	

	def getSites(self, tree):
		li = []
		for s in tree.findall('site'):
			li.append(s.text)
		return li