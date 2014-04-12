class ListTool():
	"""docstring for ListTOol"""
	def addOnlyUnique(self, item, li):
		if li == None:
			li = []
		if item in li:
			return li
		return li.append(item)



	def addOnlyUniqueFromList(self, fromList, toList):
		if toList == None or toList == []:
			toList = []
			return self.appendListToList(fromList,toList)
		for i in fromList:
			if i in toList:
				continue
			toList.append(i)
		return toList

	def getNonUniques(self, list1, list2):
		if list2 == None or list2 == []:
			return None
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
		