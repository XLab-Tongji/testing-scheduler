class TestStep(object):
	def __init__(self, type, id, name, service, action, **args):
		self._type = type
		self._id = id
		if name != None and name != '':
			self._name = name
		else:
			self._name = self._type + "_task_" + str(self._id) 
		self._service_name = service['name']
		self._call_type = service['call']
		self._action = action
		self._args = args

	def getId(self):
		return self._id

	def getName(self):
		return self._name

	def getServiceName(self):
		return self._service_name

	def getCallFunction(self):
		return self._call_type

	def getArgs(self):
		return self._args

	def action(self):
		f = getattr(self, self._action)
		f()

	def _argsParse(self):
		pass

	def __str__(self):
		return str(self.__dict__)

if __name__ == "__main__":
	args = {'command': 'start'}
	stepObj = TestStep('test_cpu', 'ansible', 'REST', **args)
	print stepObj