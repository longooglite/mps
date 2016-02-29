# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils

def getAttestation(_dbconnection, _jobTaskId):
	sql = "SELECT * FROM wf_attest WHERE job_task_id = %s"
	args = (_jobTaskId,)
	qry = _dbconnection.executeSQLQuery(sql,args)
	if len(qry) > 0:
		return qry[0]
	else:
		return None

def createAttestation(_dbconnection, _attestDict, doCommit=False):
	sql = "INSERT INTO wf_attest (job_task_id,complete,attestor_name, attestor_department,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	args = (_attestDict.get('job_task_id',-1),
	        _attestDict.get('complete',False),
	        _attestDict.get('attestor_name',''),
	        _attestDict.get('attestor_department',''),
	        _attestDict.get('created',''),
	        _attestDict.get('updated',''),
	        _attestDict.get('lastuser',''))
	_dbconnection.executeSQLCommand(sql,args,doCommit)


def updateAttestation(_dbconnection, _attestDict, doCommit=False):
	sql = "UPDATE wf_attest SET complete = %s, attestor_name = %s, attestor_department = %s, updated = %s, lastuser = %s WHERE job_task_id = %s"
	args = (_attestDict.get('complete',False),
	        _attestDict.get('attestor_name',''),
	        _attestDict.get('attestor_department',''),
	        _attestDict.get('updated',''),
	        _attestDict.get('lastuser',''),
	        _attestDict.get('job_task_id',-1))
	_dbconnection.executeSQLCommand(sql,args,doCommit)


def getAllAttestsForPersonAndCodes(_dbconnection,codes,personDict):
	inClause = stringUtils.getSQLInClause(codes)
	sql = '''SELECT wf_attest.complete,
	wf_attest.created,
	wf_attest.updated,
	wf_attest.lastuser
	FROM wf_job_task,wf_job_action,wf_appointment,wf_attest
	WHERE wf_job_task.job_action_id = wf_job_action.id AND
	wf_job_action.appointment_id = wf_appointment.id AND
	wf_job_action.person_id = %s AND '''
	sql += '''wf_job_task.task_code IN%s ORDER BY created DESC''' % (inClause)
	args = (personDict.get('id',-1),)
	qry = _dbconnection.executeSQLQuery(sql,args)
	return qry

