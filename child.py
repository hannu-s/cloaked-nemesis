from multiprocessing import Process, Pipe
import time

class Child():
	conn = None
	def BLChild(self, conn, keywords, avoids, site, targetUrl, pagesToSearch):
		self.conn = conn
		if targetUrl == "kebaab":
			time.sleep(4)
		self.conn.send(targetUrl)
		self.conn.close()