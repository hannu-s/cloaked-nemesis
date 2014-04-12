from multiprocessing import Process, Pipe
import time

class Child():
	conn = None
	def BLChild(self, conn, keywords, avoids, site, targetUrl, pagesToSearch):
		self.conn = conn
		time.sleep(5)
		self.conn.send('Child sending data')
		self.conn.close()