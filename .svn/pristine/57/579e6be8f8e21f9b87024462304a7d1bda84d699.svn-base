# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getDisclosure(_dbConnection, _jobTaskId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_disclosure', _jobTaskId, _key='job_task_id')

def getOffenses(_dbConnection, _disclosureId):
	return lookupTableSvc.getEntityListByKey(_dbConnection, 'wf_offense', _disclosureId, _key='disclosure_id', _orderBy='offense_nbr,offense_key')

def createDisclosure(_dbConnection, _disclosureDict, doCommit=True):
	sql = '''INSERT INTO wf_disclosure (job_task_id,has_disclosures,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s);'''
	args = (_disclosureDict.get('job_task_id',None),
			_disclosureDict.get('has_disclosures',False),
			_disclosureDict.get('created',''),
			_disclosureDict.get('updated',''),
			_disclosureDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateDisclosure(_dbConnection, _disclosureDict, doCommit=True):
	sql = '''UPDATE wf_disclosure SET has_disclosures=%s,updated=%s,lastuser=%s WHERE job_task_id=%s;'''
	args = (_disclosureDict.get('has_disclosures',False),
			_disclosureDict.get('updated',''),
			_disclosureDict.get('lastuser',''),
			_disclosureDict.get('job_task_id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createOffense(_dbConnection, _offenseDict, doCommit=True):
	sql = '''INSERT INTO wf_offense (disclosure_id,offense_nbr,offense_key,offense_value,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s);'''
	args = (_offenseDict.get('disclosure_id',None),
			_offenseDict.get('offense_nbr',None),
			_offenseDict.get('offense_key',None),
			_offenseDict.get('offense_value',None),
			_offenseDict.get('created',''),
			_offenseDict.get('updated',''),
			_offenseDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteOffensesForDisclosure(_dbConnection, _disclosureId, doCommit=True):
	sql = '''DELETE FROM wf_offense WHERE disclosure_id = %s'''
	args = (_disclosureId,)
	_dbConnection.executeSQLCommand(sql, args, doCommit)
