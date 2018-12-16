from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask_cors import CORS
import requests
import os
import json
import sys
import time
import datetime
import threading
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, '..'))
from loop_service import LoopService
app = Flask(__name__)
CORS(app)

@app.route('/taskid', methods=['POST'])
def getTaskId():
    requestData = request.data
    wfId = requestData['wfId']
    BASE_URL = "http://conductor_conductor-server_1:8080/api"
    wfUrl = BASE_URL + "/workflow/" + wfId

    res = requests.get(wfUrl)
    print "finishId --------------------------"
    app.logger.debug(res.json())
    app.logger.debug(res.content)
    #taskId = res.json()['tasks'][1]['taskId']
    return res.json()


@app.route('/loop', methods=['POST'])
def loop():
    requestData = request.data
    requestFile = "fake_request.json"
    with open(requestFile, "w") as f:
        f.write(requestData)
    t = threading.Thread(target=startLoop)
    t.start()
    return "start a loop!"

def startLoop():
    requestFile = "fake_request.json"
    with open(requestFile, "r") as f:
        httpBody = json.load(f)
    loopService = LoopService(httpBody)
    loopService.start()

@app.route('/stress', methods=["POST"])
def stress():
    requestData = request.data
    dataDict = json.loads(requestData)
    concurrentNum = dataDict['concurrent_num']
    app.logger.debug("stress- num:%s"%concurrentNum)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("time_log.txt", "a") as time_f:
            time_f.write("%s  STRESS num: %s\n"%(nowTime, concurrentNum))
    with open("stress_counter.txt", "w") as f2:
            f2.write(str(concurrentNum))
    if int(concurrentNum) == 5:
        with open("step_details.txt", "w") as f3:
            f3.write("")
    return jsonify(result="stressed! concurrentNum=" + str(concurrentNum)), 200

@app.route('/reach')
def reach():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("time_log.txt", "a") as time_f:
        time_f.write("%s  REACH \n"%nowTime)
    with open("stress_counter.txt", "r") as f1:
        concurrentNum = float(f1.read())
    if concurrentNum < 20:
        return jsonify(result="false"), 200
    else:
        return jsonify(result="true"), 200

@app.route('/storeData', methods=['POST'])
def storeData():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = request.data
    data = json.loads(data)
    with open("step_details.txt", "a") as step_f:
        stepResult = json.dumps({"time": nowTime, "step_result": data}, indent=True)
        step_f.write(stepResult + ",\n")
    return "storeData."

@app.route('/getData')
def getStoreData():
    with open("step_details.txt", "r") as step_f:
        result = step_f.read()
        result = "[%s]"%result[:-2]
        result = json.loads(result)
    return json.dumps({"result": result})

@app.route('/restart', methods=["POST"])
def restart():
    data = request.data
    dataDict = json.loads(data)
    wfId = dataDict['wfId']
    wfInput = dataDict['wfInput']
    loopChange = dataDict['loopChange']
    app.logger.debug("get wfId:%s"%wfId)
    app.logger.debug("get wfInput:%s"%wfInput)
    app.logger.debug("get loopChange:%s"%loopChange)

    newInput = getNewInput(wfInput, loopChange)
    app.logger.debug("new input:%s"%newInput)

    BASE_URL = "http://conductor_conductor-server_1:8080/api"
    headers = {
        "content-type": "application/json"
    }

    wfUrl = BASE_URL + "/workflow/" + wfId + "/rerun"
    rerunParams = {
        "workflowInput": {
             "change": newInput
        }
    }
    res = requests.post(wfUrl, json.dumps(rerunParams, indent=True), headers=headers)
    app.logger.debug("post res: %s"%res.content)
    return "restart!url: %s,  res:%s"%(wfUrl, res.content)
    return "ok"

@app.route('/loop_finish', methods=['POST'])
def loopFinish():
    data = request.data
    dataDict = json.loads(data)
    wfId = dataDict['wfId']
    #taskId = dataDict['taskId']
    app.logger.debug("taskId: ---------------")
    app.logger.debug(wfId)
    #app.logger.debug(taskId)
    BASE_URL = "http://conductor_conductor-server_1:8080/api"
    wfUrl = BASE_URL + "/workflow/" + wfId

    res = requests.get(wfUrl)
    print "finishId --------------------------"
    print res.json()
    print res.content
    taskId = res.json()['tasks'][1]['taskId']
    app.logger.debug("loop_finish:" + taskId)
    print taskId

    BASE_URL = "http://conductor_conductor-server_1:8080/api"
    headers = {
        "content-type": "application/json"
    }

    wfUrl = BASE_URL + "/tasks/"

    finishParams = {
        "workflowInstanceId": wfId,
        "taskId": taskId,
        "callbackAfterSeconds": 0,
        "status": "COMPLETED",
        "outputData": {
            }
    }

    res = requests.post(wfUrl, json.dumps(finishParams, indent=True), headers=headers)
    return 'ok'


def getNewInput(oldDict, changeDict):
    print "func \n"
    for (k, cv) in changeDict.items():
        print "loop \n"
        if k not in oldDict:
            continue
        ov = oldDict[k]
        print type(ov)
        if isinstance(ov, dict):
            print "dict"
            nv = getNewInput(ov, cv)
        else:
            print "str"
            nv = calculate(str(ov), str(cv))
        oldDict[k] = nv
    return oldDict

def calculate(oldValue, changeValue):
    operation = changeValue[0]
    newValue = oldValue
    if operation == '+':
        newValue = float(oldValue) + float(changeValue[2:])
    elif operation == '-':
        newValue = float(oldValue) - float(changeValue[2:])
    elif operation == '*':
        newValue = float(oldValue) * float(changeValue[2:])
    elif operation == '/':
        newValue = float(oldValue) / float(changeValue[2:])
    return newValue

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5313, debug=True)
