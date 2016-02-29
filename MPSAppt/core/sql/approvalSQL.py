# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getApproval(_dbConnection, _jobTaskId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_approval', _jobTaskId, _key='job_task_id')

def deleteApproval(_dbConnection, approvalId):
	sql = "DELETE FROM wf_approval WHERE id = %s"
	args = (approvalId,)
	_dbConnection.executeSQLCommand(sql,args)

def createApproval(_dbConnection, _approvalDict, doCommit=True):
	sql = '''INSERT INTO wf_approval (job_task_id,approval,approval_date,vote_for,vote_against,vote_abstain,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
	args = (_approvalDict.get('job_task_id',None),
			_approvalDict.get('approval',None),
			_approvalDict.get('approval_date',None),
			_approvalDict.get('vote_for',0),
			_approvalDict.get('vote_against',0),
			_approvalDict.get('vote_abstain',0),
			_approvalDict.get('created',''),
			_approvalDict.get('updated',''),
			_approvalDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateApproval(_dbConnection, _approvalDict, doCommit=True):
	sql = '''UPDATE wf_approval SET approval=%s,approval_date=%s,vote_for=%s,vote_against=%s,vote_abstain=%s,updated=%s,lastuser=%s WHERE job_task_id=%s;'''
	args = (_approvalDict.get('approval',None),
			_approvalDict.get('approval_date',None),
			_approvalDict.get('vote_for',0),
			_approvalDict.get('vote_against',0),
			_approvalDict.get('vote_abstain',0),
			_approvalDict.get('updated',''),
			_approvalDict.get('lastuser',''),
			_approvalDict.get('job_task_id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateApprovalStatus(_dbConnection, _approvalDict, doCommit=True):
	sql = '''UPDATE wf_approval SET approval=%s,updated=%s,lastuser=%s WHERE job_task_id=%s;'''
	args = (_approvalDict.get('approval',None),
			_approvalDict.get('updated',''),
			_approvalDict.get('lastuser',''),
			_approvalDict.get('job_task_id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
