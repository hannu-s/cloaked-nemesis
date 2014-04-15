import sys
from xml_rw import XMLReader, XMLWriter
from xml_parser import XMLParser
from inspection import Inspection
from inspector import Inspector
from main_updater import MainUpdater
from sorter import Sorter

class Updater():
	vote = None
	voteId = None
	masterInspectionPath = None
	XMLInspections = []

	def __init__(self, vote, voteId, skip = False):
		if skip:
			return
		self.vote = vote
		self.voteId = voteId

		xReader = XMLReader()
		xParser = XMLParser()
		confTree = xReader.getTree('xml/conf.xml')
		if confTree == None:
			print('Abort. Failed to read xml/conf.xml')
			exit()
		self.masterInspectionPath = xParser.getMIXML(confTree)

	def loadMasterInspection(self):
		insp = Inspector()
		self.XMLInspections = insp.getInspectionsStr(self.masterInspectionPath)
		if len(self.XMLInspections) == 0:
			print('Abort. No data found in', self.masterInspectionPath)
			exit()

	def voteHandling(self):
		if (self.vote != "dis"):
			m = MainUpdater(self.vote, self.voteId, self.masterInspectionPath)
			m.loadMasterInspection()
			m.storeWords()
			m.calculateKeywords()
			m.updateKeywordsXML()
			m.writeWordsXML()
			m.updateSitesXMl()
			self.XMLInspections = m.getXMLInspScored()
			m.deleteFile()
		else:
			self.loadMasterInspection()

		
	def removeIdElementFromMasterInspection(self):
		for ind, obj in enumerate(self.XMLInspections):
			if obj.ID == self.voteId:
				self.XMLInspections.pop(ind)
				return
		print('Abort. Failed to remove id:', self.voteId)
		exit()

	def writeNewMasterInspectionXML(self):
		sort = Sorter()
		self.XMLInspections = sort.sortInspectionList(self.XMLInspections)
		xWriter = XMLWriter()
		xWriter.writeMIXML(self.XMLInspections, self.masterInspectionPath)

def main(v,i):
	up = Updater(v,i)
	up.voteHandling()
	#up.loadMasterInspection()
	up.removeIdElementFromMasterInspection()
	up.writeNewMasterInspectionXML()

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])