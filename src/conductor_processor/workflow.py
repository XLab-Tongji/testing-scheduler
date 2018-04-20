import random
import json
class WorkflowFile(object):
	def __init__(self, name):
		self._name = "workflow_" + name + "_" + "".join(random.choice(str("0123456789")) for i in range(10))
		self._description = ''
		self._version = 1
		self._schemaVersion = 2
		self._tasks = []
		self._outputParameters = {}

	def getDict(self):
		return {
			"name": self._name,
			"description": self._description,
			"version": self._version,
			"schemaVersion": self._schemaVersion,
			"tasks": self._tasks,
			"outputParameters": self._outputParameters
		}

	def generateWFJson(self, flowList, stepObjArr):
		mainFlow = {}
		for flow in flowList:
			if flow['name'] == "main":
				mainFlow = flow
				break
		#notice: no flow is main exception
		mainFlowOrders = mainFlow['orders']
		for order in mainFlowOrders:
			if order['type'] == "normal":
				relateStepObj = stepObjArr[order['step'] - 1]
				genTask = NormalTask(relateStepObj)
			else:
				genTask = SwitchTask(order)
			self._tasks.append(genTask.getDict())

		return json.dumps(self.getDict(), indent=True)
		
class BaseWorkflowTask(object):
	def __init__(self, name):
		self._name = name
		self._taskReferenceName = self._name + getRandString(10)
		self._type = ''
		self._args = {}

	def __str__(self):
		dictObj = self.getDict()
		return str(dictObj)

	def getDict(self):
		d1 = {
			"name": self._name,
			"taskReferenceName": self._taskReferenceName,
			"type": self._type
		}

		return dict(d1, **self._args)



class NormalTask(BaseWorkflowTask):
	def __init__(self, stepObj):
		super(NormalTask, self).__init__(stepObj.getName())
		self._type = "HTTP"
		self._args['inputParameters'] = stepObj.getArgs()

class SwitchTask(BaseWorkflowTask):
	def __init__(self, switchDict):
		super(SwitchTask, self).__init__("switch")
		self._type = "DECISION"
		self._caseValueParam = switchDict['value']
		self._decisionCases = {}
		for k,v in switchDict['cases'].items():
			#recursive
			pass


	def getDict(self):
		pass

class ParallelTask(BaseWorkflowTask):
	def __init__(self, stepObj):
		super(ParallelTask, self).__init__(stepObj)
		self._type = "FORK"







class WorkflowTaskObjectBak(object):
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

def getRandString(length):
	return "".join(random.choice(str("0123456789")) for i in range(length))