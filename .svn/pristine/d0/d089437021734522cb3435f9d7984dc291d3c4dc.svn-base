# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as jobActionSvc
from MPSAppt.core.sql import fieldLevelRevisionsSQL
import MPSAppt.core.constants as constants

class FieldLevelRevisions(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getFieldLevelRevisionsForJobAction(self,_jobActionDict,_activeOnly=True):
		return fieldLevelRevisionsSQL.getFieldLevelRevisionsForJobAction(self.connection,_jobActionDict,_activeOnly)

	def getFieldLevelRevisionsReadyForDisplayForJobAction(self,_jobActionDict):
		return fieldLevelRevisionsSQL.getFieldLevelRevisionsReadyForDisplayForJobAction(self.connection,_jobActionDict)

	def getFieldLevelRevisionsReadyForNotificationForJobAction(self,_jobActionDict):
		return fieldLevelRevisionsSQL.getFieldLevelRevisionsReadyForNotificationForJobAction(self.connection,_jobActionDict)

	def getFieldLevelRevision(self,_jobActionDict,_revisionDict):
		return fieldLevelRevisionsSQL.getFieldLevelRevision(self.connection,_jobActionDict,_revisionDict)

	def updateFieldLevelRevisions(self,_jobActionDict,_jobTaskDict, _revisionDict,_now,_username, doCommit=True):
		if self.getFieldLevelRevision(_jobActionDict,_revisionDict):
			if _revisionDict.get('enabled',True):
				fieldLevelRevisionsSQL.updateFieldLevelRevision(self.connection,_jobActionDict,_revisionDict,_now,_username,doCommit)
			else:
				fieldLevelRevisionsSQL.deleteFieldLevelRevision(self.connection,_jobActionDict,_revisionDict,doCommit)
		else:
			if _revisionDict.get('enabled',True):
				fieldLevelRevisionsSQL.createFieldLevelRevision(self.connection,_jobActionDict,_revisionDict,_now,_username,doCommit)

	def updateRevisionsAsSent(self,_jobActionDict,_now, _username,doCommit=True):
		fieldLevelRevisionsSQL.updateRevisionsAsSent(self.connection,_jobActionDict.get('id',-1),_now, _username,doCommit)
		fieldLevelRevisionsSQL.updateJobActionRevisionsRequired(self.connection,_jobActionDict.get('id',-1),True,_now, _username,doCommit)

	def setRevisionsComplete(self,_jobActionId,_taskCode,_now,_username,doCommit=True):
		fieldLevelRevisionsSQL.setRevisionsComplete(self.connection,_jobActionId,_taskCode,_now, _username,doCommit)
		fieldLevelRevisionsSQL.updateJobActionRevisionsRequired(self.connection,_jobActionId,False,_now, _username,doCommit)

	def getFieldLevelRevisionsCache(self,_jobActionDict):
		cache = {}
		revisions = self.getFieldLevelRevisionsReadyForDisplayForJobAction(_jobActionDict)
		for revision in revisions:
			cache[revision.get('task_code','')] = revision
		return cache

	#   submit for each atomic revisions request
	def handleSubmit(self,_jobActionDict, _jobTaskDict, _revisionDict, _container, _profile, _now, _username, doCommit = True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			self.updateFieldLevelRevisions(_jobActionDict,_jobTaskDict, _revisionDict, _now, _username, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbRevisionsRequired
				logDict['item'] = ''
				logDict['message'] = 'Revisions Requested'
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	#   submit for notify candidate of revisions
	def handleNotifySubmit(self,_jobActionDict, _mockjobTaskDict, _container, _profile, _now, _username, doCommit = True):
		try:
			_container.prepareNotificationForSubmit(_jobActionDict)
			#   Common handler pre-commit activities.

			self.updateRevisionsAsSent(_jobActionDict, _now, _username,doCommit)
			self.commmonHandlerPrecommitTasks(_jobActionDict, {'id':0,'job_action_id':_jobActionDict.get('id',0)}, _container, _profile, {}, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

