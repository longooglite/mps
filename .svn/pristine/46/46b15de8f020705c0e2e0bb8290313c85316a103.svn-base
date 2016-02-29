# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getFieldLevelRevision(_dbConnection,_jobActionDict,_revisionDict):
	sql = "SELECT * FROM wf_field_revisions WHERE complete = 'f' and task_code = %s and job_action_id = %s and field_name = %s"
	args = (_revisionDict.get('task_code',''),_jobActionDict.get('id',-1),_revisionDict.get('fieldname',''))
	return _dbConnection.executeSQLQuery(sql,args)

def getFieldLevelRevisionsForJobAction(_dbConnection,_jobActionDict,_activeOnly):
	completionClause = ''
	if _activeOnly:
		completionClause = "complete = 'f' AND "
	sql = "SELECT * FROM wf_field_revisions WHERE " + completionClause + " job_action_id = %s ORDER BY when_notified"
	args = (_jobActionDict.get('id',-1),)
	return _dbConnection.executeSQLQuery(sql,args)

def getFieldLevelRevisionsReadyForDisplayForJobAction(_dbConnection,_jobActionDict):
	sql = "SELECT * FROM wf_field_revisions WHERE complete = 'f' AND when_notified <> '' AND job_action_id = %s ORDER BY when_notified"
	args = (_jobActionDict.get('id',-1),)
	return _dbConnection.executeSQLQuery(sql,args)

def getFieldLevelRevisionsReadyForNotificationForJobAction(_dbConnection,_jobActionDict):
	sql = "SELECT * FROM wf_field_revisions WHERE complete = 'f' AND when_notified = '' AND job_action_id = %s ORDER BY when_notified"
	args = (_jobActionDict.get('id',-1),)
	return _dbConnection.executeSQLQuery(sql,args)


def updateRevisionsAsSent(_dbConnection,_jobActionId,_now, _username,_doCommit):
	sql = "UPDATE wf_field_revisions SET when_notified = %s,who_notified = %s,lastuser = %s,updated = %s WHERE job_action_id = %s and when_notified = ''"
	args = (_now,_username,_username,_now,_jobActionId)
	_dbConnection.executeSQLCommand(sql,args,_doCommit)

def updateJobActionRevisionsRequired(_dbConnection,_jobActionId,_boolvalue,_now, _username,_doCommit):
	sql = "UPDATE wf_job_action SET field_revisions_required = %s,lastuser = %s,updated = %s WHERE id = %s"
	args = (_boolvalue,_username,_now,_jobActionId)
	_dbConnection.executeSQLCommand(sql,args,_doCommit)

def setRevisionsComplete(_dbConnection,_jobActionId,_taskCode,_now, _username,_doCommit):
	sql = '''UPDATE wf_field_revisions SET when_resolved = %s,who_resolved = %s,complete = 't',lastuser = %s,updated = %s WHERE
	      job_action_id = %s AND complete = 'f' AND task_code = %s'''
	args = (_now,_username,_username,_now,_jobActionId,_taskCode,)
	_dbConnection.executeSQLCommand(sql,args,_doCommit)

#   Single field revision required entry from Renee

def updateFieldLevelRevision(_dbConnection,_jobActionDict,_revisionDict,now,username,_doCommit=True):
	sql = '''UPDATE wf_field_revisions SET comment = %s,updated = %s,when_requested = %s,who_requested = %s
	WHERE complete = 'f' AND task_code = %s AND job_action_id = %s AND field_name = %s'''
	args = (_revisionDict.get('comment','',),
	        now,
	        now,
	        username,
	        _revisionDict.get('task_code',''),
	        _jobActionDict.get('id',-1),
	        _revisionDict.get('fieldname',''))
	_dbConnection.executeSQLCommand(sql,args,_doCommit)

def deleteFieldLevelRevision(_dbConnection,_jobActionDict,_revisionDict,_doCommit):
	sql = "DELETE FROM wf_field_revisions WHERE field_name = %s and task_code = %s and job_action_id = %s"
	args = (_revisionDict.get('fieldname',''),_revisionDict.get('task_code',''),_jobActionDict.get('id',-1))
	_dbConnection.executeSQLCommand(sql,args,_doCommit)

def createFieldLevelRevision(_dbConnection,_jobActionDict,_revisionDict,now,username,_doCommit):
	sql = '''INSERT INTO wf_field_revisions
	(job_action_id,task_code,field_name,comment,complete,who_requested,when_requested,
	who_notified,when_notified,who_resolved,when_resolved,created,updated,lastuser) VALUES
	(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_jobActionDict.get('id',-1),
	        _revisionDict.get('task_code',''),
	        _revisionDict.get('fieldname',''),
	        _revisionDict.get('comment',''),
	        False,
	        username,
	        now,
	        '',
	        '',
	        '',
	        '',
	        now,
	        now,
	        username)
	_dbConnection.executeSQLCommand(sql,args,_doCommit)

#   End single field revision required entry from Renee
