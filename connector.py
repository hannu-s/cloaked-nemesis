from multiprocessing import Process, Pipe
from threading import Thread
from child import *
from list_tool import ListTool

class ConnectionManager():
	connections = []
	thr = None
	results = []

	def initializeConnection(self, keywords, avoids, sites, targetUrls, pagesToSearch, searchParams):
		targets = len(targetUrls)

		for i in range(targets):
			oc = OwnConnection(i)
			oc.setParams(keywords,avoids,sites,targetUrls[i],pagesToSearch, searchParams)
			oc.initializeConnection()
			oc.freeMemory()
			self.connections.append(oc)

	def startThread(self):
		self.thr = OwnThread(self.connections)
		self.thr.deamon = True
		self.thr.start()

	def join(self):
		self.thr.join()

	def parseResults(self):
		for oc in self.connections:
			self.results.append(oc.endResult)
			# TODO
			# if not error
				# self.results.append(oc.endResult)
				
	def getResults(self):
		return self.results

class OwnThread(Thread):
	connections = []
	listTool = None
	responseUrls = []

	def __init__(self, connections):
		Thread.__init__(self)
		self.connections = connections
		self.listTool = ListTool()

	def run(self):
		for c in self.connections:
			c.startConnection()

		self.messengerLinks()
		self.messengerConfirm()

		for c in self.connections:
			c.waitForChild()

	def messengerLinks(self):
		numConns = len(self.connections)
		messages = 0
		while (messages < numConns):
			for c in self.connections:
				if not c.hadMessage:
					c.hasMessage = c.pollMessage(1)

			for ind, c in enumerate(self.connections):
				if c.hasMessage:
					msg = c.getMessage()
					messages += 1
					self.responseUrls = self.listTool.addOnlyUniqueFromList(msg, self.responseUrls)
					c.sendMessage(self.listTool.getNonUniques(msg, self.responseUrls))

	def messengerConfirm(self):
		numConns = len(self.connections)
		messages = 0
		for c in self.connections:
			c.hadMessage = False

		while (messages < numConns):
			for c in self.connections:
				if not c.hadMessage:
					c.hasMessage = c.pollMessage(1)

			for ind, c in enumerate(self.connections):
				if c.hasMessage:
					msg = c.getMessage()
					messages += 1
					c.endResult = msg

	

class OwnConnection():
	parent_conn = None
	child_conn = None
	proc = None
	keywords = None
	avoids = None
	sites = None
	targetUrl = None
	pagesToSearch = None
	isRunning = None
	hasMessage = None
	hadMessage = None
	endResult = None
	searchParams = None
	childID = None

	def __init__(self, cID):
		self.childID = cID
		self.parent_conn, self.child_conn = Pipe()
		self.isRunning = False
		self.hasMessage = False
		self.hadMessage = False

	def setParams(self, keywords, avoids, sites, targetUrl, pagesToSearch, searchParams):
		self.keywords = keywords
		self.avoids = avoids
		self.sites = sites
		self.targetUrl = targetUrl
		self.pagesToSearch = pagesToSearch
		self.searchParams = searchParams

	def initializeConnection(self):
		c = Child()
		self.proc = Process(target=c.BLChild, args=(self.childID, self.child_conn, self.keywords, self.avoids, self.sites, self.targetUrl,self.pagesToSearch, self.searchParams,))

	def startConnection(self):
		self.isRunning = True
		self.proc.start()

	def getMessage(self):
		self.hasMessage = False
		self.hadMessage = True
		return self.parent_conn.recv()

	def pollMessage(self, timeout):
		return self.parent_conn.poll(timeout)

	def sendMessage(self, msg):
		self.parent_conn.send(msg)

	def freeMemory(self):
		self.keywords = None
		self.avoids = None
		self.sites = None
		self.targetUrl = None
		self.pagesToSearch = None
		self.searchParams = None

	def waitForChild(self):
		self.proc.join()
		self.isRunning = False