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

class BLParent():
	"""docstring for BLParent"""
	__conf = None
	__associations = None
	__sites = None
	
	resultList = None
	masterInspectionPath = 'results/master_inspection.xml'

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

		goodSitesTree = xReader.getTree('xml/good_sites.xml')
		badSitesTree = xReader.getTree('xml/bad_sites.xml')
		if goodSitesTree == None or badSitesTree == None:
			exit()
		goodSites = xParser.getSites(goodSitesTree)
		badSites = xParser.getSites(badSitesTree)

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
		print(self.resultList)		

	def createMasterInspectionXML(self):
		xReader = XMLReader()
		xParser = XMLParser()
		lt = ListTool()
		os = OSTool()
		
		xmls = os.getFilesInDir('results/')
		xmls = lt.popByWord(xmls, self.masterInspectionPath)

		childInspections = []
		for ind, xml in enumerate(xmls):
			tree = xReader.getTree(xml)
			if tree == None:
				print(ind, xml, 'Failed to read.')
				continue
			link, score, url, fil = xParser.getInspectionData(tree)	
			childInspections.append( Inspection(link, score, url, fil) )

		if len(childInspections) == 0:
			print('No files read.')
			exit()

		#TODO
		#sort childInspections

		xWriter = XMLWriter()
		xWriter.writeMIXML(childInspections, self.masterInspectionPath)

		#miTree = xReader.getTree('results/master_inspection.xml')
		#miLink, miScore, miUrl, miFile = xParser.getInspectionData(miTree)
		#print(miLink, miScore)


def main():
	bl = BLParent()
	bl.startSubProcesses()
	bl.createMasterInspectionXML()
	
	'''
	xReader = XMLReader()
	confTree = xReader.getTree('xml/conf.xml')
	x = XMLParser()
	l = x.getSearchParams(confTree)
	print (l)
	l = x.getSearchSites(confTree)
	print (l)

	t = xReader.getTree('xml/keywords.xml')
	m = x.getKeys(t)
	print(m)
	'''
	'''
	a = Associations()
	a.addKeyword('abc', 1, False)
	a.addKeyword('bcd', 1, False)
	a.addKeyword('cde', 1, False)

	a.popByWord(a.keywordsList,'cdeöö')

	print (a.getIndexByWord(a.keywordsList, 'cde'))
	'''

	'''
	c = ConnectionManager()
	c.initializeConnection(["a"],["b"],["c.com"],["r.argh","lol"],1)
	c.startThread()
	c.join()
	c.parseResults()
	results = c.getResults()
	results = "results/ch1"
	print('derp')

'''

'''
	p = OwnConnection()
	p.setParams("a","a","a","a","a")
	p.initializeConnection()
	p.freeMemory()
	p.startConnection()
	print(p.getMessage())
'''
	

if __name__ == '__main__':
	main()
