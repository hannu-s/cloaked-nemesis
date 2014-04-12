class Associations():
	keywordsList = None
	avoidsList = None

	def __init__(self):
		self.keywordsList = []
		self.avoidsList = []

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

class Avoids():
	word = None
	occurance = None
	isForced = None

	def __init__(self, word, occurance, isForced):
		self.word = word
		self.occurance = occurance
		self.isForced = isForced
