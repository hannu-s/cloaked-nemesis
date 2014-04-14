from inspection import Inspection
from inspector import Inspector
from page_loader import PageLoader
import re
from word_list import WordList
from xml_rw import *

class MainUpdater():
	"""docstring for MainUpdater"""
	vote = None
	voteId = None
	miPath = None
	XMLInspections = []

	def __init__(self, vote, voteId, miPath):
		self.vote = vote
		self.voteId = voteId
		self.miPath = miPath

	def loadMasterInspection(self):
		insp = Inspector()
		self.XMLInspections = insp.getInspectionsStr(self.miPath)
		if len(self.XMLInspections) == 0:
			print('Abort. No data found in', self.miPath)
			exit()
		
	def storeWords(self):
		wl = WordList()

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
				wl.append(word, usf, usl)
			for word in pl.titleWords:
				wl.append(word, usf, usl)
			for word in pl.headerWords:
				wl.append(word, usf, usl)
			for word in pl.specialWords:
				wl.append(word, usf, usl)
			for word in pl.normalWords:
				wl.append(word, usf, usl)

		#get general from xml
		#get words from xml
		#append to wlist
		#write xml

	def removeListElesNotPatterned(self, patt, li, maxLen = 255):
		indList = []
		for i in range(len(li)):
			if re.match(patt, li[i]) == None or len(li[i]) > maxLen:
				indList.append(i)
		for i in reversed(range(len(indList))):
			li.pop(indList[i])
		return li