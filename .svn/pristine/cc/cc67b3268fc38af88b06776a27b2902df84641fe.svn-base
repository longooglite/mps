# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.buildingSQL as bldgSQL

class BuildingService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getAllBuildings(self, _includeInactive=True, _orderByDescr=False):
		return bldgSQL.getAllBuildings(self.connection, _includeInactive=_includeInactive, _orderByDescr=_orderByDescr)

	def getBuilding(self, _buildingId):
		return bldgSQL.getBuilding(self.connection, _buildingId)

	def createBuilding(self, _buildingDict, doCommit=True):
		bldgSQL.createBuilding(self.connection, _buildingDict, doCommit=doCommit)

	def updateBuilding(self, _buildingDict, doCommit=True):
		bldgSQL.updateBuilding(self.connection, _buildingDict, doCommit=doCommit)

	def saveBuilding(self, _buildingDict, _isEdit, doCommit=True):
		try:
			if _isEdit:
				self.updateBuilding(_buildingDict, doCommit=False)
			else:
				self.createBuilding(_buildingDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
