# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.constants as constants
import MPSAppt.services.lookupTableService as lookupTableSvc

def getBackgroundCheck(_dbConnection, _jobTaskId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_background_check', _jobTaskId, _key='job_task_id')

def findPending(_dbConnection):
	sql = '''SELECT DISTINCT JA.* FROM wf_background_check AS BC
				JOIN wf_job_task AS TASK JOIN wf_job_action AS JA ON TASK.job_action_id = JA.id ON BC.job_task_id = TASK.id
			WHERE BC.status IN ('%s','%s') AND JA.complete = 'f' AND JA.frozen = 'f' ORDER BY JA.id''' % \
		(constants.kBackgroundCheckStatusSubmitted, constants.kBackgroundCheckStatusInProgress)
	return _dbConnection.executeSQLQuery(sql)

def createBackgroundCheck(_dbConnection, _backgroundCheckDict, doCommit=True):
	sql = "INSERT INTO wf_background_check (job_task_id,external_key,submitted_date,submitted_error,status,status_date,flagged,report_url,report_content,completed_date,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (_backgroundCheckDict.get('job_task_id', -1),
			_backgroundCheckDict.get('external_key', ''),
			_backgroundCheckDict.get('submitted_date', ''),
			_backgroundCheckDict.get('submitted_error', ''),
			_backgroundCheckDict.get('status', constants.kBackgroundCheckStatusUnknown),
			_backgroundCheckDict.get('status_date', ''),
			_backgroundCheckDict.get('flagged', False),
			_backgroundCheckDict.get('report_url', ''),
			_backgroundCheckDict.get('report_content', None),
			_backgroundCheckDict.get('completed_date', ''),
			_backgroundCheckDict.get('created', ''),
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)


kSubmitWaiveSQL = '''UPDATE wf_background_check SET external_key=%s,submitted_date=%s,submitted_error=%s,status=%s,status_date=%s,flagged=%s,report_url=%s,report_content=%s,completed_date=%s,updated=%s,lastuser=%s WHERE id=%s'''
def enactSubmittedStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = (_backgroundCheckDict.get('external_key', ''),
			_backgroundCheckDict.get('submitted_date', ''),
			'',
			constants.kBackgroundCheckStatusSubmitted,
			_backgroundCheckDict.get('status_date', ''),
			False,
			'',
			None,
			'',
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kSubmitWaiveSQL, args, doCommit)

def enactSubmittedErrorStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			_backgroundCheckDict.get('submitted_date', ''),
			_backgroundCheckDict.get('submitted_error', ''),
			constants.kBackgroundCheckStatusSubmittedError,
			_backgroundCheckDict.get('status_date', ''),
			False,
			'',
			None,
			'',
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kSubmitWaiveSQL, args, doCommit)

def enactWaivedStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			'',
			'',
			constants.kBackgroundCheckStatusWaived,
			_backgroundCheckDict.get('status_date', ''),
			False,
			'',
			None,
			'',
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kSubmitWaiveSQL, args, doCommit)


kInProgressSQL = '''UPDATE wf_background_check SET submitted_error=%s,status=%s,status_date=%s,flagged=%s,completed_date=%s,updated=%s,lastuser=%s WHERE id=%s'''
def enactInProgressStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			constants.kBackgroundCheckStatusInProgress,
			_backgroundCheckDict.get('status_date', ''),
			False,
			'',
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kInProgressSQL, args, doCommit)

kCompleteSQL = '''UPDATE wf_background_check SET submitted_error=%s,status=%s,status_date=%s,flagged=%s,report_content=%s,completed_date=%s,updated=%s,lastuser=%s WHERE id=%s'''
def enactCompleteStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			constants.kBackgroundCheckStatusComplete,
			_backgroundCheckDict.get('status_date', ''),
			_backgroundCheckDict.get('flagged', False),
			_backgroundCheckDict.get('report_content', ''),
			_backgroundCheckDict.get('completed_date', ''),
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kCompleteSQL, args, doCommit)


kAcceptRejectSQL = '''UPDATE wf_background_check SET submitted_error=%s,status=%s,status_date=%s,updated=%s,lastuser=%s WHERE id=%s'''
def enactAcceptStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			constants.kBackgroundCheckStatusAccepted,
			_backgroundCheckDict.get('status_date', ''),
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kAcceptRejectSQL, args, doCommit)

def enactAcceptFindingsStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			constants.kBackgroundCheckStatusAcceptedWithFindings,
			_backgroundCheckDict.get('status_date', ''),
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kAcceptRejectSQL, args, doCommit)

def enactRejectedStatus(_dbConnection, _backgroundCheckDict, doCommit=True):
	args = ('',
			constants.kBackgroundCheckStatusRejected,
			_backgroundCheckDict.get('status_date', ''),
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(kAcceptRejectSQL, args, doCommit)


def updateReportURL(_dbConnection, _backgroundCheckDict, doCommit=True):
	sql = '''UPDATE wf_background_check SET report_url=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_backgroundCheckDict.get('report_url', ''),
			_backgroundCheckDict.get('updated', ''),
			_backgroundCheckDict.get('lastuser', ''),
			_backgroundCheckDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
