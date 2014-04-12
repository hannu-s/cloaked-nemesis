from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml_rw import *
from xml_parser import XMLParser
from associations import Associations
from connector import ConnectionManager
from configure import Configure
from sites import Sites

class BLParent():
	"""docstring for BLParent"""
	__conf = None
	__associations = None
	__sites = None
	def __init__(self):
		self.__conf = Configure()
		self.__associations = Associations()
		self.__sites = Sites()

		xReader = XMLReader()
		xParser = XMLParser()
		confTree = xReader.getTree('xml/conf.xml')
		if confTree == None:
			return
		searchParams = xParser.getSearchParams(confTree)
		searchSites = xParser.getSearchSites(confTree)
		pagesToSearch = xParser.getPagesToSearch(confTree)

		self.__conf.setParams(searchSites, searchParams, pagesToSearch)

		keywordTree = xReader.getTree('xml/keywords.xml')
		fKeywordTree = xReader.getTree('xml/f_keywords.xml')
		if keywordTree == None or fKeywordTree == None:
			return
		keywords = xParser.getKeywords(keywordTree)
		fKeywords = xParser.getKeywords(fKeywordTree)
		avoids = xParser.getAvoids(keywordTree)
		fAvoids = xParser.getAvoids(fKeywordTree)

		self.__associations.setParams(keywords, avoids, fKeywords, fAvoids)

		goodSitesTree = xReader.getTree('xml/good_sites.xml')
		badSitesTree = xReader.getTree('xml/bad_sites.xml')
		goodSites = xParser.getSites(goodSitesTree)
		if goodSitesTree == None or badSitesTree == None:
			return
		badSites = xParser.getSites(badSitesTree)

		self.__sites.setParams(goodSites, badSites)

		print(keywords,searchParams,badSites)


def main():
	bl = BLParent()

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
