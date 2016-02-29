# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.workflowComponentSQL as wfComponentSQL

class WorkflowComponentService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	#   Components

	def createComponent(self, _componentDict, doCommit=True):
		wfComponentSQL.createComponent(self.connection, _componentDict, doCommit=doCommit)

	def updateComponent(self, _componentDict, doCommit=True):
		wfComponentSQL.updateComponent(self.connection, _componentDict, doCommit=doCommit)

	def deleteComponent(self, _componentId, doCommit=True):
		wfComponentSQL.deleteComponent(self.connection, _componentId, doCommit=doCommit)

	def createComponentOverride(self, _overrideDict, doCommit=True):
		wfComponentSQL.createComponentOverride(self.connection, _overrideDict, doCommit=doCommit)

	def deleteComponentOverride(self, _componentOverrideId, doCommit=True):
		wfComponentSQL.deleteComponentOverride(self.connection, _componentOverrideId, doCommit=doCommit)

	def updateComponentOverride(self, _overrideDict, doCommit=True):
		wfComponentSQL.updateComponentOverride(self.connection, _overrideDict, doCommit=doCommit)

	#   Workflows

	def createWorkflow(self, _workflowDict, doCommit=True):
		wfComponentSQL.createWorkflow(self.connection, _workflowDict, doCommit=doCommit)

	def updateWorkflow(self, _workflowDict, doCommit=True):
		wfComponentSQL.updateWorkflow(self.connection, _workflowDict, doCommit=doCommit)
