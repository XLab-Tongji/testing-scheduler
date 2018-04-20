import yaml
import json
DIR = "../test/test_story/logic/ts_logic_01.yaml"
TEMP_FILE = "temp"
print "START"

jsonObj = "not written"
with open(DIR, 'r') as f:
	jsonObj = yaml.load(f.read())
	print jsonObj

with open(TEMP_FILE, 'w') as tf:
	tf.write(json.dumps(jsonObj, indent=True))

print "END"