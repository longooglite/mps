# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.core.sql.terminationSQL as terminationSQL

class TerminationService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getTerminationTypes(self):
		return terminationSQL.getTerminationTypes(self.connection)