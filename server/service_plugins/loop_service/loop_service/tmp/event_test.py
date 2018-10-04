import requests
import json

def _getFinishTaskId():
        taskRefName = 'abc'
        wfid = 'a93395d0-8808-434a-8b18-daf5018ca8bb'
        BASE_URL = "http://10.60.38.181:5201/api"
        headers = {
            "content-type": "application/json"
        }

        wfUrl = BASE_URL + "/workflow/" + wfid

        res = requests.get(wfUrl)
        print "finishId --------------------------"
        print res.json()
        print res.json()['tasks'][1]['taskId']


if __name__ == '__main__':
    _getFinishTaskId()