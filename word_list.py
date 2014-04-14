class WordList():
	"""docstring for WordList"""
	def __init__(self):
		self.words = []
		
	def append(self, word, useful, useless):
		if (useful):
			useful = 1
			useless = 0
		if (useless):
			useless = 1
			useful = 0
		hasMatch = False
		for ind,obj in enumerate(self.words):
			if word == obj.word:
				self.words[ind].occ += 1
				self.words[ind].usef += useful
				self.words[ind].usel += useless
				hasMatch = True
		if hasMatch:
			return
		self.words.append(Word(word, 1, useful, useless))

	def set(self, word, occ, useful, useless):
		self.words.append(Word(word, occ, useful, useless))

class Word(object):
	def __init__(self, word, occ, usef, usel):
		self.word = word
		self.occ = occ
		self.usef = usef
		self.usel = usel
		