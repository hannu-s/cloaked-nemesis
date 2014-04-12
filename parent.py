from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml_rw import *

class XMLParser():
	"""docstring for XMLParser"""
	def getSearchParams(self, confT):
		li = []
		for sp in confT.findall('params/search_param'):
			li.append(sp.text)
		return li
	
	def getSearchSites(self, confT):
		li = []
		for si in confT.findall('sites/site'):
			li.append(si.text)
		return li		
		

def main():
	xReader = XMLReader()
	confTree = xReader.getTree('xml/conf.xml')
	x = XMLParser()
	l = x.getSearchParams(confTree)
	print (l)
	l = x.getSearchSites(confTree)
	print (l)

if __name__ == '__main__':
	main()
