# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.disclosureSQL as disclosureSQL
import MPSAppt.services.jobActionService as jobActionSvc


class DisclosureService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getDisclosure(self, _jobTaskId):
		#   Gets only the wf_disclosure table record.
		return disclosureSQL.getDisclosure(self.connection, _jobTaskId)

	def getFullDisclosure(self, _jobTaskId):
		#   Gets the wf_disclosure table record PLUS a List of attached wf_offenses,
		#   collapsed by offense_nbr.
		disclosure =  disclosureSQL.getDisclosure(self.connection, _jobTaskId)
		if not disclosure:
			return disclosure

		#   disclosure['offenses'] is a List of 'Aggregate Offense' dictionaries
		#   Each 'Aggregate Offense' dictionary contains:
		#       key 'disclosure_id'
		#       key 'offense_nbr'
		#       key 'field_list', whose value is a List of dictionaries, and each dictionary
		#           containing a single field key and associated value

		disclosure['offenses'] = self.getOffenses(disclosure.get('id',0))
		return disclosure

	def getOffenses(self, _disclosureId):
		offenses = []
		rawData = disclosureSQL.getOffenses(self.connection, _disclosureId)

		lastOffenseNbr = -1
		curOffense = {}
		for offenseDict in rawData:
			thisOffenseNbr = offenseDict.get('offense_nbr', -1)
			if thisOffenseNbr != lastOffenseNbr:
				curOffense = {}
				curOffense['disclosure_id'] = _disclosureId
				curOffense['offense_nbr'] = thisOffenseNbr
				curOffense['field_list'] = []
				offenses.append(curOffense)
				lastOffenseNbr = thisOffenseNbr
			curOffense['field_list'].append(offenseDict)

		return offenses

	def createDisclosure(self, _disclosureDict, doCommit=True):
		disclosureSQL.createDisclosure(self.connection, _disclosureDict, doCommit)

	def updateDisclosure(self, _jobTaskDict, _disclosureDict, doCommit=True):
		existingDisclosure = self.getDisclosure(_jobTaskDict.get('id',0))

		try:
			if existingDisclosure:
				_disclosureDict['id'] = existingDisclosure.get('id',0)
				disclosureSQL.updateDisclosure(self.connection, _disclosureDict, doCommit=False)
			else:
				self.createDisclosure(_disclosureDict, doCommit=False)
				disclosureId = self.connection.getLastSequenceNbr('wf_disclosure')
				_disclosureDict['id'] = disclosureId

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def updateOffenses(self, _jobTaskDict, _disclosureDict, doCommit=True):
		try:
			disclosureId = _disclosureDict.get('id',0)
			disclosureSQL.deleteOffensesForDisclosure(self.connection, disclosureId, doCommit=False)
			for offenseDict in _disclosureDict.get('offenses', []):
				offenseDict['disclosure_id'] = disclosureId
				disclosureSQL.createOffense(self.connection, offenseDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _disclosureDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Disclosure table row.
			#   Update associated Offenses.
			self.updateDisclosure(_jobTaskDict, _disclosureDict, doCommit=False)
			self.updateOffenses(_jobTaskDict, _disclosureDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbDisclose
				logDict['item'] = _container.getDescr()
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
