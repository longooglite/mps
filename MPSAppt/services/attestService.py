# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.attestSQL as attestSQL
import MPSAppt.services.jobActionService as jobActionSvc
import MPSCore.utilities.dateUtilities as dateUtilities

class AttestService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def findViableAttest(self,codes,lookbackDays,personDict):
		rawAttests = attestSQL.getAllAttestsForPersonAndCodes(self.connection,codes,personDict)
		for attest in rawAttests:
			attestDate = dateUtilities.parseDate(attest.get('created',''),'%Y-%m-%d')
			exceeds,days = dateUtilities.datePlusDaysExceedsNow(attestDate,lookbackDays)
			if not exceeds:
				return attest
		return None

	def getAttestation(self, _jobTaskId):
		return attestSQL.getAttestation(self.connection, _jobTaskId)

	def createAttestation(self, _attestDict, doCommit=True):
		attestSQL.createAttestation(self.connection, _attestDict, doCommit)

	def updateAttestation(self, _jobTaskDict, _attestDict, doCommit=True):
		existingAttestation = self.getAttestation(_jobTaskDict.get('id',0))

		try:
			if existingAttestation:
				attestSQL.updateAttestation(self.connection, _attestDict, doCommit=False)
			else:
				self.createAttestation(_attestDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _attestDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Attestation table row.
			self.updateAttestation(_jobTaskDict, _attestDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbAttest
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
