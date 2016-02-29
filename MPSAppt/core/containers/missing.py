# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task

#   Missing is a special container used only in Workflow Admin.
#   It represents a container that does not exist in the workflow,
#   but is referenced in the workflow.

class Missing(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)

	def getDescr(self): return 'Missing'
	def getClassName(self): return 'Missing'
	def getIsMissing(self): return True
