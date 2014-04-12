from list_tool import ListTool

class Associations():
	keywordsList = None
	avoidsList = None
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

	def getIndexByWord(self, li, word):
		for index, obj in enumerate(li):
			if obj.word == word:
				return index
		return -1

	def pop(self, li, index):
		if index < 0 or index >= len(li):
			return
		li.pop(index)

	def popByWord(self, li, word):
		index = self.getIndexByWord(li, word)
		if index == -1:
			return
		li.pop(index)

class Keywords():
	word = None
	occurance = None
	isForced = None

	def __init__(self, word, occurance, isForced):
		self.word = word
		self.occurance = occurance
		self.isForced = isForced
