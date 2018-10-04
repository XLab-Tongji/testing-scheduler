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
sys.path.append("..")
from loop_service import LoopService
app = Flask(__name__)
CORS(app)

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
    return json.dumps("{result:%s}"%result)

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

    BASE_URL = "http://10.60.38.181:5201/api"
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
    app.run(host="0.0.0.0", port=6000, debug=True)