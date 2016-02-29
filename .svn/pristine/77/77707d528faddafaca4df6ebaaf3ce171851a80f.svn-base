# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.serviceAndRankSQL as serviceAndRankSQL
import MPSAppt.services.jobActionService as jobActionSvc


class ServiceAndRankService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getServiceAndRank(self, _jobTaskId):
		return serviceAndRankSQL.getServiceAndRank(self.connection, _jobTaskId)

	def getBuildings(self):
		return serviceAndRankSQL.getBuildings(self.connection)

	def updateServiceAndRank(self,_jobTaskDict, _serviceAndRankDict, doCommit=True):
		if serviceAndRankSQL.getServiceAndRank(self.connection,_jobTaskDict.get('id',-1)):
			serviceAndRankSQL.updateServiceAndRank(self.connection,_jobTaskDict, _serviceAndRankDict, doCommit)
		else:
			serviceAndRankSQL.createServiceAndRank(self.connection,_jobTaskDict, _serviceAndRankDict, doCommit)

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _serviceAndRankDict, _container, _profile, _now, _username, doCommit=True):
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
			self.updateServiceAndRank(_jobTaskDict, _serviceAndRankDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				logDict['item'] = 'complete'
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


	# def updatePlaceholder(self, _jobTaskDict, _placeholderDict, doCommit=True):
	# 	existingPlaceholder = self.getPlaceholder(_jobTaskDict.get('id',0))
	#
	# 	try:
	# 		if existingPlaceholder:
	# 			placeholderSQL.updatePlaceholder(self.connection, _placeholderDict, doCommit=False)
	# 		else:
	# 			self.createPlaceholder(_placeholderDict, doCommit=False)
	#
	# 		if doCommit:
	# 			self.connection.performCommit()
	#
	# 	except Exception, e:
	# 		try: self.connection.performRollback()
	# 		except Exception, e1: pass
	# 		raise e
	#
