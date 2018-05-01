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
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from conductorclient.run_new_workflow import WorkflowMgr
BASE_DIR = os.path.dirname(__file__)
CONDUCTOR_SERVER_ADDR = "http://10.60.38.181:5201"
STORE_TASK_PATH = BASE_DIR + "/tmp/fake_task_2.json"
STORE_WF_PATH = BASE_DIR + "/tmp/fake_workflow_2.json"

@click.command()
@click.option("--filepath", help="file path of test case")
def cmdParse(filepath):
	parse(filepath)

def parse(filepath):
	filePrefix, fileName = os.path.split(filepath)
	print '------------ start to parse the test story:%s ------------------'%fileName
	with open(filepath) as f:
		yaml_file = yaml.load(f)
		parseStory(yaml_file['schema'], fileName)

	workflowId = runWorkFlow()

	print '------------------- execute end --------------------------------'

	return workflowId

def parseStory(schema, storyName = 'story0'):
	if schema == None:
		return parseLog(False, reason='schema not found.')
	steps = schema['steps']
	if steps == None:
		return parseLog(False, reason='steps is invalid.')
	flows = schema['flows']
	if flows == None:
		return parseLog(False, reasion='flows is invalid.')
	## steps is a list, step is dict. no json here.
	# steps = sorted(steps, sortById)
	testStepMgr = TestStepManager()
	
	stepObjArr = []
	for step in steps:
		stepObj = testStepMgr.getStepObj(step['type'], step['id'], step['name'], step['service'], step['action'], **step['args'])
		stepObjArr.append(stepObj)

	#generate workflow by 'flow' and 'step'
	storyName = os.path.splitext(storyName)[0]
	wfFileObj = WorkflowFile(storyName)
	workflowDict, taskMetaList = wfFileObj.generateMetaData(flows, stepObjArr)

	with open(STORE_TASK_PATH, 'w') as f:
		f.write(json.dumps({'task_group':taskMetaList}, indent=True))
	with open(STORE_WF_PATH, 'w') as f:
		f.write(json.dumps(workflowDict, indent=True))

def runWorkFlow():
	wfMgr = WorkflowMgr(CONDUCTOR_SERVER_ADDR)
	wfMgr.setTaskDefFromFile(STORE_TASK_PATH)
	wfMgr.setWorkflowFromFile(STORE_WF_PATH)
	inputParam = {'input': 'fake'}
	workflowId = wfMgr.startWorkflow(inputParam)
	return workflowId

def parseLog(flag, **msg):
	return {'result': flag, 'message': msg}

def helloe():
	return "hello"

if __name__ == "__main__":
	cmdParse() 