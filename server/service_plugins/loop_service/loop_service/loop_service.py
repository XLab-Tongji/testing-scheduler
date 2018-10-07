import requests
import json
from copy import deepcopy
import random
import os
BASE_DIR = os.path.dirname(__file__)
TEMP_FILES = {
	"workflow": 				"template_workflow.json",
	"task_def": 				"template_task.json",
	"wf_http_task": 			"template_wf_http_task.json",
	"wf_decision_task": 		"template_wf_decision_task.json",
	"wf_event_task": 			"template_wf_event_task.json",
	"event_handler": 			"template_event_handler.json",
	"event_handler_actions": 	"template_event_handler_actions.json"
}
SERVER_ADDR = "http://t-scheduler-server:5313"


class LoopService(object):
	def __init__(self, args):
		self._clientArgs = args
		print args
		self._parseClientArgs()

		self._workflowName = ""
		self._workflowDef = {}
		self._tasksDef = []
		self._template = {}
		self._loadTemplates()

	def _parseClientArgs(self):
		self._clientWorkflowId = self._clientArgs['workflowId']
		self._clientTaskRefName = self._clientArgs['taskRefName']
		self._clientFinishTaskRefName = self._clientArgs['finishTaskRefName']
		self._loopTasks = self._clientArgs['loopTasks']
		self._loopCheckTask = self._clientArgs['loopCheckTask']
		self._loopChanges = self._clientArgs['loopChange']
		self._wfInput = {}

	def _loadTemplates(self):
		for (fileKey, fileDir) in TEMP_FILES.items():
			with open(os.path.join(BASE_DIR, fileDir)) as f:
				self._template[fileKey] = json.load(f)

	def _createLoopWorkflow(self):
		self._workflowName = "%s_%s_loop_%s"%(self._clientWorkflowId, self._clientTaskRefName, self._getRandomString("", 2))
		self._workflowName = "loop_%s"%(self._getRandomString("", 3))
		print "createLoopWorkflow:", self._workflowName
		self._workflowDef = deepcopy(self._template['workflow'])
		self._workflowDef['name'] = self._workflowName
		self._workflowDef['description'] = "loop function workflow"
		self._setLoopTasks()
		self._setLoopChecker()

	def _setLoopTasks(self):
		for loopTask in self._loopTasks:
			self._addNewTaskDef(loopTask['name'])
		self._workflowDef['tasks'] = self._loopTasks

		for  task in self._workflowDef['tasks']:
			taskRefName = task['taskReferenceName']
			if taskRefName not in self._loopChanges.keys():
				continue
			print "----------------------task"
			print task
			print "\n\n"
			httpBody = task['inputParameters']['http_request']['body']
			taskChangeParams = self._loopChanges[taskRefName]
			for taskParam in httpBody.keys():
				if taskParam in taskChangeParams.keys():
					initValue = httpBody[taskParam]
					if taskRefName not in self._wfInput:
						self._wfInput[taskRefName] = {}
					self._wfInput[taskRefName][taskParam] = initValue
					print self._wfInput
					httpBody[taskParam] = "${workflow.input.change.%s.%s}"%(taskRefName, taskParam)

	def _setLoopChecker(self):
		self._addNewTaskDef(self._loopCheckTask['name'])
		taskList = self._workflowDef['tasks']
		taskList.append(self._loopCheckTask)
		#append storeData task
		storeDataTask = self._getStoreTask()
		taskList.append(storeDataTask)

		#append decision after check
		decisionTaskDefName = "loop_decision"
		self._addNewTaskDef(decisionTaskDefName)
		decisionTask = deepcopy(self._template['wf_decision_task'])
		decisionTask['name'] = decisionTaskDefName
		decisionTask['taskReferenceName'] = decisionTaskDefName
		decisionTask['inputParameters']['decisionVal'] = "${%s.output.response.body.result}"%self._loopCheckTask['taskReferenceName']

		getDataTask = self._getReturnDataTask()

		#decisionTask['decisionCases']['true'] = [getDataTask, self._getEventTask("loop_end")]
		decisionTask['decisionCases']['true'] = [getDataTask, self._getFinishTask()]
		decisionTask['decisionCases']['false'] = [self._getRecallTask()]
		taskList.append(decisionTask)

        def _getFinishTask(self):
                taskName = "finish_return_wf"
                self._addNewTaskDef(taskName)
		# taskId = self._getFinishTaskId()
                recallTask = deepcopy(self._template['wf_http_task'])
                recallTask['name'] = taskName
                recallTask['taskReferenceName'] = taskName
                httpRequest = recallTask['inputParameters']['http_request']
                httpRequest['uri'] = SERVER_ADDR + "/loop_finish"
                httpRequest['method'] = "POST"
                httpRequest['body'] = {
                        "wfId" : self._clientWorkflowId
                }

                return recallTask

        def _getFinishTaskId(self):
                taskRefName = self._clientFinishTaskRefName

                BASE_URL = "http://conductor_conductor-server_1:8080/api"
                headers = {
                    "content-type": "application/json"
                }

                wfUrl = BASE_URL + "/workflow/" + self._clientWorkflowId

                res = requests.get(wfUrl)
                print "finishId --------------------------  " + wfUrl
                print res
                print res.content
                print "res.content"
                print res.json()
                print res.json()['tasks']
                #return wfUrl
                return res.json()['tasks'][1]['taskId']

	def _getRecallTask(self):
		taskName = "restart_wf"
		self._addNewTaskDef(taskName)
		recallTask = deepcopy(self._template['wf_http_task'])
		recallTask['name'] = taskName
		recallTask['taskReferenceName'] = taskName
		httpRequest = recallTask['inputParameters']['http_request']
		httpRequest['uri'] = SERVER_ADDR + "/restart"
		httpRequest['method'] = "POST"
		httpRequest['body'] = {
			"wfId" : "${workflow.workflowId}",
			"wfInput": "${workflow.input.change}",
			"loopChange": self._loopChanges
		}

		return recallTask

	def _getEventTask(self, taskName):
		self._addNewTaskDef(taskName)

		eventTask = deepcopy(self._template['wf_event_task'])
		eventTask['name'] = taskName
		eventTask['taskReferenceName'] = eventTask['name']
		return eventTask

	def _registerEventHandlers(self):
		restartEvent = "loop_next"
		restartHandler = self._getRestartHandler(restartEvent)
		loopEndEvent = "loop_end"
		endHandler = self._getLoopEndHandler(loopEndEvent)

		return restartHandler, endHandler
		### register handlers into conductor server

	def _getRestartHandler(self, eventName):
		anotherWFName = "workflow_tc_logic_00(4415897769)"
		rHandler = deepcopy(self._template['event_handler'])
		rHandler['name'] = "restart" + self._getRandomString("_", 3)
		print "getRestartHandler:", self._workflowName
		rHandler['event'] = "conductor:%s:%s"%(self._workflowName, eventName)
		startWFAction = self._template['event_handler_actions']['start_workflow']
		startWFAction['start_workflow']['name'] = self._workflowName
		startWFAction['start_workflow']['name'] = anotherWFName
		rHandler['actions'].append(startWFAction)
		return rHandler

	def _getLoopEndHandler(self, eventName):
		endHandler = deepcopy(self._template['event_handler'])
		endHandler['name'] = "loop_finish" + self._getRandomString("_", 3)
		endHandler['event'] = "conductor:%s:%s"%(self._workflowName, eventName)
		completeTaskAction = self._template['event_handler_actions']['complete_task']
		completeTaskAction['complete_task']['workflowId'] = self._clientWorkflowId
		completeTaskAction['complete_task']['taskRefName'] = self._clientFinishTaskRefName
		endHandler['actions'].append(completeTaskAction)
		return endHandler


	def _addNewTaskDef(self, taskName):
		taskDef = deepcopy(self._template['task_def'])
		taskDef['name'] = taskName
		self._tasksDef.append(taskDef)

	def _getStoreTask(self):
		taskDefName = "store_task"
		self._addNewTaskDef(taskDefName)

		storeWFTask = deepcopy(self._template['wf_http_task'])
		storeWFTask['name'] = taskDefName
		storeWFTask['taskReferenceName'] = "store_loop_data"
		request = storeWFTask['inputParameters']['http_request']
		request['uri'] = "%s/%s"%(SERVER_ADDR, "storeData")
		request['method'] = "POST"
		request['body'] = {}
		request['body']['task_output'] = {}
		taskOutput = request['body']['task_output']
		for loopTask in self._loopTasks:
			taskOutput[loopTask['name']] = "${%s.output.response.body}"%loopTask['taskReferenceName']
		return storeWFTask

	def _getReturnDataTask(self):
		taskDefName = "return_data_task"
		self._addNewTaskDef(taskDefName)

		returnWFTask = deepcopy(self._template['wf_http_task'])
		returnWFTask['name'] = taskDefName
		returnWFTask['taskReferenceName'] = "get_loop_data"
		request = returnWFTask['inputParameters']['http_request']
		request['uri'] = "%s/%s"%(SERVER_ADDR, "getData")
		request['method'] = "GET"

		self._workflowDef['outputParameters'] = {
			taskDefName: "${%s.output.response.body}"%"get_loop_data"
		}
		return returnWFTask

	def _createTaskDef(self):
		pass

	def start(self):
		self._createLoopWorkflow()
		with open(os.path.join(BASE_DIR, "tmp/fake_workflow.json"), "w") as f:
			f.write(json.dumps(self._workflowDef, indent=True))
		with open(os.path.join(BASE_DIR, "tmp/fake_tasks.json"), "w") as f:
			f.write(json.dumps(self._tasksDef, indent=True))
		h1, h2 = self._registerEventHandlers()
		with open(os.path.join(BASE_DIR, "tmp/fake_handler.json"), "w") as f:
			f.write(json.dumps({"h1": h1, "h2": h2}, indent=True))

		###
		BASE_URL = "http://conductor_conductor-server_1:8080/api"
		headers = {
			"content-type": "application/json"
		}
		taskDefUrl = BASE_URL + "/metadata/taskdefs"
		res = requests.post(taskDefUrl, json.dumps(self._tasksDef, indent=True), headers=headers)

		workflowDefUrl = BASE_URL + "/metadata/workflow"
		res = requests.post(workflowDefUrl, json.dumps(self._workflowDef, indent=True), headers=headers)

		handlerUrl = BASE_URL + "/event/"
		requests.post(handlerUrl, json.dumps(h1, indent=True), headers=headers)

		startWorkflowUrl = BASE_URL + "/workflow/" + self._workflowName
		workflowInput = {
			"change": self._wfInput
		}
		res = requests.post(startWorkflowUrl, json.dumps(workflowInput, indent=True), headers=headers)
		print res

	def loop(self):
		pass

	def _getRandomString(self, prefix, length):
		return prefix + "".join([random.choice(str("0123456789")) for i in range(length)])
if __name__ == "__main__":
	requestFile = "fake_body_args.json"
	with open(requestFile, "r") as f:
		httpBody = json.load(f)
	loopService = LoopService(httpBody)
	loopService.start()
	#print loopService._wfInput
