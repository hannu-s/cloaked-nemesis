import xml.etree.ElementTree as ET
from inspection import Inspection
from word_list import WordList

class XMLReader():
	"""docstring for XMLReader"""
	def checkIfExists(self, fp):
		try:
			f = open(fp, "r")
			f.close()
		except Exception as e:
			print (e)
			return False
		return True

	def getTree(self, filePath):
		if not self.checkIfExists(filePath):
			return None
		return ET.parse(filePath)
		
		
class XMLWriter():
	def writeMIXML(self, dataList, filePath):
		root = ET.Element("findings")
		for ind, data in enumerate(dataList):
			if data.ID != None:
				ind = data.ID
			ele = ET.SubElement(root, "finding")
			ele.set('id', str(ind))

			field1 = ET.SubElement(ele, "link")
			field1.text = data.link

			field2 = ET.SubElement(ele, "score")
			field2.text = str(data.score)

			field3 = ET.SubElement(ele, "url")
			field3.text = data.url

			field4 = ET.SubElement(ele, "file")
			field4.text = data.fil

		tree = ET.ElementTree(root)
		tree.write(filePath)

	def writeWordXML(self, wl, filePath):
		root = ET.Element("words")
		for ind, data in enumerate(wl):
			ele = ET.SubElement(root, "word")

			field1 = ET.SubElement(ele, "link")
			field1.text = data.link
			field1.set()

		tree = ET.ElementTree(root)
		tree.write(filePath)