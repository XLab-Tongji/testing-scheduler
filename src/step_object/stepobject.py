from testservice import TestService
class StepObject(object):
	def __init__(self, type, service, call, **args):
		if type == 'test':
			self._obj = TestService(service, call, **args)
	def getObj(self):
		return self._obj
	def __str__(self):
		return str(self._obj)