from multiprocessing import Process, Pipe
import time

class Child():
	conn = None
	def BLChild(self, conn, keywords, avoids, site, targetUrl, pagesToSearch):
		self.conn = conn
		foundLinks = [targetUrl]
		self.conn.send(foundLinks)
		linksToRemove = self.conn.recv()
		
		#very end
		self.conn.send("Work succesful")
		self.conn.close()