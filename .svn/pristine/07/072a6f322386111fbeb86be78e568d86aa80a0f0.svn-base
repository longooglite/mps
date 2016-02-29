# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.npiSQL as npiSQL
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.constants as constants


class NPIService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getNPI(self, _jobTaskId):
		return npiSQL.getNPI(self.connection,_jobTaskId)

	def updateNPI(self, _jobActionDict, _jobTaskDict, _npiDict, doCommit=True):
		existingNPI = self.getNPI(_jobTaskDict.get('id',0))

		try:
			if existingNPI:
				npiSQL.updateNPI(self.connection, _npiDict, doCommit=False)
			else:
				npiSQL.createNPI(self.connection, _npiDict, doCommit)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _npiDict, _container, _profile, _now, _username, doCommit = True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Confirm Title table row.
			self.updateNPI(_jobActionDict,_jobTaskDict, _npiDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				logDict['item'] = 'incomplete' if _npiDict.get('complete',False) else 'complete'
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
