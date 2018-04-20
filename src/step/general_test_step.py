from step.test_step import TestStep

class GeneralTestStep(TestStep):
	__step_type__ = "test"

	def __init__(self, id, name, service, action, **args):
		super(GeneralTestStep, self).__init__(self.__step_type__, id, name, service, action, **args)
