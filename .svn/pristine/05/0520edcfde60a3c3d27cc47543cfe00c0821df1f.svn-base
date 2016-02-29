# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getConfirmedTitle(_dbConnection, _jobTaskId):
	sql = "SELECT wf_confirmed_title.id,wf_confirmed_title.job_task_id,wf_confirmed_title.department_id,wf_confirmed_title.title_id," \
	      "wf_confirmed_title.created,wf_confirmed_title.updated,wf_confirmed_title.lastuser," \
	      "wf_title.code,wf_title.descr,wf_title.isactionable " \
	      "FROM wf_confirmed_title,wf_title WHERE " \
	      "wf_title.id = wf_confirmed_title.title_id " \
	      "AND wf_confirmed_title.job_task_id = %s"
	args = (_jobTaskId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	if qry:
		return qry[0]

def createConfirmedTitle(_dbConnection, _confirmedTitleDict, doCommit):
	sql = '''INSERT INTO wf_confirmed_title (job_task_id,title_id,department_id,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s);'''
	args = (_confirmedTitleDict.get('job_task_id',None),
			_confirmedTitleDict.get('title_id',None),
			_confirmedTitleDict.get('department_id',None),
			_confirmedTitleDict.get('created',''),
			_confirmedTitleDict.get('updated',''),
			_confirmedTitleDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateConfirmedTitle(_dbConnection, _confirmedTitleDict, doCommit=False):
	sql = '''UPDATE wf_confirmed_title SET title_id=%s,department_id=%s,updated=%s,lastuser=%s WHERE job_task_id=%s;'''
	args = (_confirmedTitleDict.get('title_id',0),
	        _confirmedTitleDict.get('department_id',None),
			_confirmedTitleDict.get('updated',''),
			_confirmedTitleDict.get('lastuser',''),
			_confirmedTitleDict.get('job_task_id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteConfirmedTitle(_dbConnection,confirmedTitleId):
	sql = "DELETE FROM wf_confirmed_title WHERE id = %s"
	args = (confirmedTitleId,)
	_dbConnection.executeSQLCommand(sql,args)