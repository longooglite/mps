# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.approvalSQL as approvalSQL
import MPSAppt.services.jobActionService as jobActionSvc


class ApprovalService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getApproval(self, _jobTaskId):
		return approvalSQL.getApproval(self.connection, _jobTaskId)

	def createApproval(self, _approvalDict, doCommit=True):
		approvalSQL.createApproval(self.connection, _approvalDict, doCommit)

	def deleteApproval(self,approvalDict):
		approvalSQL.deleteApproval(self.connection,approvalDict.get('id',-1))
		jobActionSvc.JobActionService(self.connection).unfreezeJobTaskById(approvalDict.get('job_task_id',-1))

	def updateApproval(self, _jobTaskDict, _approvalDict, doCommit=True):
		existingApproval = self.getApproval(_jobTaskDict.get('id',0))

		try:
			if existingApproval:
				approvalSQL.updateApproval(self.connection, _approvalDict, doCommit=False)
			else:
				self.createApproval(_approvalDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def updateApprovalStatus(self, _jobTaskDict, _approvalDict, doCommit=True):
		approvalSQL.updateApprovalStatus(self.connection, _approvalDict, doCommit=False)


	def handleSubmit(self, _jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self._handle(_jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbSubmit, 'submitFreeze', 'dashboardEvents', doCommit)

	def handleApprove(self, _jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self._handle(_jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbApprove, 'approveFreeze','approveDashboardEvents', doCommit)

	def handleDeny(self, _jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self._handle(_jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbDeny, 'denyFreeze', 'denyDashboardEvents', doCommit)

	def handleRevisions(self, _jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self._handle(_jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbRevisionsRequired, 'revisionsRequiredFreeze', 'revisionsDashboardEvents', doCommit)

	def _handle(self, _jobActionDict, _jobTaskDict, _approvalDict, _container, _profile, _formData, _now, _username, _verb, _freezeConfigKey, _dashboardConfigKey, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Approval table row.
			self.updateApproval(_jobTaskDict, _approvalDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = _verb
				logDict['item'] = _container.getDescr()
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Activity Log Text override.
			freezeThawConfigDict = _container.getConfigDict().get(_freezeConfigKey, {})
			overrideActivityLogText = freezeThawConfigDict.get('activityLogText', None)
			if overrideActivityLogText:
				activityLogDict = _container.getConfigDict().get('activityLog',{})
				if activityLogDict:
					appendToActivityLogText = ''
					if _verb == constants.kJobActionLogVerbRevisionsRequired:
						appendToActivityLogText = self.getRevisionsRequiredItemText(_container,_formData)
					activityLogDict['activityLogText'] = overrideActivityLogText + appendToActivityLogText

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _dashboardConfigKeyName=_dashboardConfigKey, _freezeConfigKeyName=_freezeConfigKey, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def getRevisionsRequiredItemText(self,_container,_formData):
		itemList = []
		for key in _formData:
			if _formData.get(key) == 'true':
				item = _container.workflow.getContainer(key)
				if item:
					itemList.append(item.containerDict.get('descr',''))
		if itemList:
			return ': ' + ', '.join(itemList)
		return ''
