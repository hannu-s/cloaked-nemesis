from inspection import Inspection
from xml_rw import XMLReader
from xml_parser import XMLParser

class Inspector():
	"""docstring for Inspector"""

	def getInspections(self, xmls):
		xReader = XMLReader()
		xParser = XMLParser()
		XMLInspections = []
		for ind, xml in enumerate(xmls):
			tree = xReader.getTree(xml)
			if tree == None:
				print(ind, xml, 'Failed to read.')
				continue
			link, score, url, fil = xParser.getInspectionData(tree)
			for i in range(len(link)):
				XMLInspections.append( Inspection(link[i], score[i], url[i], fil[i]) )
		return XMLInspections