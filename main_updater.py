from inspection import Inspection
from inspector import Inspector
from page_loader import PageLoader
import re
from word_list import WordList
from xml_rw import *
from xml_parser import XMLParser
from os_tool import OSTool
from page_to_xml import PageToXML

class MainUpdater():
	"""docstring for MainUpdater"""
	vote = None
	voteId = None
	miPath = None
	XMLInspections = []
	wl = None
	wordAvg = None
	avgRatio = None
	ratioDiff = 2
	keywords = None
	avoids = None

	def __init__(self, vote, voteId, miPath):
		self.vote = vote
		self.voteId = voteId
		self.miPath = miPath
		self.wordXMLPath = "xml/words.xml"

	def loadMasterInspection(self):
		insp = Inspector()
		self.XMLInspections = insp.getInspectionsStr(self.miPath)
		if len(self.XMLInspections) == 0:
			print('Abort. No data found in', self.miPath)
			exit()
		
	def storeWords(self):
		self.wl = WordList()
		xReader = XMLReader()
		xParser = XMLParser()

		if xReader.checkIfExistsQuiet('xml/words.xml'):
			tree = xReader.getTree('xml/words.xml')
			wordAvg, avgRatio = xParser.getGeneralFromWords(tree)
			self.wl = xParser.getWords(tree)

		usf = 0
		usl = 0
		if self.vote == "up":
			usf = 1
		else:
			usl = 1

		for ind, obj in enumerate(self.XMLInspections):
			if obj.ID != self.voteId:
				continue

			pl = PageLoader(obj.fil)
			if not pl.isReadable():
				print('Abort. File not readable:', obj.fil)
				exit()
			pl.read()

			patt = "^[a-zA-Z0-9]*$"
			pl.linkWords = self.removeListElesNotPatterned(patt, pl.linkWords)
			pl.titleWords = self.removeListElesNotPatterned(patt, pl.titleWords)
			pl.headerWords = self.removeListElesNotPatterned(patt, pl.headerWords)
			pl.specialWords = self.removeListElesNotPatterned(patt, pl.specialWords)
			pl.normalWords = self.removeListElesNotPatterned(patt, pl.normalWords)

			for word in pl.linkWords:
				self.wl.append(word, usf, usl)
			for word in pl.titleWords:
				self.wl.append(word, usf, usl)
			for word in pl.headerWords:
				self.wl.append(word, usf, usl)
			for word in pl.specialWords:
				self.wl.append(word, usf, usl)
			for word in pl.normalWords:
				self.wl.append(word, usf, usl)
			return

	def removeListElesNotPatterned(self, patt, li, maxLen = 255):
		indList = []
		for i in range(len(li)):
			if re.match(patt, li[i]) == None or len(li[i]) > maxLen:
				indList.append(i)
		for i in reversed(range(len(indList))):
			li.pop(indList[i])
		return li

	def deleteFile(self):
		for ind, obj in enumerate(self.XMLInspections):
			if obj.ID == self.voteId:
				os = OSTool()
				os.deleteFile(obj.fil)
				return

	def writeWordsXML(self):
		xWriter = XMLWriter()
		xWriter.writeWordXML(self.wl,self.wordAvg,self.avgRatio,self.wordXMLPath)

	def calculateKeywords(self):
		self.keywords = WordList()
		self.avoids = WordList()
		self.wordAvg = 0
		self.avgRatio = 0
		usef = 0
		usel = 0

		for data in self.wl.words:
			self.wordAvg += data.occ
			usef += data.usef
			usel += data.usel

		l = len(self.wl.words)
		if l == 0:
			l = 1
		self.wordAvg = self.wordAvg / l
		if usel == 0:
			self.avgRatio = usef
		else:
			self.avgRatio = usef / usel
		

		for data in self.wl.words:
			if data.usel == 0:
				ratio = data.usef
			else:
				ratio = data.usef / data.usel

			if ratio > self.avgRatio * self.ratioDiff:
				self.keywords.set(data.word, data.occ, data.usef, data.usel)
			elif ratio < self.avgRatio / self.ratioDiff:
				self.avoids.set(data.word, data.occ, data.usef, data.usel)

	def updateKeywordsXML(self):
		xWriter = XMLWriter()
		xWriter.writeKeywordsXML(self.keywords, self.avoids, 'xml/keywords.xml')
	
	def updateSitesXMl(self):
		xReader = XMLReader()
		xParser = XMLParser()
		xWriter = XMLWriter()
		tree = xReader.getTree('xml/sites.xml')
		gdSites, bdSites = xParser.getSites(tree)
		data = None
		for obj in self.XMLInspections:
			if obj.ID == self.voteId:
				data = obj
				break
		if self.vote == "up":
			gdSites.append(obj.url)
		else:
			bdSites.append(obj.url)
		xWriter.writeSitesXML(gdSites,bdSites,'xml/sites.xml')

	def getXMLInspScored(self):
		p = PageToXML(self.XMLInspections, self.keywords, self.avoids)
		self.XMLInspections = p.getScore()
		return self.XMLInspections

