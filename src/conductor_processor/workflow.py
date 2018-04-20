import random
class WorkflowFile(object):
	def __init__(self, name):
		self._name = "workflow_" + name + "_" + "".join(random.choice(str("0123456789")) for i in range(10))
		self._description = ''
		self._version = 1
		self._schemaVersion = 2
		self._tasks = []
		self._outputParameters = {}

	def generateFromSteps(self, stepObjArr):
		i = 0
		name = ''
		for stepObj in stepObjArr:
			wfTaskObj = WorkflowTaskObject(stepObj, i)
			self._tasks.append(wfTaskObj.getDict())
			name = wfTaskObj.getReferenceName()
			i += 1
		self._outputParameters['output'] = "${" + name + ".output}"

		return self.getDict()

	def getDict(self):
		return {
			"name": self._name,
			"description": self._description,
			"version": self._version,
			"schemaVersion": self._schemaVersion,
			"tasks": self._tasks
		}

class WorkflowTaskObject(object):
	def __init__(self, stepObj, no):	
		self._name = "task_" + stepObj.getName()
		self._taskReferenceName = self._name + "_" + str(no)
		self._type = ''
		if stepObj.getCallFunction() == "REST":
			self._type = 'HTTP'
			self._inputParam = {}

			args = stepObj.getArgs()
			uri = "http://%s:%s/%s" %(str(args['ip']), str(args['port']), str(args['api']))
			method = args['method'] if args['method'] else "GET"
			self._inputParam['http_request'] = {}
			request_data = self._inputParam['http_request']
			request_data['uri'] = uri
			request_data['method'] = method
			if args['req_body'] != None:
				request_data['request_body'] = args['req_body']

	def getDict(self):
		return {
			"name": self._name,
			"taskReferenceName": self._taskReferenceName,
			"inputParameters": self._inputParam,
			"type": self._type
		}

	def getReferenceName(self):
		return self._taskReferenceName