# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getMailById(_dbConnection, _emailId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_email', _emailId, _key='id')

def createEMail(_dbConnection, _emailDict, doCommit=True):
	sql = '''INSERT INTO wf_email (job_action_id,task_code,email_from,email_to,email_cc,email_bcc,email_subject,email_body,email_date,email_sent,email_send_response,created,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_emailDict.get('job_action_id',''),
			_emailDict.get('task_code',''),
			_emailDict.get('email_from',''),
			_emailDict.get('email_to',''),
			_emailDict.get('email_cc',''),
			_emailDict.get('email_bcc',''),
			_emailDict.get('email_subject',''),
			_emailDict.get('email_body',''),
			_emailDict.get('email_date',''),
			_emailDict.get('email_sent',''),
			_emailDict.get('email_send_response',''),
			_emailDict.get('created',''),
			_emailDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateSentEmail(_dbConnection, _emailId, _send_response, _sent, doCommit=True):
	sql = '''UPDATE wf_email SET email_sent = %s, email_send_response = %s WHERE id = %s'''
	args = (_sent, _send_response, _emailId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteEmail(_dbConnection, _emailId, doCommit=True):
	args = (_emailId,)
	_dbConnection.executeSQLCommand('''DELETE FROM wf_email_attachment WHERE email_id=%s''', args, doCommit)
	_dbConnection.executeSQLCommand('''DELETE FROM wf_email WHERE id=%s''', args, doCommit)

def getEmailsForJobActionId(_dbConnection,_jobactionId):
	sql = "SELECT * FROM wf_email WHERE job_action_id = %s ORDER BY email_date ASC"
	args = (_jobactionId,)
	return _dbConnection.executeSQLQuery(sql,args)

def getEmail(_dbConnection,_emailId):
	sql = "SELECT * FROM wf_email WHERE id = %s"
	args = (_emailId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

