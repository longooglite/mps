# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json
import MPSCV.core.cvSQL as cvSQL
import MPSCV.services.metaService as metaSvc
import MPSCV.utilities.environmentUtils as envUtils
import MPSCore.utilities.dictUtilities as dictUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

######################## CV Person ########################

def getPerson(_connection, _community, _user_id):
	return cvSQL.getPerson(_connection, _community, _user_id)

def createPerson(_connection, _community, _user_id, doCommit=True):
	if getPerson(_connection, _community, _user_id) == []:
		return cvSQL.createPerson(_connection, _community, _user_id, doCommit)

def initializeCV(_connection, _community, _user_id, _fieldCode, _fieldValue):
	ts = envUtils.getEnvironment().formatUTCDate()

	try:
		#   Create a row.
		rowDict = {}
		rowDict['cvCommunity'] = _community
		rowDict['cvOwnerName'] = _user_id
		rowDict['exclude_from_cv_val'] = False
		rowDict['user_sort_seq'] = 0
		rowDict['who_dunit'] = _user_id
		rowDict['when_dunit'] = ts
		rowId = cvSQL.insertRow(_connection, rowDict, doCommit=False)[0]['id']

		#   Add an attribute
		attributeDict = {}
		attributeDict['row_id'] = rowId
		attributeDict['field_code'] = _fieldCode
		attributeDict['attribute_value'] = _fieldValue
		attributeDict['who_dunit'] = _user_id
		attributeDict['when_dunit'] = ts
		cvSQL.insertAttribute(_connection, attributeDict, doCommit=False)

		_connection.performCommit()

	except Exception, e:
		try: _connection.performRollback()
		except Exception, e1: pass
		raise e

def getFormalName(connection, community, username, cvNameCode):
	return cvSQL.getFormalName(connection, community, username, cvNameCode)

def getProxiedCVsForGrantee(connection, _grantee_community, _grantee):
	return cvSQL.getProxiedCVsForGrantee(connection, _grantee_community, _grantee)

def getProxiedCVsForGrantor(connection, _grantor_community, _grantor):
	return cvSQL.getProxiedCVsForGrantor(connection, _grantor_community, _grantor)

def getProxiedCVForGrantorAndGrantee(connection, _grantor_community, _grantor, _grantee_community, _grantee):
	return cvSQL.getProxiedCVForGrantorAndGrantee(connection, _grantor_community, _grantor, _grantee_community, _grantee)

def saveNewProxy(connection, _grantor_community, _grantor, _grantee_community, _grantee, canReadWrite):
	now = envUtils.getEnvironment().formatUTCDate()
	cvSQL.saveNewProxy(connection, _grantor_community, _grantor, _grantee_community, _grantee, canReadWrite, now)

def updateProxyApproval(connection,id,canWrite,approved):
	now = envUtils.getEnvironment().formatUTCDate()
	if approved:
		cvSQL.updateProxyApproval(connection,id,canWrite,now)
	else:
		cvSQL.updateProxyDenied(connection,id,now)

def updateProxyRole(connection,id,canWrite):
	cvSQL.updateProxyRole(connection, id, canWrite)

def updateProxyDenied(connection,id):
	now = envUtils.getEnvironment().formatUTCDate()
	cvSQL.updateProxyDenied(connection, id, now)

def saveRequestForProxyAccess(connection,cvholder_community,cvholder,proxyrequestor_community,proxyrequestor,requestingReadWrite):
	now = envUtils.getEnvironment().formatUTCDate()
	cvSQL.saveRequestForProxyAccess(connection, cvholder_community, cvholder, proxyrequestor_community, proxyrequestor, requestingReadWrite, now)


######################## CV Data ########################

def getRow(_dbConnection, _rowId):
	return cvSQL.getRow(_dbConnection, _rowId)

def getRowData(_dbConnection, _rowId):
	return cvSQL.getRowData(_dbConnection, _rowId)

