# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   Components

def createComponent(_dbConnection, _componentDict, doCommit=True):
	sql = '''INSERT INTO wf_component (code,descr,component_type_id,is_site_override,src,value,car_relative_path) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
	args = (_componentDict.get('code', None),
			_componentDict.get('descr', None),
			_componentDict.get('component_type_id', None),
			_componentDict.get('is_site_override', None),
			_componentDict.get('src', None),
			_componentDict.get('value', None),
			_componentDict.get('car_relative_path', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateComponent(_dbConnection, _componentDict, doCommit=True):
	sql = '''UPDATE wf_component SET code=%s,descr=%s,component_type_id=%s,is_site_override=%s,src=%s,value=%s,car_relative_path=%s WHERE id=%s'''
	args = (_componentDict.get('code', None),
			_componentDict.get('descr', None),
			_componentDict.get('component_type_id', None),
			_componentDict.get('is_site_override', None),
			_componentDict.get('src', None),
			_componentDict.get('value', None),
			_componentDict.get('car_relative_path', None),
			_componentDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteComponent(_dbConnection, _componentId, doCommit=True):
	sql = '''DELETE FROM wf_component WHERE id=%s'''
	_dbConnection.executeSQLCommand(sql, (_componentId,), doCommit)

def createComponentOverride(_dbConnection, _overrideDict, doCommit=True):
	sql = '''INSERT INTO wf_component_override (workflow_code,component_code,title_code,value) VALUES (%s,%s,%s,%s)'''
	args = (_overrideDict.get('workflow_code', None),
			_overrideDict.get('component_code', None),
			_overrideDict.get('title_code', None),
			_overrideDict.get('value', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteComponentOverride(_dbConnection, _componentOverrideId, doCommit=True):
	sql = '''DELETE FROM wf_component_override WHERE id=%s'''
	_dbConnection.executeSQLCommand(sql, (_componentOverrideId,), doCommit)

def updateComponentOverride(_dbConnection, _overrideDict, doCommit=True):
	sql = '''UPDATE wf_component_override SET value=%s WHERE id=%s'''
	args = (_overrideDict.get('value', None),
			_overrideDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

#   Workflows

def createWorkflow(_dbConnection, _workflowDict, doCommit=True):
	sql = '''INSERT INTO wf_workflow (code,descr,job_action_type_id) VALUES (%s,%s,%s)'''
	args = (_workflowDict.get('code', None),
			_workflowDict.get('descr', None),
			_workflowDict.get('job_action_type_id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateWorkflow(_dbConnection, _workflowDict, doCommit=True):
	sql = '''UPDATE wf_workflow SET code=%s,descr=%s,job_action_type_id=%s WHERE id=%s'''
	args = (_workflowDict.get('code', None),
			_workflowDict.get('descr', None),
			_workflowDict.get('job_action_type_id', None),
			_workflowDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
