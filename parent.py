from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml_rw import *
from xml_parser import XMLParser
from associations import Associations
from connector import ConnectionManager
	
class BLParent():
	"""docstring for BLParent"""
	__conf = None
	__associations = None
	__sites = None
	def __init__(self, arg):
		self.arg = arg


def main():
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
	c = ConnectionManager()
	c.initializeConnection(["a"],["b"],["c.com"],["r.argh","lol"],1)
	c.startThread()
	c.join()
	c.parseResults()
	results = c.getResults()
	results = "results/ch1"
	print('derp')

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
