from multiprocessing import Process, Pipe
import time
import httplib2
from bs4 import BeautifulSoup
import re
from list_tool import ListTool

class Child():
	conn = None
	def BLChild(self, conn, keywords, avoids, site, targetUrl, pagesToSearch, searchParams):
		self.conn = conn
		foundLinks = [targetUrl]
		self.conn.send(foundLinks)
		linksToRemove = self.conn.recv()
		
		

		#very end
		self.conn.send("Work succesful")
		self.conn.close()

class Page():
	score = 0
	maxLen = 255
	fileName = None
	def __init__(self, url, link, title = [], header = [], spec = [], norm = []):
		if url[0] == '/' and url[1] == 'r':
			url = 'http://www.reddit.com' + url
		self.url = url
		self.link = link
		self.title = title
		self.header = header
		self.spec = spec
		self.norm = norm

	def followLink(self):
		h = httplib2.Http(".cache")
		(resp, content) = h.request(self.url, "GET",
                            headers={'cache-control':'no-cache'})
		soup = BeautifulSoup(content)
		self.title = soup.title.string

		for h in soup.find_all('h1'):
			self.header.append(str(h.get_text()+" "))
		for h in soup.find_all('h2'):
			self.header.append(str(h.get_text()+" "))
		for h in soup.find_all('h3'):
			self.header.append(str(h.get_text()+" "))

		for b in soup.find_all('b'):
			self.spec.append(str(h.get_text()+" "))

		for b in soup.find_all('i'):
			self.spec.append(str(h.get_text()+" "))

		for b in soup.find_all('p'):
			self.norm.append(str(h.get_text()+" "))

	def parseResults(self):
		lt = ListTool()
		patt = "^[a-zA-Z0-9]*$"
		self.title = self.title.split(' ')
		for ind, item in enumerate(self.title):
			if re.match(patt, item) == None or len(item) > self.maxLen:
				self.title.pop(ind)
		self.title = lt.removeDuplicates(self.title)

		for ind, item in enumerate(self.header):
			if re.match(patt, item) == None or len(item) > self.maxLen:
				self.header.pop(ind)
		self.header = lt.removeDuplicates(self.header)

		for ind, item in enumerate(self.spec):
			if re.match(patt, item) == None or len(item) > self.maxLen:
				self.spec.pop(ind)
		self.spec = lt.removeDuplicates(self.spec)

		for ind, item in enumerate(self.norm):
			if re.match(patt, item) == None or len(item) > self.maxLen:
				self.norm.pop(ind)
		self.norm = lt.removeDuplicates(self.norm)

	def writePageData(self, fileName):
		t = ""
		t = t.join(self.title) + '\n'
		h = ""
		h = h.join(self.header) + '\n'
		s = ""
		s = s.join(self.spec) + '\n'
		n = ""
		n = n.join(self.norm)
		
		f = open(fileName, 'w+')
		f.write(self.url + '\n' + t + h + s + n)
		f.close()

	def getScores(self, keywords, avoids):
		lMulti = 100
		tMulti = 50
		hMulti = 10
		sMulti = 5
		nMulti = 1


p = Page('http://www.reddit.com/r/programming/', 'lolol asd')
p.followLink()
p.parseResults()
p.writePageData('pages/herpderp')
'''
h = httplib2.Http(".cache")
(resp, content) = h.request("http://www.reddit.com/r/programming/", "GET",
                            headers={'cache-control':'no-cache'})
soup = BeautifulSoup(content)
siteTable = soup.find("div", {"id": "siteTable"})
#remove clearleft divs
[s.extract() for s in siteTable('div',{'class':'clearleft'})]


urls = []
links = []
titles = []
headers = []
specials = []
normals = []

print(soup.title.string)
'''
#for div in siteTable.find_all('div', {'class':'entry unvoted'}):
#	print (div.a.get('href'), div.a.get_text(), '\n')