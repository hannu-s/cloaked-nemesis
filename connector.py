from multiprocessing import Process, Pipe
from child import *

class ConnectionManager():
	Connections = []

	def __init__(self):
		pass

	def addConnection(self):
		Connections.append(OwnConnection())

	


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

	def __init__(self):
		self.parent_conn, self.child_conn = Pipe()
		self.isRunning = False

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
		return self.parent_conn.recv()

	def freeMemory(self):
		self.keywords = None
		self.avoids = None
		self.sites = None
		self.targetUrl = None
		self.pagesToSearch = None

	def waitForChild(self):
		self.proc.join()
		self.isRunning = False