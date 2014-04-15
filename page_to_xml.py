from page_loader import PageLoader
from list_tool import ListTool
class PageToXML():
	def __init__(self, xmlInsp, keyWords = None, avoids = None):
		self.xmlInsp = xmlInsp
		self.keyWords = []
		self.avoids = []
		for obj in keyWords.words:
			self.keyWords.append(obj.word)
		for obj in avoids.words:
			self.avoids.append(obj.word)
		self.lMulti = 100
		self.tMulti = 50
		self.hMulti = 10
		self.sMulti = 5
		self.nMulti = 1

	def getScore(self):
		lt = ListTool()
		for data in self.xmlInsp:
			pl = PageLoader(data.fil)
			if not pl.isReadable():
				print('Abort. XMLInspections data corrupted. File not readable:', data.fil)
				return False
			pl.read()
			lWords = lt.getNonUniques(self.keyWords, pl.linkWords)
			tWords = lt.getNonUniques(self.keyWords, pl.titleWords)
			hWords = lt.getNonUniques(self.keyWords, pl.headerWords)
			sWords = lt.getNonUniques(self.keyWords, pl.specialWords)
			nWords = lt.getNonUniques(self.keyWords, pl.normalWords)
			score = len(lWords) * self.lMulti
			score += len(tWords) * self.tMulti
			score += len(hWords) * self.hMulti
			score += len(sWords) * self.sMulti
			score += len(nWords) * self.nMulti
			data.score = score
		return self.xmlInsp