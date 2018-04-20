import os
import sys
from step.test_step import TestStep
class TestStepManager(object):
	def __init__(self):
		currentDirPath = os.path.dirname(os.path.abspath(__file__))
		sys.path.append(currentDirPath)

		excludeFiles = ('__init__.py', 'step_manager.py', 'test_step.py')
		for fileName in os.listdir(currentDirPath):
			if os.path.isfile(os.path.join(currentDirPath, fileName)) and \
			os.path.splitext(fileName)[1] == '.py' and \
			fileName not in excludeFiles:
			   	__import__(os.path.splitext(fileName)[0])

	def getStepObj(self, type, id, name, service, action, **args):
		for subclass in TestStep.__subclasses__():
			#print "__step_type__:%s"%subclass.__step_type__
			if type == subclass.__step_type__:
				return subclass(id, name, service, action, **args)

if __name__ == "__main__":
	tsMgr = TestStepManager()
	args = {'command': 'start', 'method': 'POST', 'target': {'ip': '192.168.199.130',
          'port': '8080'}, 'domain': 'make_a_phonecall', 'amount': '100', 'duration': '60'}
	stepObj = tsMgr.getStepObj('workload', 'test_cpu', 'ansible', 'REST', **args)
	print stepObj
	print stepObj.__class__.__mro__