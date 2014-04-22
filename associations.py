from list_tool import ListTool

class Associations():
	keywordsList = None		# 2D format [val,occ]
	avoidsList = None		# 2D format [val,occ]
	listTool = None

	def __init__(self):
		self.keywordsList = []
		self.avoidsList = []
		self.listTool = ListTool()

	def setParams(self, keywords, avoids, fKeywords, fAvoids):
		self.keywordsList = self.listTool.addOnlyUniqueFromList(keywords, fKeywords)
		self.avoidsList = self.listTool.addOnlyUniqueFromList(avoids, fAvoids)

	def addKeyword(self, word, occurance, isForced):
		self.keywordsList.append(Keywords(word, occurance, isForced))

	def addAvoids(self, word, occurance, isForced):
		self.avoidsList.append(Avoids(word, occurance, isForced))

class Keywords():
	word = None
	occurance = None
	isForced = None

	def __init__(self, word, occurance, isForced):
		self.word = word
		self.occurance = occurance
		self.isForced = isForced
