import json
import os
class TaskFile(object):
	def __init__(self, taskName = 'task_0'):
		self._defaultConfFile = self._getFilePath("defaultTaskFile.json")
		print self._defaultConfFile
		with open(self._defaultConfFile) as defaultConf:
			self._jsonObj = json.load(defaultConf)
		self._jsonObj['name'] = taskName

	def generateFromStep(self, stepObject):
		self._jsonObj['name'] = "task_" + stepObject.getName()
		return self._jsonObj

	def getJsonObj(self):
		return self._jsonObj

	def _getFilePath(self, fileName):
		dirPath = os.path.dirname(os.path.realpath(__file__))
		return os.path.join(dirPath, fileName)