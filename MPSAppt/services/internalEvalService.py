# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.internalEvalSQL as intEvalSQL

class InternalEvalService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getAllEvaluators(self, _includeInactive=True):
		return intEvalSQL.getAllEvaluators(self.connection, _includeInactive=_includeInactive)

	def getEvaluator(self, _evaluatorId):
		return intEvalSQL.getEvaluator(self.connection, _evaluatorId)

	def createEvaluator(self, _evaluatorDict, doCommit=True):
		intEvalSQL.createEvaluator(self.connection, _evaluatorDict, doCommit=doCommit)

	def updateEvaluator(self, _evaluatorDict, doCommit=True):
		intEvalSQL.updateEvaluator(self.connection, _evaluatorDict, doCommit=doCommit)

	def saveInternalEvaluator(self, _evaluatorDict, _isEdit, doCommit=True):
		try:
			if _isEdit:
				self.updateEvaluator(_evaluatorDict, doCommit=False)
			else:
				self.createEvaluator(_evaluatorDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
