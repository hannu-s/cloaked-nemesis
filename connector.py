from multiprocessing import Process, Pipe
from threading import Thread
from child import *
from list_tool import *

class ConnectionManager():
	connections = []
	thr = None
	def initializeConnection(self, keywords, avoids, sites, targetUrls, pagesToSearch):
		targets = len(targetUrls)
		for i in range(targets):
			oc = OwnConnection()
			oc.setParams(keywords,avoids,sites,targetUrls[i],pagesToSearch)
			oc.initializeConnection()
			oc.freeMemory()
			self.connections.append(oc)

	def startThread(self):
		self.thr = OwnThread(self.connections)
		self.thr.deamon = True
		self.thr.start()

class OwnThread(Thread):
	connections = []
	listTool = None
	responseUrls = []
	def __init__(self, connections):
		Thread.__init__(self)
		self.connections = connections
		self.listTool = ListTool()

	def run(self):
		numConns = len(self.connections)
		messages = 0
		for c in self.connections:
			c.startConnection()

		while (messages < numConns):
			for c in self.connections:
				c.hasMessage = c.pollMessage(1)

			for ind, c in enumerate(self.connections):
				if c.hasMessage:
					msg = c.getMessage()
					print(ind, msg)
					messages += 1
					self.responseUrls = self.listTool.addOnlyUniqueFromList(msg, self.responseUrls)
					c.sendMessage(self.listTool.getNonUniques(msg, self.responseUrls))

		for c in self.connections:
			c.waitForChild()

		print(self.responseUrls)

	


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

	def __init__(self):
		self.parent_conn, self.child_conn = Pipe()
		self.isRunning = False
		self.hasMessage = False

	def setParams(self, keywords, avoids, sites, targetUrl, pagesToSearch,):
		self.keywords = keywords
		self.avoids = avoids
		self.sites = sites
		self.targetUrl = targetUrl
		self.pagesToSearch = pagesToSearch

	def initializeConnection(self):
		c = Child()
		self.proc = Process(target=c.BLChild, args=(self.child_conn, self.keywords, self.avoids, self.sites, self.targetUrl,self.pagesToSearch,))

	def startConnection(self):
		self.isRunning = True
		self.proc.start()

	def getMessage(self):
		self.hasMessage = False
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

	def waitForChild(self):
		self.proc.join()
		self.isRunning = False