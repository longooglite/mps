# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.sql.confirmTitleSQL as confirmTitleSQL
import MPSAppt.core.constants as constants

class ConfirmedTitleService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getConfirmedTitle(self, _jobTaskId):
		return confirmTitleSQL.getConfirmedTitle(self.connection, _jobTaskId)

	def createConfirmedTitle(self, _confirmedTitleDict, doCommit=True):
		confirmTitleSQL.createConfirmedTitle(self.connection, _confirmedTitleDict, doCommit)

	def deleteConfirmedTitle(self,confirmedTitleDict):
		confirmTitleSQL.deleteConfirmedTitle(self.connection,confirmedTitleDict.get('id',-1))
		jobActionSvc.JobActionService(self.connection).unfreezeJobTaskById(confirmedTitleDict.get('job_task_id',-1))

	def updateConfirmedTitle(self, _jobActionDict, _jobTaskDict, _confirmedTitleDict, updateAppointmentTitle, doCommit=True):
		existingConfirmedTitle = self.getConfirmedTitle(_jobTaskDict.get('id',0))

		try:
			if updateAppointmentTitle:
				jobActionSvc.JobActionService(self.connection).updateAppointmentTitle(_jobActionDict.get('appointment_id',0),_confirmedTitleDict.get('title_id'),_confirmedTitleDict.get('updated',''),_confirmedTitleDict.get('lastuser',''),doCommit)
			if existingConfirmedTitle:
				confirmTitleSQL.updateConfirmedTitle(self.connection, _confirmedTitleDict, doCommit=False)
			else:
				self.createConfirmedTitle(_confirmedTitleDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, confirmedTitleDict, _container, _profile, _now, _username, doCommit = True):
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
			updateAppointmentTitle = True
			if _container.getConfigDict().get('secondaryAppointmentMode',False):
				updateAppointmentTitle = False
			self.updateConfirmedTitle(_jobActionDict,_jobTaskDict, confirmedTitleDict,updateAppointmentTitle, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				logDict['item'] = 'incomplete' if confirmedTitleDict.get('complete',False) else 'complete'
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
