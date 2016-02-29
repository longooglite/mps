# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCV.services.metaService as metaSvc
import MPSCV.services.cvService as cvSvc
import MPSCV.core.cvSQL as cvSQL
import MPSCore.utilities.exceptionUtils as excUtils

class CVImporter():

	#   THIS METHOD ENTIRELY REPLACES A CV.
	#   THERE IS NO 'UPDATE' CAPABILITY.
	#   IT'S AN UN-CEREMONIOUS WIPE AND RELOAD.

	def doImport(self, _dbConnection, _cvDict, _overrideCommunity='', _overrideUsername='', _erasePubmedData=True):

		try:
			#   Get a community and username.
			#   If an override is provided, use it.
			#   Otherwise, we must find it in the given CV Data.

			community = _overrideCommunity
			if not community:
				community = _cvDict.get('community', '')
			if not community:
				raise excUtils.MPSException(_userMessage="Community not found")

			username = _overrideUsername
			if not username:
				username = _cvDict.get('username', '')
			if not username:
				raise excUtils.MPSException(_userMessage="User name not found")


			#   Determine if we have an existing CV for this username.
			personList = cvSvc.getPerson(_dbConnection, community, username)
			if personList:
				#   Delete an existing CV.
				cvSvc.deleteCV(_dbConnection, community, username, deletePerson=False, erasePubmedData=_erasePubmedData, doCommit=False)
			else:
				#   Create the CV Person.
				cvSvc.createPerson(_dbConnection, community, username, doCommit=False)

			#   Create the CV data rows.
			fieldCodeToIdCache = self.buildFieldCache(_dbConnection)
			for rowDict in _cvDict.get('rowList', []):
				self.processRow(_dbConnection, community, username, rowDict, fieldCodeToIdCache)

			#   Make it so.
			_dbConnection.performCommit()

		except Exception, e:
			try: _dbConnection.performRollback()
			except Exception, e1: pass
			raise

	def buildFieldCache(self, _dbConnection):
		fieldCodeToIdCache = {}
		fieldList = metaSvc.getAllFields(_dbConnection)
		for fieldDict in fieldList:
			id = fieldDict.get('id',None)
			code = fieldDict.get('code','')
			if id and code:
				fieldCodeToIdCache[code] = id
		return fieldCodeToIdCache

	def processRow(self, _dbConnection, _community, _username, _rowDict, _fieldCodeToIdCache):

		#   Map Field Codes in the input data to IDs.
		#   Ignore errors, those fields simply won't get imported.
		#   If we end up with no data for the row, don't add a row. Duh.

		haveData = False
		for fieldDict in _rowDict.get('fieldList', []):
			code = fieldDict.get('code', '')
			if code:
				id = _fieldCodeToIdCache.get(code, None)
				if id:
					fieldDict['id'] = id
					haveData = True

		if haveData:
			rowId = cvSvc.createBasicRow(_dbConnection, _community, _username, _rowDict, doCommit=False)[0]['id']

			for fieldDict in _rowDict.get('fieldList', []):
				if 'id' in fieldDict:
					insertDict = {}
					insertDict['row_id'] = rowId
					insertDict['field_code'] = fieldDict.get('code', '')
					insertDict['attribute_value'] = fieldDict.get('value', '')
					insertDict['who_dunit'] = fieldDict.get('who', _username)
					insertDict['when_dunit'] = fieldDict.get('when', '')
					cvSQL.insertAttribute(_dbConnection, insertDict, doCommit=False)
