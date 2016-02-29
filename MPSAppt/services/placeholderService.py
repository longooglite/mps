# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.placeholderSQL as placeholderSQL
import MPSAppt.services.jobActionService as jobActionSvc


class PlaceholderService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getPlaceholder(self, _jobTaskId):
		return placeholderSQL.getPlaceholder(self.connection, _jobTaskId)

	def createPlaceholder(self, _placeholderDict, doCommit=True):
		placeholderSQL.createPlaceholder(self.connection, _placeholderDict, doCommit)

	def updatePlaceholder(self, _jobTaskDict, _placeholderDict, doCommit=True):
		existingPlaceholder = self.getPlaceholder(_jobTaskDict.get('id',0))

		try:
			if existingPlaceholder:
				placeholderSQL.updatePlaceholder(self.connection, _placeholderDict, doCommit=False)
			else:
				self.createPlaceholder(_placeholderDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _placeholderDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Placeholder table row.
			self.updatePlaceholder(_jobTaskDict, _placeholderDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				logDict['item'] = 'incomplete' if _placeholderDict.get('complete',False) else 'complete'
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
