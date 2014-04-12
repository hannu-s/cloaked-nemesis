import xml.etree.ElementTree as ET
class XMLReader():
	"""docstring for XMLReader"""
	def __checkIfExists(self, fp):
		try:
			f = open(fp, "r")
			f.close()
		except Exception as e:
			print (e)
			return False
		return True

	def getTree(self, filePath):
		if not self.__checkIfExists(filePath):
			return None
		return ET.parse(filePath)
		
		
class XMLWriter():
	def writeXML(self, tree, filePath):
		try:
			tree.write(filePath)
		except Exception as e:
			print (e)