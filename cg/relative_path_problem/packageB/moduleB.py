
def writeHello(message):
	with open("./hello.txt", "a") as f:
		f.write(message + "\n")

class ModuleBWrite(object):
	def __init__(self):
		pass
	def writeHello(self, message):
		with open("./hello.txt", "a") as f:
			f.write(message + "\n")

if __name__ == "__main__":
	writeHello("moduleB write")