from page_loader import PageLoader
from list_tool import ListTool
class PageToXML():
	def __init__(self, xmlInsp, keyWords = None, avoids = None):
		self.xmlInsp = xmlInsp
		self.keyWords = keyWords
		self.avoids = avoids
		self.lMulti = 100
		self.tMulti = 50
		self.hMulti = 10
		self.sMulti = 5
		self.nMulti = 1

	def getScore():
		lt = ListTool()
		for data in self.xmlInsp:
			pl = PageLoader(data.fil)
			if not pl.isReadable():
				print('Abort. XMLInspections data corrupted. File not readable:', data.fil)
				return
			pl.read()
			lWords = lt.addOnlyUniqueFromList(self.keyWords, pl.linkWords)
			tWords = lt.addOnlyUniqueFromList(self.keyWords, pl.titleWords)
			hWords = lt.addOnlyUniqueFromList(self.keyWords, pl.headerWords)
			sWords = lt.addOnlyUniqueFromList(self.keyWords, pl.specialWords)
			nWords = lt.addOnlyUniqueFromList(self.keyWords, pl.normalWords)
			score = len(lWords) * self.lMulti
			score += len(tWords) * self.tMulti
			score += len(hWords) * self.hMulti
			score += len(sWords) * self.sMulti
			score += len(nWords) * self.nMulti
			data.score = score
		return self.xmlInsp