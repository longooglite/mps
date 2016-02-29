# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.sql.jointPromotionsSQL as jointPromotionSQL
import MPSAppt.core.constants as constants

class JointPromotionsService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getJointPromotions(self, _jobTaskId):
		return jointPromotionSQL.getJointPromotions(self.connection, _jobTaskId)

	def createJointPromotion(self, _jointPromotionsDict, _job_TaskId, _username, _now, doCommit=True):
		jointPromotionSQL.createJointPromotion(self.connection, _jointPromotionsDict, _job_TaskId, _username, _now, doCommit)

	def deleteAllJointPromotions(self,_jobTaskDict, doCommit=True):
		jointPromotionSQL.deleteAllJointPromotions(self.connection,_jobTaskDict.get('id',-1),doCommit)

	def updateJointPromotions(self, _jobActionDict, _jobTaskDict, _jointPromotionsList, _username, _now, doCommit=True):
		try:
			self.deleteAllJointPromotions(_jobTaskDict,doCommit)
			for jointPromotionDict in _jointPromotionsList:
				self.createJointPromotion(jointPromotionDict,_jobTaskDict.get('id',-1),_username,_now)
			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _jointPromotionsDict, _container, _profile, _now, _username, doCommit = True):
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
			self.updateJointPromotions(_jobActionDict,_jobTaskDict, _jointPromotionsDict,_username, _now, doCommit=False)

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
