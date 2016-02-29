# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def createWorkflowComponent(connection,code,descr,component,isOverride,src,component_type_id,doCommit = True):
	sql = "INSERT INTO wf_component (code, descr, value, is_site_override,src,component_type_id) VALUES (%s,%s,%s,%s,%s,%s)"
	args = (code,descr,component,isOverride,src,component_type_id)
	connection.executeSQLCommand(sql,args,doCommit)

def createWorkflow(connection,code,descr,job_action_type_id,doCommit = True):
	sql = "INSERT INTO wf_workflow (code,descr,job_action_type_id) VALUES (%s,%s,%s)"
	args = (code,descr,job_action_type_id)
	connection.executeSQLCommand(sql,args,doCommit)

def updateComponentSrcAndValue(connection,src,value,code,doCommit = True):
	sql = "UPDATE wf_component set src = %s, value = %s WHERE code = %s"
	args = (src,value,code,)
	connection.executeSQLCommand(sql,args,doCommit)

def updateComponentCodeSrcAndValue(connection,newcode,src,value,code,doCommit = True):
	sql = "UPDATE wf_component set code = %s,src = %s, value = %s WHERE code = %s"
	args = (newcode,src,value,code,)
	connection.executeSQLCommand(sql,args,doCommit)

def getContainerJSON(connection,workflowCode):
	sql = "select value from wf_component where code = %s"
	args = (workflowCode,)
	return connection.executeSQLQuery(sql,args)

def getAllContainerRows(connection):
	sql = "select * from wf_component"
	return connection.executeSQLQuery(sql,())

def getAllContainerCodesAndDescriptions(connection):
	sql = "select wf_component.code,wf_component.descr,wf_component_type.descr as wftype from wf_component,wf_component_type where wf_component_type.id = component_type_id order by wf_component.code"
	return connection.executeSQLQuery(sql,())

def updateWorkflowCodeDescr(connection,oldcode,newcode,optionalDescr,doCommit = True):
	if optionalDescr:
		sql = "update wf_workflow set code = %s,descr = %s where code = %s"
		args = (newcode,optionalDescr,oldcode)
	else:
		sql = "update wf_workflow set code = %s where code = %s"
		args = (newcode,oldcode)
	connection.executeSQLCommand(sql,args)