def getRowPerson(_dbConnection, _rowId):
	return cvSQL.getRowPerson(_dbConnection, _rowId)

def getCVListDisplayDataForUser(_dbConnection, _community, _username, _categoryName, isPrintedCV=False):
	flatList = cvSQL.getCVListDisplayDataForUser(_dbConnection, _community, _username, _categoryName, isPrintedCV)
	rowList = _organizeCVListDisplayDataByRow(flatList, isPrintedCV)
	subcategoryList = metaSvc.getSubCategoriesForCategory(_dbConnection, _categoryName)
	_applySubcategoriesToRows(subcategoryList, rowList)
	rowList = _removeNonDisplayColumns(rowList, isPrintedCV)

	result = {}
	for rowDict in rowList:
		if isPrintedCV and rowDict.get('row_exclude_from_cv_val',False):
			pass
		else:
			groupCode = rowDict.get('group_code', None)
			if groupCode:
				groupDict = result.get(groupCode, None)
				if not groupDict:
					groupDict = {}
					dictUtils.copyKeysWithPrefix(rowDict, groupDict, 'group_')
					groupDict['rowList'] = []
					groupDict['rowList'].append(rowDict)
					result[groupCode] = groupDict
				else:
					groupDict['rowList'].append(rowDict)
	return result

def _organizeCVListDisplayDataByRow(_flatList,isPrintedCV = False):
	rowList = []
	lastRowId = -1
	curRowDict = None

	for flatDict in _flatList:
		thisRowId = flatDict.get('row_id', 0)
		if thisRowId != lastRowId:
			lastRowId = thisRowId
			curRowDict = {}
			curRowDict['fieldList'] = []
			dictUtils.copyKeysWithPrefix(flatDict, curRowDict, 'row_')
			rowList.append(curRowDict)

		fieldDict = {}
		dictUtils.copyKeysWithPrefix(flatDict, fieldDict, 'field_')
		dictUtils.copyKeysWithPrefix(flatDict, fieldDict, 'affordance_')
		dictUtils.copyKeysWithPrefix(flatDict, fieldDict, 'attribute_')
		if fieldDict.get('attribute_value','') and fieldDict.get('affordance_code','') == 'Repeating_Text':
			fieldDict['attribute_value'] = getCategoryListHeader(fieldDict['attribute_value'],isPrintedCV)
		if fieldDict.get('attribute_value','') and fieldDict.get('affordance_code','') == 'Repeating_Text_Selector':
			fieldDict['attribute_value'] = getCategoryListSelectorHeader(fieldDict['attribute_value'],isPrintedCV)

		curRowDict['fieldList'].append(fieldDict)

	return rowList

def getCategoryListHeader(jsonList,isPrintedCV=False):
	delimiter = '; '
	if isPrintedCV:
		delimiter = '<br/>'
	theList = json.loads(jsonList)
	if len(theList) == 1:
		return theList[0]
	else:
		return delimiter.join(theList)

def getCategoryListSelectorHeader(jsonList,isPrintedCV=False):
	delimiter = '; '
	if isPrintedCV:
		delimiter = '<br/>'
	rawList = json.loads(jsonList)
	newList = []
	for elem in rawList:
		newList.append(elem.get('name',''))
	return delimiter.join(newList)

def _applySubcategoriesToRows(_subCategoryList, _rowList):
	if not _subCategoryList:
		return

	for _rowDict in _rowList:
		if len(_subCategoryList) == 1:
			_applySubcategoryToRow(_subCategoryList[0], _rowDict)
		else:
			for fieldDict in _rowDict.get('fieldList', []):
				if fieldDict.get('affordance_code', '') == 'Category':
					subcategoryName = fieldDict.get('attribute_value', '')
					for subCategoryDict in _subCategoryList:
						if subCategoryDict.get('code', '') == subcategoryName:
							_applySubcategoryToRow(subCategoryDict, _rowDict)
							break;

		if 'group_id' not in _rowDict:
			_applySubcategoryToRow(_subCategoryList[0], _rowDict)

