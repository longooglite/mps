# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getActivityLogsForJobAction(_dbConnection, _jobActionId):
	sql = '''SELECT LOG.id AS log_id, LOG.job_action_id, LOG.job_task_id, TASK.task_code, LOG.activity, LOG.created AS log_created, LOG.lastuser AS log_lastuser, CMT.id AS comment_id, CMT.comment_code, CMT.comment, CMT.created AS comment_created, CMT.lastuser AS comment_lastuser
			FROM wf_activity_log AS LOG
				LEFT OUTER JOIN wf_comment AS CMT ON CMT.activity_log_id = LOG.id
				JOIN wf_job_task AS TASK ON LOG.job_task_id = TASK.id
			WHERE (LOG.job_action_id = %s) OR
				(TASK.id IN (SELECT primary_job_task_id FROM wf_job_task AS TASK2 WHERE (TASK2.job_action_id = %s) AND (TASK2.primary_job_task_id IS NOT NULL)))
			ORDER BY LOG.created DESC, TASK.task_code, CMT.id'''
	return _dbConnection.executeSQLQuery(sql, (_jobActionId, _jobActionId))

def createActivityLog(_dbConnection, logDict, doCommit=True):
	sql = '''INSERT INTO wf_activity_log (job_action_id,job_task_id,activity,created,lastuser) VALUES (%s,%s,%s,%s,%s);'''
	args = (logDict.get('job_action_id',None),
			logDict.get('job_task_id',None),
			logDict.get('activity',''),
			logDict.get('created',''),
			logDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createCommentLog(_dbConnection, logDict, doCommit=True):
	sql = '''INSERT INTO wf_comment (activity_log_id,comment_code,comment,created,lastuser) VALUES (%s,%s,%s,%s,%s);'''
	args = (logDict.get('activity_log_id',None),
			logDict.get('comment_code',None),
			logDict.get('comment',''),
			logDict.get('created',''),
			logDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
