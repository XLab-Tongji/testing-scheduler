import random
import json
from task import TaskFile
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

	def generateMetaData(self, flowList, stepObjArr):
		print "in workflowFIle-----------------------------"
		
		flowObj = Flow(flowList, stepObjArr)
		self._tasks, taskMetaList = flowObj.parseMainFlow()

		print "in workflowFIle end end end-----------------------------"
		return self.getDict(), taskMetaList



class Flow(object):
	def __init__(self, flowList, stepObjArr):
		self._mainFlow = {}
		self._subFlowDict = {}
		self._stepObjArr = stepObjArr
		for flow in flowList:
			if flow['name'] == "main":
				self._mainFlow = flow
			else:
				self._subFlowDict[flow['name']] = flow
		#notice: no flow is main exception

	def parseMainFlow(self):
		return self.parseOrderList(self._mainFlow['orders'], self._stepObjArr)

	@staticmethod
	def parse(obj, stepObjArr):
		if isinstance(obj, dict):
			return Flow.parseFlow(obj, stepObjArr)
		else:
			return Flow.parseOrderList(obj, stepObjArr)

	@staticmethod
	def parseFlow(flowDict, stepObjArr):
		orderList = flowDict['orders']
		return Flow.parseOrderList(orderList, stepObjArr)

	@staticmethod
	def parseOrderList(orderList, stepObjArr):
		tasks = []
		taskMetaAllList = []
		for order in orderList:
			if order['type'] == "normal":
				genTask = NormalTask(order, stepObjArr)
			elif order['type'] == "switch":
				genTask = SwitchTask(order, stepObjArr)

			tasks.append(genTask.getDict())
			taskMetaList = genTask.getTaskMetaList()
			if taskMetaList != None:
				taskMetaAllList.extend(taskMetaList)
		return tasks, taskMetaAllList

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

	def getName(self):
		return self._name

	def getTaskMetaList(self):
		taskFile = TaskFile()
		return [taskFile.generateFromStep(self)]

class NormalTask(BaseWorkflowTask):
	def __init__(self, order, stepObjArr):
		relatedStepObj = stepObjArr[order['step'] - 1]
		super(NormalTask, self).__init__(relatedStepObj.getName())
		self._type = "HTTP"
		self._args['inputParameters'] = relatedStepObj.getArgs()

	
class SwitchTask(BaseWorkflowTask):
	def __init__(self, order, stepObjArr):
		super(SwitchTask, self).__init__("switch")
		self._type = "DECISION"
		self._args['caseValueParam'] = order['value']
		self._args['decisionCases'] = {}
		self._childTaskMetaList = []
		for case, caseOrders in order['cases'].items():
			self._args['decisionCases'][case], taskMetaList = Flow.parse(caseOrders, stepObjArr)
			if taskMetaList != None:
				self._childTaskMetaList.extend(taskMetaList)
	def getTaskMetaList(self):
		selfTaskMetaList = super(SwitchTask, self).getTaskMetaList()
		selfTaskMetaList.extend(self._childTaskMetaList)
		return selfTaskMetaList
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