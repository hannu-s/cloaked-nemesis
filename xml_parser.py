from word_list import WordList

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

	def getMIXML(self, confT):
		return confT.find('mixml').text

	def getFKeys(self, tree):
		li = []
		for k in tree.findall('word'):
			li.append(k.text)
		return li	

	def getKeywords(self, tree):
		li = []
		for k in tree.findall('keywords/word'):
			val = k.text
			li.append(val)
		return li	

	def getAvoids(self, tree):
		li = []
		for k in tree.findall('avoids/word'):
			val = k.text
			li.append(val)
		return li	

	def getSites(self, tree):
		gd = []
		bd = []
		for s in tree.findall('good_sites/site'):
			gd.append(s.text)
		for s in tree.findall('bad_sites/site'):
			bd.append(s.text)
		return gd,bd

	def getInspectionData(self, tree):
		link = []
		score = []
		url = []
		fil= []

		for data in tree.findall('finding'):
			link.append(data.find('link').text)
			score.append(data.find('score').text)
			url.append(data.find('url').text)
			fil.append(data.find('file').text)

		return link, score, url, fil

	def getInspectionDataWithId(self, tree):
		link = []
		url = []
		score = []
		fil = []
		ID = []

		for data in tree.findall('finding'):
			link.append(data.find('link').text)
			score.append(data.find('score').text)
			url.append(data.find('url').text)
			fil.append(data.find('file').text)
			ID.append(data.get('id'))

		return link, score, url, fil, ID

	def getGeneralFromWords(self, tree):
		wordAvg = float(tree.find('general/word_avg').text)
		avgRatio = float(tree.find('general/avg_ratio').text)
		return wordAvg, avgRatio

	def getWords(self, tree):
		wl = WordList()
		for data in tree.findall('words/word'):
			word = data.text
			occ = int(data.get('occured'))
			usf = int(data.get('useful'))
			usl = int(data.get('useless'))
			wl.set(word,occ,usf,usl)
		return wl

