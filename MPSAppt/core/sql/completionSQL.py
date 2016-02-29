# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getCompletion(_dbConnection, _jobTaskId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_completion', _jobTaskId, _key='job_task_id')

def createCompletion(_dbConnection, _completionDict, doCommit=True):
	sql = '''INSERT INTO wf_completion (job_task_id,effective_date,scheduled_date,termination_type_id,complete,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'''
	args = (_completionDict.get('job_task_id',None),
			_completionDict.get('effective_date',''),
			_completionDict.get('scheduled_date',''),
			_completionDict.get('termination_type_id',None),
			_completionDict.get('complete',False),
			_completionDict.get('created',''),
			_completionDict.get('updated',''),
			_completionDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateCompletion(_dbConnection, _completionDict, doCommit=True):
	sql = '''UPDATE wf_completion SET effective_date=%s,scheduled_date=%s,termination_type_id=%s,complete=%s,updated=%s,lastuser=%s WHERE job_task_id=%s;'''
	args = (_completionDict.get('effective_date',None),
			_completionDict.get('scheduled_date',None),
			_completionDict.get('termination_type_id',None),
			_completionDict.get('complete',False),
			_completionDict.get('updated',''),
			_completionDict.get('lastuser',''),
			_completionDict.get('job_task_id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
