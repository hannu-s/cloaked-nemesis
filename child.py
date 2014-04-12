from multiprocessing import Process, Pipe
import time

class Child():
	conn = None
	def BLChild(self, conn, keywords, avoids, site, targetUrl, pagesToSearch):
		self.conn = conn
		data = [targetUrl]
		self.conn.send(data)
		self.conn.recv()
		self.conn.close()