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
					requestBody['testcase'] = tcBaseDir + requestBody['testcase']
