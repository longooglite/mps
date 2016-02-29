# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.backgroundCheck.abstractBackgroundCheckService as absService
import MPSAppt.core.sql.lookupTableSQL as lookupTableSvc

class AbstractCredentialCheckService(absService.AbstractBackgroundCheckService):
	def __init__(self, _container, _dbConnection):
		absService.AbstractBackgroundCheckService.__init__(self, _container, _dbConnection)
		self.doCommit = True

	################################################################################
	#   Required method implementations.
	################################################################################

	#   Submit a request to the 3rd-party service, initiating a new request.
	#   See superclass for description.

	def submit(self, doCommit, **kwargs):
		self.doCommit = doCommit
		if self.isFake():
			return self.createFakeSubmissionResult(_success=True)
		raise Exception("non-fake submit is not supported")


	#   Query the status of an outstanding request.
	#   See superclass for description.

	def getCandidateStatus(self, _externalKey, doCommit, **kwargs):
		self.doCommit = doCommit
		if self.isFake():
			return self.createFakeCandidateStatusResult(_success=True, _forceComplete=False, _forceFlagged=False)
		raise Exception("non-fake getCandidateStatus is not supported")


	#   Obtain URL to the most recent report for an outstanding request.
	#   See superclass for description.

	def getCandidateReport(self, _externalKey, doCommit, **kwargs):
		self.doCommit = doCommit
		if self.isFake():
			return self.createFakeCandidateReportResult(_success=True)
		raise Exception("non-fake getCandidateReport is not supported")


	#   Obtain the List of Orders pertaining to this Background and Education Check request.
	#   See superclass for description.

	def getOrders(self, doCommit, **kwargs):
		self.doCommit = doCommit
		return self.getCredentialCheckOrders(**kwargs)


	################################################################################
	#   Support methods.
	################################################################################

	def createExternalKey(self):

		#   Returns a string representation of the next sequential integer external key.

		currentList = lookupTableSvc.getLookupTable(self.connection, 'wf_credential_check_sequence', _orderBy='id')
		if not currentList:
			sql = '''INSERT INTO wf_credential_check_sequence (seq) VALUES (1)'''
			self.connection.executeSQLCommand(sql, doCommit=self.doCommit)
			return '1'

		current = currentList[0]
		new = current.get('seq', 0) + 1
		sql = '''UPDATE wf_credential_check_sequence SET seq = %s'''
		self.connection.executeSQLCommand(sql, _args=(new,), doCommit=self.doCommit)
		return str(new)



	################################################################################
	#   Fakes.
	################################################################################

	def createFakeSubmissionResult(self, _success=True):
		result = { 'externalKey': self.createExternalKey() }
		if _success:
			self.setOKStatus(result)
		else:
			self.setErrorStatus(result)
			result['error'] = "System-generated error: submit"
		return result

	def createFakeCandidateStatusResult(self, _success=True, _forceComplete=False, _forceFlagged=False):
		result = { 'complete': _forceComplete, 'flagged': _forceFlagged }
		if _success:
			self.setOKStatus(result)
		else:
			self.setErrorStatus(result)
			result['error'] = "System-generated error: get candidate status"
		return result

	def createFakeCandidateReportResult(self, _success=True):
		result = { }
		if _success:
			self.setOKStatus(result)
			result['url'] = 'http://cache.freescale.com/files/microcontrollers/doc/app_note/AN3414.pdf'
		else:
			self.setErrorStatus(result)
			result['error'] = "System-generated error: get candidate report"
		return result



	################################################################################
	#   Abstract methods (subclasses must implement).
	################################################################################

	#   Obtain the List of Orders pertaining to this Background and Education Check request.
	#   This is a pass-thru call to satisfy AbstractCredentialCheckService's getOrders method.
	#   See superclass for description.

	def getCredentialCheckOrders(self, **kwargs):
		raise Exception("getCredentialCheckOrders not implemented")
