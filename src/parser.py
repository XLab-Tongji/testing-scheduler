#!/usr/bin/env python
import click
import os
import yaml
import json
from step.test_step import TestStep
from step.step_manager import TestStepManager
from conductor_processor.task import TaskFile
from conductor_processor.workflow import WorkflowFile
import sys
sys.path.append("..")
from conductorclient.run_new_workflow import WorkflowMgr

serverAddr = "http://192.168.199.131:8080"
storeTaskPath = "tmp/fake_task.json"
storeWorkflowPath = "tmp/fake_workflow.json"

SERVER_ADDR = "http://192.168.199.131:8080"
STORE_TASK_PATH = "tmp/fake_task_2.json"
STORE_WF_PATH = "tmp/fake_workflow_2.json"

@click.command()
@click.option("--filepath", help="file path of test case")
def parse(filepath):
	filePrefix, fileName = os.path.split(filepath)
	print '------------ start to parse the test story:%s ------------------'%fileName
	with open(filepath) as f:
		yaml_file = yaml.load(f)
		#print yaml_file
		parseStory(yaml_file['schema'], fileName)

	#runWorkFlow()

	print '------------------- execute end --------------------------------'

def parseStory(schema, storyName = 'story0'):
	if schema == None:
		return parseLog(False, reason='schema not found.')
	steps = schema['steps']
	if steps == None:
		return parseLog(False, reason='steps is invalid.')
	flows = schema['flows']
	if flows == None:
		return parseLog(False, reasion='flows is invalid.')
	#print steps
	#print type(steps)
	## steps is a list, step is dict. no json here.
	# steps = sorted(steps, sortById)
	testStepMgr = TestStepManager()
	
	stepObjArr = []
	taskDictArr = []
	for step in steps:
		stepName = step['type'] + "_task_" + str(step['id'])
		stepObj = testStepMgr.getStepObj(step['type'], step['id'], stepName, step['service'], step['action'], **step['params'])
		stepObjArr.append(stepObj)

		taskFileObj = TaskFile()
		taskDict = taskFileObj.generateFromStep(stepObj)
		taskDictArr.append(taskDict)

	with open(STORE_TASK_PATH, 'w') as f:
		f.write(json.dumps({'task_group':taskDictArr}, indent=True))
	# for step in stepObjArr:
	# 	print step
	# for taskObj in taskObjArr:
	# 	print taskObj


	#generate workflow by 'flow' and 'step'
	
	wfFileObj = WorkflowFile(storyName)
	wfJson = wfFileObj.generateJson(flows, stepObjArr)
	print wfJson


# def sortById(dictX, dictY):
# 	if dictX['id'] > dictY['id']:
# 		return 1
# 	elif dictX['id'] < dictY['id']:
# 		return -1
# 	else:
# 		return 0

def parseStory_bak(schema, storyName = 'story0'):
	if schema == None:
		return parseLog(False, reason='schema not found.')
	steps = schema['steps']
	if steps == None:
		return parseLog(False, reason='steps is empty.')

	taskArr = []
	stepArr = []

	for step in steps:
		stepObj = stepMgr.getStepObj(step['type'], step['name'], step['service'], step['call'], **step['args'])
		stepArr.append(stepObj)
		print "generate a %s step object:%s"%(step['type'], stepObj)
		taskObj = TaskFile()
		taskJsonObj = taskObj.generateFromStep(stepObj)
		taskArr.append(taskJsonObj)
		print "generate the task file by the step."

	with open(storeTaskPath, "w") as task_file:
		task_file.write(json.dumps({"group1": taskArr}, indent=True))

	workflowObj = WorkflowFile(storyName)
	workflowJsonObj = workflowObj.generateFromSteps(stepArr)
	print "generate the workflow file by the steps."
	with open(storeWorkflowPath, "w") as workflow_file:
		workflow_file.write(json.dumps(workflowJsonObj, indent=True))

def runWorkFlow():
	wfMgr = WorkflowMgr(serverAddr)
	wfMgr.setTaskDefFromFile(storeTaskPath)
	wfMgr.setWorkflowFromFile(storeWorkflowPath)
	inputParam = {'input': 'fake'}
	wfMgr.startWorkflow(inputParam)

def parseLog(flag, **msg):
	return {'result': flag, 'message': msg}


if __name__ == "__main__":
	parse() 