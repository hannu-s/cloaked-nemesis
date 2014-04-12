from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml_rw import *
from xml_parser import XMLParser
from associations import Associations
	
class BLParent():
	"""docstring for BLParent"""
	__conf = None
	__keywords = None
	__avoids = None
	__sites = None
	def __init__(self, arg):
		self.arg = arg


def main():
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

if __name__ == '__main__':
	main()
