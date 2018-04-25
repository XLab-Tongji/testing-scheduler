import random
import json
from task import TaskFile
class WorkflowFile(object):
	def __init__(self, name):
		self._name = "workflow_" + name + "(%s)"%getRandString(10)
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
		flowObj = Flow(flowList, stepObjArr)
		self._tasks, taskMetaList = flowObj.parseMainFlow()

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

	def parse(self, obj, stepObjArr):
		if isinstance(obj, str):
			return self.parseFlow(obj, stepObjArr)
		else:
			return self.parseOrderList(obj, stepObjArr)

	def parseFlow(self, flowName, stepObjArr):
		orderList = self._subFlowDict[flowName]['orders']
		return self.parseOrderList(orderList, stepObjArr)

	def parseOrderList(self, orderList, stepObjArr):
		tasks = []
		taskMetaAllList = []
		for order in orderList:
			if order['type'] == "normal":
				genTask = NormalTask(order, stepObjArr, self)
			elif order['type'] == "switch":
				genTask = SwitchTask(order, stepObjArr, self)
			elif order['type'] == "parallel":
				genTask = ParallelTask(order, stepObjArr, self)
			tasks.append(genTask.getDict())

			if order['type'] == "parallel":
				joinTask = genTask.getJoinTask()
				tasks.append(joinTask.getDict())

			
			taskMetaList = genTask.getTaskMetaList()
			if taskMetaList != None:
				taskMetaAllList.extend(taskMetaList)
		return tasks, taskMetaAllList


class BaseWorkflowTask(object):
	def __init__(self, name):
		self._name = name
		self._taskReferenceName = self._name + "_task_%s"%getRandString(10)
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
	def __init__(self, order, stepObjArr, flowObj):
		relatedStepObj = stepObjArr[order['step'] - 1]
		super(NormalTask, self).__init__(relatedStepObj.getName())
		self._taskReferenceName = "task_%s"%getRandString(10)
		self._type = "HTTP"
		self._args['inputParameters'] = relatedStepObj.getArgs()
		print "NormalTask:----------------------\n", relatedStepObj.getArgs()

	
class SwitchTask(BaseWorkflowTask):
	seqNumber = 0
	def __init__(self, order, stepObjArr, flowObj):
		super(SwitchTask, self).__init__("switch_" + str(SwitchTask.seqNumber))
		SwitchTask.seqNumber = SwitchTask.seqNumber + 1
		self._type = "DECISION"
		caseValueParam = 'value'
		self._args['inputParameters'] = {caseValueParam: order['value']}
		self._args['caseValueParam'] = caseValueParam
		self._args['decisionCases'] = {}
		self._childTaskMetaList = []
		for case, caseOrders in order['cases'].items():
			self._args['decisionCases'][case], taskMetaList = flowObj.parse(caseOrders, stepObjArr)
			if taskMetaList != None:
				self._childTaskMetaList.extend(taskMetaList)
	def getTaskMetaList(self):
		selfTaskMetaList = super(SwitchTask, self).getTaskMetaList()
		selfTaskMetaList.extend(self._childTaskMetaList)
		return selfTaskMetaList

class ParallelTask(BaseWorkflowTask):
	seqNumber = 0
	def __init__(self, order, stepObjArr, flowObj):
		InstSeqNumber = ParallelTask.seqNumber
		super(ParallelTask, self).__init__("parallel_" + str(InstSeqNumber))
		ParallelTask.seqNumber = ParallelTask.seqNumber + 1
		self._type = "FORK_JOIN"
		self._args['forkTasks'] = []
		self._childTaskMetaList = []
		lastTasksNameList = []
		parallelList = order['parallel'].items()
		parallelList.sort()
		for key, orderList in parallelList:
			print orderList
			taskList, taskMetaList = flowObj.parse(orderList, stepObjArr)
			self._args['forkTasks'].append(taskList)
			lastTasksNameList.append(taskList[-1]['taskReferenceName'])
			if taskMetaList != None:
				self._childTaskMetaList.extend(taskMetaList)
		self._joinTaskObj = ParallelJoinTask(InstSeqNumber, lastTasksNameList)

	def getTaskMetaList(self):
		selfTaskMetaList = super(ParallelTask, self).getTaskMetaList()
		selfTaskMetaList.extend(self._childTaskMetaList)
		selfTaskMetaList.extend(self._joinTaskObj.getTaskMetaList())
		return selfTaskMetaList

	def getJoinTask(self):
		return self._joinTaskObj

class ParallelJoinTask(BaseWorkflowTask):
	def __init__(self, seqNumber, joinOnList):
		super(ParallelJoinTask, self).__init__("paralleljoin_" + str(seqNumber))
		self._type = "JOIN"
		self._args['joinOn'] = joinOnList

def getRandString(length):
	return "".join(random.choice(str("0123456789")) for i in range(length))