def _applySubcategoryToRow(_subcategoryDict, _rowDict):
	dictUtils.copyKeysWithPrefix(_subcategoryDict, _rowDict, 'group_')

def _removeNonDisplayColumns(_rowList, isPrintedCV = False):
	result = []
	for rowDict in _rowList:
		newDict = {}
		dictUtils.copyKeysWithPrefix(rowDict, newDict, 'row_')
		dictUtils.copyKeysWithPrefix(rowDict, newDict, 'group_')
		newDict['fieldList'] = []
		key = "field_display_on_list_seq"
		if isPrintedCV:
			key = "field_display_on_pdf_seq"
		for fieldDict in rowDict.get('fieldList', []):
			if fieldDict.get(key, ''):
				newDict['fieldList'].append(fieldDict)
		result.append(newDict)

	return result

def getCVExportDataForUser(_dbConnection, _community, _username):
	rowList = []
	flatList = cvSQL.getCVExportDataForUser(_dbConnection, _community, _username)

	if flatList:
		lastRowId = -1
		curRowDict = None

		for flatDict in flatList:
			thisRowId = flatDict.get('row_id', 0)
			if thisRowId != lastRowId:
				lastRowId = thisRowId
				curRowDict = {}
				curRowDict['exclude'] = flatDict.get('row_exclude_from_cv_val', False)
				curRowDict['sortSeq'] = flatDict.get('row_user_sort_seq', 0)
				curRowDict['who'] = flatDict.get('row_who_dunit', '')
				curRowDict['when'] = flatDict.get('row_when_dunit', '')
				curRowDict['fieldList'] = []
				rowList.append(curRowDict)

			fieldDict = {}
			fieldDict['code'] = flatDict.get('field_code', '')
			fieldDict['value'] = flatDict.get('attribute_value', '')
			fieldDict['who'] = flatDict.get('attribute_who_dunit', '')
			fieldDict['when'] = flatDict.get('attribute_when_dunit', '')
			curRowDict['fieldList'].append(fieldDict)

	result = {}
	result['community'] = _community
	result['username'] = _username
	result['rowList'] = rowList
	return result


@mpsExceptionWrapper("Unable to save CV data")
def saveRowData(_dbConnection, _cvCommunity, _cvOwnerName, _rowDict, _insertList, _updateList, _loggedInUser):
	ts = envUtils.getEnvironment().formatUTCDate()

	#   Save all data in a single transaction.

	try:
		#   Update the cv_row.
		modRowDict = {}
		modRowDict['exclude_from_cv_val'] = _rowDict.get('exclude_from_cv_val', False)
		modRowDict['user_sort_seq'] = _rowDict.get('user_sort_seq', 0)
		modRowDict['who_dunit'] = _loggedInUser
		modRowDict['when_dunit'] = ts
		if 'row_id' in _rowDict:
			rowId = _rowDict['row_id']
			modRowDict['id'] = rowId
			cvSQL.saveRow(_dbConnection, modRowDict, doCommit=False)
		else:
			modRowDict['cvCommunity'] = _cvCommunity
			modRowDict['cvOwnerName'] = _cvOwnerName
			rowId = cvSQL.insertRow(_dbConnection, modRowDict, doCommit=False)[0]['id']

		#   Do cv_attribute inserts.
		for keyValueTuple in _insertList:
			insertDict = {}
			insertDict['row_id'] = rowId
			insertDict['field_code'] = keyValueTuple[0]
			insertDict['attribute_value'] = keyValueTuple[1]
			insertDict['who_dunit'] = _loggedInUser
			insertDict['when_dunit'] = ts
			cvSQL.insertAttribute(_dbConnection, insertDict, doCommit=False)

		#   Do cv_attribute updates.
		for idValueTuple in _updateList:
			updateDict = {}
			updateDict['id'] = idValueTuple[0]
			updateDict['attribute_value'] = idValueTuple[1]
			updateDict['who_dunit'] = _loggedInUser
			updateDict['when_dunit'] = ts
			cvSQL.saveAttribute(_dbConnection, updateDict, doCommit=False)

		_dbConnection.performCommit()

	except Exception, e:
		try: _dbConnection.performRollback()
		except Exception, e1: pass
		raise e

