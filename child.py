from multiprocessing import Process, Pipe
import time
import httplib2
from bs4 import BeautifulSoup
import re
from list_tool import ListTool
from inspection import Inspection

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

	def readReddit(self):
		h = httplib2.Http(".cache")
		(resp, content) = h.request(self.targetUrl, "GET",
		                            headers={'cache-control':'no-cache'})
		soup = BeautifulSoup(content)
		siteTable = soup.find("div", {"id": "siteTable"})
		#remove clearleft divs
		[s.extract() for s in siteTable('div',{'class':'clearleft'})]

		insp = []
		pages = []
		urls = []
		links = []

		for div in siteTable.find_all('div', {'class':'entry unvoted'}):
			urls.append(div.a.get('href'))
			links.append(div.a.get_text())

		for ind, url in enumerate(urls):
			p = Page(url, links[ind])
			p.followLink()
			p.parseResults()
			if not p.writePageData('pages/asd.txt'):
				print('Error occured while writing page data!')
				return
			p.getScore()
			p.releaseMemory()
			pages.append(p)
			insp.append(Inspection(links[ind], p.score, url, p.fileName))



class Page():
	score = 0
	maxLen = 255
	fileName = None
	lMulti = 100
	tMulti = 50
	hMulti = 10
	sMulti = 5
	nMulti = 1

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
		self.link = self.link.split(' ')
		self.title = self.title.split(' ')
		for ind, item in enumerate(self.link):
			if re.match(patt, item) == None or len(item) > self.maxLen:
				self.link.pop(ind)
		self.link = lt.removeDuplicates(self.link)

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
		self.fileName = fileName
		t = ""
		t = t.join(self.title) + '\n'
		h = ""
		h = h.join(self.header) + '\n'
		s = ""
		s = s.join(self.spec) + '\n'
		n = ""
		n = n.join(self.norm)
		try:
			f = open(fileName, 'w+')
			f.write(self.url + '\n' + t + h + s + n)
		except Exception as e:
			print(e)
			return False
		try:
			f.close()
		except:
			return False
		return True

	def getScore(self, keyWords, avoids):
		lt = ListTool()
		lWords = lt.getNonUniques(keyWords, self.link)
		tWords = lt.getNonUniques(keyWords, self.title)
		hWords = lt.getNonUniques(keyWords, self.header)
		sWords = lt.getNonUniques(keyWords, self.spec)
		nWords = lt.getNonUniques(keyWords, self.norm)

		score = len(lWords) * self.lMulti
		score += len(tWords) * self.tMulti
		score += len(hWords) * self.hMulti
		score += len(sWords) * self.sMulti
		score += len(nWords) * self.nMulti

		lWords = lt.getNonUniques(avoids, self.link)
		tWords = lt.getNonUniques(avoids, self.title)
		hWords = lt.getNonUniques(avoids, self.header)
		sWords = lt.getNonUniques(avoids, self.spec)
		nWords = lt.getNonUniques(avoids, self.norm)

		score -= len(lWords) * self.lMulti
		score -= len(tWords) * self.tMulti
		score -= len(hWords) * self.hMulti
		score -= len(sWords) * self.sMulti
		score -= len(nWords) * self.nMulti

		self.score = score

	def releaseMemory(self):
		self.title = None
		self.header = None
		self.spec = None
		self.norm = None
'''
p = Page('http://www.reddit.com/r/programming/', 'lolol asd kebab')
p.followLink()
p.parseResults()
p.writePageData('pages/herpderp')
p.getScore(['asd', 'kebab'],['derp'])
p.releaseMemory()
print(p.score)
'''
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