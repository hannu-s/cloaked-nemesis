import os, sys
import subprocess

class OSTool():
	"""docstring for OSTool"""
	def __init__(self):
		pass

	def getDirContent(self, dirPath, showGit = False):
		subDirList = []
		fileList = []
		for dirname, dirnames, filenames in os.walk(dirPath):
			# print path to all subdirectories first.
			for subdirname in dirnames:
				subDirList.append(os.path.join(dirname, subdirname))

			# print path to all filenames.
			for filename in filenames:
				fileList.append(os.path.join(dirname, filename))

			if not showGit and '.git' in dirnames:
				# don't go into any .git directories.
				dirnames.remove('.git')
		return subDirList, fileList

	def getAbsolutePath(self, filePath = "."):
		return os.path.abspath(filePath)

	def getFilesInDir(self, dirPath):
		li = []
		for dirname, dirnames, filenames in os.walk(dirPath):
			for filename in filenames:
				li.append(os.path.join(dirname, filename))
		return li

	def deleteFile(self, filePath):
		try:
			os.remove(filePath)
		except Exception as e:
			print(e)
		
	def startProgram(self, program, param = None):
		if param == None:
			subprocess.Popen([program], stdin=None, stdout=None, stderr=None)
		else:
			subprocess.Popen([program, param], stdin=None, stdout=None, stderr=None)

	def callProgram(self, program, param = None):
		if param == None:
			subprocess.call([program])
		else:
			subprocess.call([program, param])


