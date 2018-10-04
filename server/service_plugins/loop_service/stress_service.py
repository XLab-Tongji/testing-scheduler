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
app = Flask(__name__)
CORS(app)

@app.route('/stress')
def stress():
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("time_log.txt", "a") as time_f:
                time_f.write("%s  STRESS \n"%nowTime)
        with open("stress_counter.txt", "r") as f1:
                counter = int(f1.read())
        counter = counter + 1
        with open("stress_counter.txt", "w") as f2:
                f2.write(str(counter))
        return jsonify(result="stressed! counter=" + str(counter)), 200

@app.route('/reach')
def reach():
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("time_log.txt", "a") as time_f:
                time_f.write("%s  REACH \n"%nowTime)
        with open("stress_counter.txt", "r") as f1:
                counter = int(f1.read())
        if counter < 10:
                return jsonify(result="false"), 200
        else:
                return jsonify(result="true"), 200
@app.route('/restart', methods=["POST"])
def restart():
        data = request.data
        dataDict = json.loads(data)
        wfId = dataDict['wfId']
        app.logger.debug("get wfId:%s"%wfId)

        BASE_URL = "http://10.60.38.181:5201/api"
        headers = {
                "content-type": "application/json"
        }

        wfUrl = BASE_URL + "/workflow/" + wfId + "/rerun"
        res = requests.post(wfUrl, json.dumps({}, indent=True), headers=headers)
        app.logger.debug("post res: %s"%res.content)
        return "restart!url: %s,  res:%s"%(wfUrl, res.content)
if __name__ == "__main__":
        app.run(host="0.0.0.0", port=6000, debug=True)