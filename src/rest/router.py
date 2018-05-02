from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import test_parser
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
	return "Hello, World! This is a greet from parser."

@app.route("/story-list/<service_name>")
def getTCDir(service_name):
	baseTestDir = os.path.join(BASE_DIR, "..", "..", "test", "test_story")
	storyDir = os.path.join(baseTestDir, service_name)
	if os.path.exists(storyDir):
		fileList = os.listdir(storyDir)
		data = {"code": "200", "result": {"files": fileList}}
	else:
		data = {"code": "500", "error": "no such stories!"}
	
	return jsonify(data)

@app.route("/run-test/story", methods=['POST'])
def runTestStory():
	time.sleep(5)
	stories = json.loads(request.form['stories'])
	service_name = request.form['service']
	baseTestDir = os.path.join(BASE_DIR, "..", "..", "test", "test_story")
	for story in stories:
		storyDir = os.path.join(baseTestDir, service_name, story)
		app.logger.debug("storyDir:%s"%storyDir)
		workflowId = test_parser.parse(storyDir)
	return jsonify({"code": 200, "result": {"workflowId": workflowId}})


@app.route("/story-content")
def getStoryContent():
	story_name = request.args['story']
	service_name = request.args['service']
	baseTestDir = os.path.join(BASE_DIR, "..", "..", "test", "test_story")
	storyFileDir = os.path.join(baseTestDir, service_name, story_name)
	storyFileDir = os.path.join(BASE_DIR, "..", "tmp", "fake_workflow.json")
	with open(storyFileDir, "r") as f:
		storyContent = f.read()
	result = {"code": 200, "result": {"service": service_name, "story": story_name, "content": storyContent}}
	return jsonify(result)


if __name__ == "__main__":
	app.debug = True
	app.run()