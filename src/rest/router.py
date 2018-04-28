from flask import Flask
import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello, World! This is a greet from parser."

@app.route("/test-story/<service_name>")
def getTCDir(service_name):
	baseTestDir = os.path.join(BASE_DIR, "..", "..", "test", "test_story")
	storyDir = os.path.join(baseTestDir, service_name)
	#return "basedir is: %s, dir is:%s"%(os.path.abspath(baseTestDir), storyDir)
	if os.path.exists(storyDir):
		fileList = os.listdir(storyDir)
		data = {"code": "200", "result": {"files": fileList}}
	else:
		data = {"code": "500", "result": "error"}
	
	return json.dumps(data)


if __name__ == "__main__":
	app.debug = True
	app.run()