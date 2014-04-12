from multiprocessing import Process, Pipe
from child import *

class ProcessManager():
	processes = []

	def __init__(self):
		pass

	def addProcess(self):
		pass


class OwnProcess():
	parent_conn = None
	child_conn = None
	proc = None

	def __init__(self):
		self.parent_conn, self.child_conn = Pipe()
		c = Child()
		self.proc = Process(target=c.BLChild, args=(self.child_conn,))
		self.proc.start()
		print (self.parent_conn.recv())
		self.proc.join()