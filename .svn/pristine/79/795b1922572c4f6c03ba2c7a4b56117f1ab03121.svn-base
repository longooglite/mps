# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as jobActionService
import MPSAppt.core.sql.jobPostingSQL as jobPostingSQL
import MPSAppt.core.constants as constants

class JobPostingService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getJobPosting(self,jobTaskId):
		return jobPostingSQL.getJobPosting(self.connection,jobTaskId)


	def addOrUpdateJobPosting(self, _jobTaskDict, _jobPostingDict, doCommit=True):
		existingJobPosting = self.getJobPosting(_jobTaskDict.get('id',0))
		try:
			if existingJobPosting:
				jobPostingSQL.updateJobPosting(self.connection, _jobPostingDict, doCommit=False)
			else:
				jobPostingSQL.createJobPosting(self.connection, _jobPostingDict, doCommit = False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _jobPostingDict, _container, _profile,doCommit = True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _jobPostingDict.get('created','')
			logDict['lastuser'] = _jobPostingDict.get('lastuser','')

			#   Create/Update the Job Posting table row.
			self.addOrUpdateJobPosting(_jobTaskDict, _jobPostingDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				logDict['item'] = 'incomplete' if _jobPostingDict.get('complete',False) else 'complete'
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionService.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _jobPostingDict.get('created',''), _jobPostingDict.get('lastuser',''), doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
