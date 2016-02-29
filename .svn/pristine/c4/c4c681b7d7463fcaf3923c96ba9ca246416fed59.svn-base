# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants


class UberContainerService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def createUberContainer(self, _workflow, _containerCode, _groupCode, _titleCode):
		parameterBlock = {}
		parameterBlock['userProfile'] = _workflow.getUserProfile()
		parameterBlock['userPermissions'] = _workflow.getUserProfile().get('userProfile', {}).get('userPermissions', [])
		parameterBlock['titleCode'] = _titleCode
		parameterBlock['containerDict'] = self.createUberContainerDict(_containerCode, _groupCode)
		parameterBlock['workflow'] = _workflow

		className = constants.kContainerClassUberForm
		importString = "from MPSAppt.core.containers.%s import %s" % (className.lower(), className)
		exec importString

		container = eval(className + "('%s', parameterBlock)" % _containerCode)
		return container

	def createUberContainerDict(self, _containerCode, _groupCode):
		tainer = {
			"code": _containerCode,
			"descr": "Preview",
			"componentType": "Task",
			"affordanceType":"Item",
			"optional": False,
			"enabled": True,
			"logEnabled": False,
			"accessPermissions": ["apptVisitor"],
			"viewPermissions": ["apptVisitor"],
			"freezable": False,
			"className": "UberForm",
			"config": {
				"questionGroupCode": _groupCode,
				"submitEnabled": True,
				"draftEnabled": True,
				"savedSetsEnabled": False,
			},
		}
		return tainer
