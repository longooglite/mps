# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils

def getComponents(_dbConnection):
	sql = "SELECT code,is_site_override,descr,value FROM wf_component ORDER BY code,is_site_override asc"
	return _dbConnection.executeSQLQuery(sql)

def getComponentByCode(_dbConnection, _componentCode):
	sql = "SELECT * FROM wf_component WHERE code = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_componentCode,))
	return qry[0] if qry else None

def getTitleOverrides(_dbConnection,workflowCode,titleCode):
	sql = "SELECT workflow_code,component_code,value FROM wf_component_override WHERE title_code = %s and (workflow_code = %s or workflow_code = '') ORDER BY workflow_code"
	args = (titleCode,workflowCode,)
	return _dbConnection.executeSQLQuery(sql, args)

def getTitleOverrideForWorkflowComponentTitle(_dbConnection, _workflowCode, _titleCode, _componentCode):
	sql = "SELECT * FROM wf_component_override WHERE workflow_code = %s AND title_code = %s and component_code = %s"
	args = (_workflowCode, _titleCode, _componentCode)
	qry = _dbConnection.executeSQLQuery(sql, args)
	return qry[0] if qry else None

def getWorkflow(_dbConnection,_workflowCode):
	sql = "SELECT * FROM wf_workflow WHERE code = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_workflowCode,))
	return qry[0] if qry else None

def getWorkflowById(_dbConnection,_workflowId):
	sql = "SELECT * FROM wf_workflow WHERE id = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_workflowId,))
	return qry[0] if qry else None

def getWorkflows(_dbConnection):
	sql = "SELECT * FROM wf_workflow ORDER BY descr, code, id"
	return _dbConnection.executeSQLQuery(sql)

def getWorkflowEntriesForMetatackAndJAType(_dbConnection,_metatrackId,_jobActionTypeList):
	sql = '''SELECT wf.id,wf.code,wf.descr FROM wf_workflow wf, wf_job_action_type jatype, wf_workflow_metatrack wfmt
	WHERE wfmt.workflow_id = wf.id AND
	wf.job_action_type_id = jatype.id
	AND jatype.code IN %s''' % (stringUtils.getSQLInClause(_jobActionTypeList))
	sql += ''' AND
	wfmt.metatrack_id = %s ORDER BY wf.descr'''
	return _dbConnection.executeSQLQuery(sql, (_metatrackId,))

def getWorkflowEntriesForJATypes(_dbConnection,_jobActionTypeList):
	sql = '''SELECT wf.id,wf.code,wf.descr,jatype.code AS jatypecode FROM wf_workflow wf, wf_job_action_type jatype
		WHERE wf.job_action_type_id = jatype.id
		AND jatype.active = 't' AND jatype.code IN %s''' % (stringUtils.getSQLInClause(_jobActionTypeList))
	sql += ''' ORDER BY wf.descr'''
	return _dbConnection.executeSQLQuery(sql, ())