class TestService(object):
	def __init__(self, service, call, **args):
		self._service = service
		self._call = call
		self._args = args

	def __str__(self):
		return 'service:%s'%self._service

	def getName(self):
		return self._service

	def getCallFunction(self):
		return self._call

	def getArgs(self):
		return self._args
	#def run(self):