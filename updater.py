import sys
from xml_rw import XMLReader, XMLWriter
from xml_parser import XMLParser
from inspection import Inspection
from inspector import Inspector

class Updater(object):
	vote = None
	voteId = None
	masterInspectionPath = None
	XMLInspections = []

	def __init__(self, vote, voteId):
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
			#start master_updater
			pass
		
	def removeIdElementFromMasterInspection(self):
		for ind, obj in enumerate(self.XMLInspections):
			if obj.ID == self.voteId:
				self.XMLInspections.pop(ind)
				return
		print('Abort. Failed to remove id:', self.voteId)
		exit()

	def writeNewMasterInspectionXML(self):
		xWriter = XMLWriter()
		xWriter.writeMIXML(self.XMLInspections, self.masterInspectionPath)

def main(v,i):
	up = Updater(v,i)
	up.loadMasterInspection()
	up.voteHandling()
	up.removeIdElementFromMasterInspection()
	up.writeNewMasterInspectionXML()
	print('Done')

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])