def createBasicRow(_dbConnection, _cvCommunity, _cvOwnerName, _rowDict, doCommit=True):
	insertDict = {}
	insertDict['cvCommunity'] = _cvCommunity
	insertDict['cvOwnerName'] = _cvOwnerName
	insertDict['exclude_from_cv_val'] = _rowDict.get('exclude', False)
	insertDict['user_sort_seq'] = _rowDict.get('sortSeq', 0)
	insertDict['who_dunit'] = _rowDict.get('who', _cvOwnerName)
	insertDict['when_dunit'] = _rowDict.get('when', '')
	return cvSQL.insertRow(_dbConnection, insertDict, doCommit)

@mpsExceptionWrapper("Unable to resequence CV data")
def resequence(_dbConnection, _rowSequenceList):

	#   Save all data in a single transaction.

	sequenceNbr = 1
	try:
		for rowId in _rowSequenceList:
			cvSQL.updateRowSequence(_dbConnection, rowId, sequenceNbr, doCommit=False)
			sequenceNbr += 1

		_dbConnection.performCommit()

	except Exception, e:
		try: _dbConnection.performRollback()
		except Exception, e1: pass
		raise e

@mpsExceptionWrapper("Unable to delete CV data")
def deleteRow(_dbConnection, _rowId, doCommit=True):

	#   Delete all data in a single transaction.
	try:
		cvSQL.deleteAttributesForRow(_dbConnection, _rowId, doCommit=False)
		cvSQL.deleteRow(_dbConnection, _rowId, doCommit=False)
		if doCommit:
			_dbConnection.performCommit()

	except Exception, e:
		try: _dbConnection.performRollback()
		except Exception, e1: pass
		raise e

@mpsExceptionWrapper("Unable to delete CV")
def deleteCV(_dbConnection, _community, _username, deletePerson=False, erasePubmedData=True, doCommit=True):

	#   Obliterate the CV data for the named Person.
	#   Optionally erase Pubmed data.
	#   Optionally delete the person table row.
	#   Delete all data in a single transaction.
	try:
		if erasePubmedData or deletePerson:
			cvSQL.deletePubmedPubsForUsername(_dbConnection, _community, _username, doCommit=False)
			cvSQL.deletePubmedHeadersForUsername(_dbConnection, _community, _username, doCommit=False)

		cvSQL.deleteAttributesForUsername(_dbConnection, _community, _username, doCommit=False)
		cvSQL.deleteRowsForUsername(_dbConnection, _community, _username, doCommit=False)

		if deletePerson:
			cvSQL.deletePerson(_dbConnection, _community, _username, doCommit=False)
		else:
			cvSQL.whackPersonData(_dbConnection, _community, _username, doCommit=False)

		if doCommit:
			_dbConnection.performCommit()

	except Exception, e:
		try: _dbConnection.performRollback()
		except Exception, e1: pass
		raise e


###### pubmed ######
def importPubMedData(_dbConnection, cv_id,pubData,authorSearchString = ''):
	now = envUtils.getEnvironment().formatUTCDate()
	pubimportResult = cvSQL.createPubImportHeader(_dbConnection,cv_id, now)
	if len(pubimportResult) > 0:
		pubimportId = pubimportResult[0].get('id',-1)
		didInsert = False
		if pubimportId > -1:
			for pub in pubData:
				didInsert = cvSQL.importPubMedData(_dbConnection, pubimportId, cv_id, pub.serializePublication(), now, pub.uid, authorSearchString)
			if didInsert:
				_dbConnection.executeSQLCommand("COMMIT;", ())
			else:
				cvSQL.removePubHeader(_dbConnection,pubimportId)
