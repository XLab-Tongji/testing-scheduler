from step.test_step import TestStep
import os
import yaml
class GeneralTestStep(TestStep):
	__step_type__ = "test"

	def __init__(self, id, name, service, action, **args):
		super(GeneralTestStep, self).__init__(self.__step_type__, id, name, service, action, **args)
		self._argsParse()
		self.action()

	def _argsParse(self):
		self._serviceParse()

	def _serviceParse(self):
		if self._callType == "REST":
			httpRequestParam = {}
			envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
			with open(envFilePath, 'r') as f:
				conf = yaml.load(f)
				conf = conf[self._serviceName]
				httpRequestParam['uri'] = "http://%s:%s/"%(conf['ip'], conf['port'])
			httpRequestParam['method'] = self._args['method']
			self._args.pop('method')
			httpRequestParam['body'] = self._args
			self._args = {}
			self._args['http_request'] = httpRequestParam



	def run_testcase(self):
		### fimd_service_conf, set proper command in data to transfer
		if self._callType == "REST":
			if "http_request" in self._args:
				requestParam = self._args['http_request']
				envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
				with open(envFilePath, 'r') as f:
					conf = yaml.load(f)
					conf = conf[self._serviceName]
					apiPath = conf['apis'][self._action]
					requestParam['uri'] = requestParam['uri'] + apiPath
					tcBaseDir = conf['testcase_base_dir']
					requestBody = requestParam['body']

					requestBody['action'] = "run_test_case"
					requestBody['args']['testcase'] = tcBaseDir + requestBody['args']['testcase']

				if requestParam['method'] == "GET":
					requestParam.pop('body')



	## this function is for testing, can be removed latter.
	def start(self):
		if self._callType == "REST":
			if "http_request" in self._args:
				requestParam = self._args['http_request']
				envFilePath = os.path.join(self._getCurrentDir(), "..", "env", self._serviceName + ".yaml")
				with open(envFilePath, 'r') as f:
					conf = yaml.load(f)
					conf = conf[self._serviceName]
				requestBody = requestParam['body']
				command = requestBody['command']
				requestBody.pop('command')
				apiPath = conf['apis'][command]['realname']
				requestParam['uri'] = requestParam['uri'] + apiPath
				
				if "args" in requestBody:
					requestBody = requestBody['args']
					requestParam['body'] = requestBody
				
				if "format" not in conf['apis'][command]:
					if "args" not in requestBody:
						requestParam.pop("body")
					return

				requestBodyFormat = conf['apis'][command]['format']

				print "requestBody"
				print requestBody
				for k,v in requestBodyFormat.items():
					print k, v
					print k in requestBody
					if k in requestBody and isinstance(requestBody[k], eval(v)):
						print "param %s:%s is ok--------------"%(k, requestBody[k])
					else:
						requestBody[k] = "default"

				if requestParam['method'] == "GET":
					requestParam.pop('body')
				## should contain the logic of request_body data
				## should contain the logic of request_body data
				## should contain the logic of request_body data