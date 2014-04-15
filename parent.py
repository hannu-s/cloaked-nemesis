from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml_rw import *
from xml_parser import XMLParser
from associations import Associations
from connector import ConnectionManager
from configure import Configure
from sites import Sites
from list_tool import ListTool
from os_tool import OSTool
from inspection import Inspection
from sorter import Sorter
from inspector import Inspector


class BLParent():
	"""docstring for BLParent"""
	__conf = None
	__associations = None
	__sites = None
	
	resultList = None
	masterInspectionPath = None

	def __init__(self):
		self.__conf = Configure()
		self.__associations = Associations()
		self.__sites = Sites()
		resultList = []

		xReader = XMLReader()
		xParser = XMLParser()
		confTree = xReader.getTree('xml/conf.xml')
		if confTree == None:
			exit()
		searchParams = xParser.getSearchParams(confTree)
		searchSites = xParser.getSearchSites(confTree)
		pagesToSearch = xParser.getPagesToSearch(confTree)
		self.masterInspectionPath = xParser.getMIXML(confTree)

		self.__conf.setParams(searchSites, searchParams, pagesToSearch)

		keywordTree = xReader.getTree('xml/keywords.xml')
		fKeywordTree = xReader.getTree('xml/f_keywords.xml')
		if keywordTree == None or fKeywordTree == None:
			exit()
		keywords = xParser.getKeywords(keywordTree)
		fKeywords = xParser.getKeywords(fKeywordTree)
		avoids = xParser.getAvoids(keywordTree)
		fAvoids = xParser.getAvoids(fKeywordTree)

		self.__associations.setParams(keywords, avoids, fKeywords, fAvoids)

		sitesTree = xReader.getTree('xml/sites.xml')
		if sitesTree == None:
			exit()
		goodSites, badSites = xParser.getSites(sitesTree)

		self.__sites.setParams(goodSites, badSites)

	def startSubProcesses(self):
		CM = ConnectionManager()
		lt = ListTool()
		sitesList = []
		sitesList = lt.addOnlyUniqueFromList(self.__sites.goodSites, self.__sites.badSites)

		CM.initializeConnection(	self.__associations.keywordsList, 	self.__associations.avoidsList, 
									sitesList, 	self.__conf.siteToSearchList,	 self.__conf.pagesToSearch, 
									self.__conf.searchParamsList)
		CM.startThread()
		CM.join()
		CM.parseResults()
		
		self.resultList = CM.getResults()		

	def createMasterInspectionXML(self, delChildXMLs = False):
		lt = ListTool()
		os = OSTool()
		sort = Sorter()
		insp = Inspector()

		xmls = os.getFilesInDir('results/')
		xmls = lt.popByWord(xmls, self.masterInspectionPath)

		XMLInspections = insp.getInspections(xmls)				

		if len(XMLInspections) == 0:
			print('No files read.')
			exit()

		XMLInspections = sort.sortInspectionList(XMLInspections)

		xWriter = XMLWriter()
		xWriter.writeMIXML(XMLInspections, self.masterInspectionPath)

		if delChildXMLs:
			for xml in xmls:
				os.deleteFile(xml)

	def startServerProg(self):
		os = OSTool()
		os.startProgram('google-chrome', 'localhost:80/tracker/')

def main():
	bl = BLParent()
	bl.startSubProcesses()
	bl.createMasterInspectionXML(False)
	bl.startServerProg()
	

if __name__ == '__main__':
	main()
