from collections import OrderedDict

class ListTool():
	"""docstring for ListTOol"""
	def addOnlyUnique(self, item, li):
		if li == None:
			li = []
		if item in li:
			return li
		return li.append(item)



	def addOnlyUniqueFromList(self, fromList, toList):
		if toList == None or len(toList) == 0:
			toList = []
			return self.appendListToList(fromList,toList)
		for i in fromList:
			if i in toList:
				continue
			toList.append(i)
		return toList

	def addOnlyUniqueFrom2DList(self, fromList, toList, index):
		if toList == None or len(toList) == 0:
			toList = []
			return self.appendListToList(fromList,toList)
		for i in fromList:
			if not self.in2DList(toList, index, i[index]):
				toList.append(i)
		return toList

	def in2DList(self, li, index, val):
		for i in li:
			if i[index] == val:
				return True
		return False

	def getNonUniques(self, list1, list2):
		if list2 == None or len(list2) == 0:
			return []
		li = []
		for i in list1:
			if i in list2:
				li.append(i)
		return li

	def appendListToList(self, list1, list2):
		for i in list1:
			list2.append(i)
		return list2

	def descending(self, li):
		pass

	def validateList(self, val):
		if val == None:
			val = []
		return val	

	def getIndexByWord(self, li, word):
		for index, obj in enumerate(li):
			if obj == word:
				return index
		return -1

	def pop(self, li, index):
		if index < 0 or index >= len(li):
			return li
		li.pop(index)
		return li

	def popByWord(self, li, word):
		index = self.getIndexByWord(li, word)
		if not index == -1:
			li.pop(index)
		return li

	def removeDuplicates(self, li):
		li = list(OrderedDict.fromkeys(li))
		return li