# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getPlaceholder(_dbConnection, _jobTaskId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_placeholder', _jobTaskId, _key='job_task_id')

def createPlaceholder(_dbConnection, _placeholderDict, doCommit=True):
	sql = '''INSERT INTO wf_placeholder (job_task_id,complete,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s);'''
	args = (_placeholderDict.get('job_task_id',None),
			_placeholderDict.get('complete',False),
			_placeholderDict.get('created',''),
			_placeholderDict.get('updated',''),
			_placeholderDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updatePlaceholder(_dbConnection, _placeholderDict, doCommit=True):
	sql = '''UPDATE wf_placeholder SET complete=%s,updated=%s,lastuser=%s WHERE job_task_id=%s;'''
	args = (_placeholderDict.get('complete',False),
			_placeholderDict.get('updated',''),
			_placeholderDict.get('lastuser',''),
			_placeholderDict.get('job_task_id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
