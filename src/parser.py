#!/usr/bin/env python
import click
import os
import yaml
import json
from stepObject.stepobject import StepObject
from conductorFileObject.taskFileObject import TaskFileObject
from conductorFileObject.workflowObject import WorkflowObject
import sys
sys.path.append("..")
from conductorclient.run_new_workflow import WorkflowMgr

serverAddr = "http://192.168.199.130:8080"
storeTaskPath = "tmp/fake_task.json"
storeWorkflowPath = "tmp/fake_workflow.json"

@click.command()
@click.option("--filepath", help="file path of test case")
def parse(filepath):
	filePrefix, fileName = os.path.split(filepath)
	print 'start to parse the test story:', fileName
	with open(filepath) as f:
		yaml_file = yaml.load(f)
		parseStory(yaml_file['schema'], fileName)

	runWorkFlow()

	print 'execute end...'

def parseStory(schema, storyName = 'story0'):
	if schema == None:
		return parseLog(False, reason='schema not found.')
	steps = schema['steps']
	if steps == None:
		return parseLog(False, reason='steps is empty.')
	workflow = ""
	taskArr = []
	stepArr = []

	for step in steps:
		stepObj = StepObject(step['type'], step['service'], step['call'], **step['args']).getObj()
		#print stepObj
		stepArr.append(stepObj)

		taskObj = TaskFileObject("task_xx")
		taskJsonObj = taskObj.generateFromStep(stepObj)
		taskArr.append(taskJsonObj)

	## print json.dumps(taskArr)
	with open(storeTaskPath, "w") as task_file:
		task_file.write(json.dumps({"group1": taskArr}, indent=True))

	workflowObj = WorkflowObject(storyName)
	workflowJsonObj = workflowObj.generateFromSteps(stepArr)
	## print json.dumps(workflowJsonObj, indent=True)
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