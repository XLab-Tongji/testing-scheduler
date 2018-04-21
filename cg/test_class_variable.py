class Number:
	num = 0
	def __init__(self):
		Number.num = Number.num + 1

	def getNum(self):
		print Number.num

obj1 = Number()
obj1.getNum()

obj2 = Number()
obj2.getNum()

obj1.getNum()