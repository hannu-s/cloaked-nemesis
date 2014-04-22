from inspection import Inspection
from list_tool import ListTool

class Sorter():

	def sortInspectionList(self, li):
		if li == None or len(li) == 0:
			li = []
			return li

		lt = ListTool()
		newList = []
		done = False
		while not done:
			currHS = -1000000
			currIN = -1
			done = True
			for ind, obj in enumerate(li):
				if int(obj.score) > currHS:
					currHS = int(obj.score)
					currIN = ind
					done = False

			if not done:
				newList.append(li[currIN])
				li = lt.pop(li, currIN)

		return newList



		