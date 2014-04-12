from multiprocessing import Process, Pipe

class Child():
	conn = None
	def BLChild(self, conn):
		self.conn = conn
		self.conn.send('Child sending data')
		self.conn.close()