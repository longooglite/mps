# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils

def persistReport(_dbConnection,_community,_username,_reportname,_srcFile,_parameters,_content,_date_created,_file_type):
	sql = '''INSERT INTO wf_reporting (community,username,report_name,src_file,parameters,content,date_created,file_type,date_read) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_community,_username,_reportname,_srcFile,_parameters,_content,_date_created,_file_type,'')
	_dbConnection.executeSQLCommand(sql,args)

def getReportsForUser(_dbConnection, _community, _username):
	sql = "SELECT id,community,username,report_name,src_file,parameters,date_created,file_type,date_read FROM wf_reporting WHERE community = %s AND username = %s ORDER BY id DESC"
	args = (_community, _username,)
	return _dbConnection.executeSQLQuery(sql,args)

def getNbrUnreadReportsForUser(_dbConnection, _communty, _username):
	sql = "SELECT count(*) as count FROM wf_reporting WHERE community = %s AND username = %s and date_read = ''"
	args = (_communty, _username)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return 0 if not qry else qry[0]['count']

def getReportContentForUser(_dbConnection, _community, _username, _reportId):
	#   match on user as well as id to ensure only this user can see this report
	sql = "SELECT * FROM wf_reporting WHERE community = %s AND username = %s and id = %s"
	args = (_community, _username,_reportId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def deleteReport(_dbConnection, _reportId, doCommit=True):
	sql = '''DELETE FROM wf_reporting WHERE id=%s'''
	args = (_reportId,)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getReportsCreatedBefore(_dbConnection, _beforeDateStr):
	sql = '''SELECT id,community,username,report_name FROM wf_reporting WHERE date_created < %s'''
	return _dbConnection.executeSQLQuery(sql, (_beforeDateStr,))

def markAsRead(_dbConnection,_reportId,_now):
	sql = "UPDATE wf_reporting SET date_read = %s WHERE id = %s"
	args = (_now,_reportId)
	_dbConnection.executeSQLCommand(sql,args)

#   Reporting Data

def getItemData(_dbConnection,_itemCodes,_beginDateStr,_endDateStr,itemTableName):
	itemInClause = stringUtils.getSQLInClause(_itemCodes)
	sql = '''SELECT * FROM wf_job_task,%s
	WHERE %s.job_task_id = wf_job_task.id
	AND task_code IN%s
	AND wf_job_task.job_action_id IN
	(SELECT id FROM wf_job_action WHERE complete = 't' AND updated BETWEEN '%s' AND '%s') ORDER BY task_code,wf_job_task.id ''' % (itemTableName,itemTableName,itemInClause,_beginDateStr,_endDateStr)
	args = ()
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry


