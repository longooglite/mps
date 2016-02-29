# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils

def dashboardExists(connection, _code, _jobActionId):
	sql = '''SELECT count(*) AS count FROM wf_dashboard WHERE code = %s AND job_action_id = %s AND active = 't' '''
	return connection.executeSQLQuery(sql, (_code, _jobActionId))[0]['count']

def createDashboard(connection, _jobActionId, _department_id, _code, _description, _permisssionsList, _sortOrder, _now, _lastuser, doCommit=True):
	sql = '''INSERT INTO wf_dashboard (code,description,active,job_action_id,department_id,view_permission,sort_order,created,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_code, _description, True, _jobActionId,_department_id, _permisssionsList, _sortOrder, _now, _lastuser)
	connection.executeSQLCommand(sql, args, doCommit)

def removeDashoardEvent(connection, _code, _jobActionId, doCommit=True):
	sql = '''UPDATE wf_dashboard SET active = 'f' WHERE code = %s AND job_action_id = %s'''
	connection.executeSQLCommand(sql, (_code, _jobActionId), doCommit)

def removeAllDashoardEvents(connection, _jobActionId, doCommit=True):
	sql = '''UPDATE wf_dashboard SET active = 'f' WHERE job_action_id = %s'''
	connection.executeSQLCommand(sql, (_jobActionId,), doCommit)

kDashTableAlias = 'DASH'
kJobActionTableAlias = 'JA'
kAppointmentTableAlias = 'APPT'
kPositionTableAlias = 'POS'
kPersonTableAlias = 'PERS'

kDashPrefix = 'dash_'
kJobActionPrefix = 'ja_'
kAppointmentPrefix = 'appt_'
kPositionPrefix = 'pos_'
kPersonPrefix = 'pers_'

kDashTableColumns = ['id','code','description','active','job_action_id','department_id','view_permission','sort_order','created','lastuser']
kJobActionTableColumns = ['id','person_id','position_id','appointment_id','current_status','workflow_id','workflow_json','complete','frozen','revisions_required','created','updated','completed','lastuser']
kAppointmentTableColumns = ['id','person_id','title_id','position_id','start_date','end_date','appointment_status_id','created','updated','lastuser']
kPositionTableColumns = ['id','department_id','title_id','pcn','is_primary','created','updated','lastuser']
kPersonTableColumns = ['id','username','first_name','middle_name','last_name','suffix','email','employee_nbr','created','updated','lastuser']

def formatColumnList(_alias, _prefix, _columnList):
	parts = []
	for columnName in _columnList:
		parts.append("%s.%s AS %s%s" % (_alias, columnName, _prefix, columnName))
	return ','.join(parts)

selectParts = []
selectParts.append(formatColumnList(kDashTableAlias, kDashPrefix, kDashTableColumns))
selectParts.append(formatColumnList(kJobActionTableAlias, kJobActionPrefix, kJobActionTableColumns))
selectParts.append(formatColumnList(kAppointmentTableAlias, kAppointmentPrefix, kAppointmentTableColumns))
selectParts.append(formatColumnList(kPositionTableAlias, kPositionPrefix, kPositionTableColumns))
selectParts.append(formatColumnList(kPersonTableAlias, kPersonPrefix, kPersonTableColumns))
selectColumns = ','.join(selectParts)

queryParts = ["SELECT"]
queryParts.append(selectColumns)
queryParts.append("FROM wf_dashboard AS %s" % kDashTableAlias)
queryParts.append("JOIN wf_job_action AS %s" % kJobActionTableAlias)
queryParts.append("JOIN wf_appointment AS %s ON %s.appointment_id = %s.id" % (kAppointmentTableAlias, kJobActionTableAlias, kAppointmentTableAlias))
queryParts.append("JOIN wf_position AS %s ON %s.position_id = %s.id" % (kPositionTableAlias, kJobActionTableAlias, kPositionTableAlias))
queryParts.append("LEFT OUTER JOIN wf_person AS %s ON %s.person_id = %s.id" % (kPersonTableAlias, kJobActionTableAlias, kPersonTableAlias))
queryParts.append("ON %s.job_action_id = %s.id" % (kDashTableAlias, kJobActionTableAlias))
queryParts.append("WHERE %s.active = 't'" % kDashTableAlias)
queryParts.append("AND %s.department_id IN" % kDashTableAlias)
queryParts.append("%s")
queryParts.append("ORDER BY %s.sort_order ASC, %s.code ASC, %s.created DESC" % (kDashTableAlias, kDashTableAlias, kDashTableAlias))
dashboardQuery = ' '.join(queryParts)

def getActiveDashboardItemsRestrictedByDepartment(connection, userdepartmentList):
	deptInClause = stringUtils.getSQLInClause(userdepartmentList,False)
	if not deptInClause:
		return []
	sqlQuery = dashboardQuery % (deptInClause)
	return connection.executeSQLQuery(sqlQuery)
