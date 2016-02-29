# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getUberQuestions(_dbConnection):
	sql = "SELECT * FROM wf_uber_question ORDER BY code"
	return _dbConnection.executeSQLQuery(sql)

def getUberOptions(_dbConnection):
	sql = "SELECT * FROM wf_uber_option ORDER BY uber_question_id, seq asc, code"
	return _dbConnection.executeSQLQuery(sql)

def getUberOptionsForQuestion(_dbConnection, _questionDict):
	sql = "SELECT * FROM wf_uber_option WHERE uber_question_id = %s ORDER BY seq asc, code"
	return _dbConnection.executeSQLQuery(sql, (_questionDict.get('id', 0),))

def getUberGroups(_dbConnection):
	sql = "SELECT * FROM wf_uber_group ORDER BY code"
	return _dbConnection.executeSQLQuery(sql)

def createUber(_dbConnection, _uberDict, doCommit=True):
	sql = '''INSERT INTO wf_uber (job_task_id,uber_question_json,complete,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s)'''
	args = (_uberDict.get('job_task_id', None),
			_uberDict.get('uber_question_json', None),
			_uberDict.get('complete', None),
			_uberDict.get('created', None),
			_uberDict.get('updated', None),
			_uberDict.get('lastuser', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateUberJson(_dbConnection, _uberDict, doCommit=True):
	sql = '''UPDATE wf_uber SET uber_question_json=%s,updated=%s,lastuser=%s WHERE job_task_id=%s'''
	args = (_uberDict.get('uber_question_json', None),
			_uberDict.get('updated', None),
			_uberDict.get('lastuser', None),
			_uberDict.get('job_task_id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateUberComplete(_dbConnection, _uberDict, doCommit=True):
	sql = '''UPDATE wf_uber SET complete=%s,updated=%s,lastuser=%s WHERE job_task_id=%s'''
	args = (_uberDict.get('complete', None),
			_uberDict.get('updated', None),
			_uberDict.get('lastuser', None),
			_uberDict.get('job_task_id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createUberResponse(_dbConnection, _uberResponseDict, doCommit=True):
	sql = '''INSERT INTO wf_uber_response (job_task_id,question_code,repeat_seq,response,revisions_required,revisions_required_date,revisions_required_comment,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_uberResponseDict.get('job_task_id', None),
			_uberResponseDict.get('question_code', None),
			_uberResponseDict.get('repeat_seq', None),
			_uberResponseDict.get('response', None),
			_uberResponseDict.get('revisions_required', False),
			_uberResponseDict.get('revisions_required_date', ''),
			_uberResponseDict.get('revisions_required_comment', ''),
			_uberResponseDict.get('created', None),
			_uberResponseDict.get('updated', None),
			_uberResponseDict.get('lastuser', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateUberResponse(_dbConnection, _uberResponseDict, doCommit=True):
	sql = '''UPDATE wf_uber_response SET response=%s,revisions_required=%s,revisions_required_date=%s,revisions_required_comment=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_uberResponseDict.get('response', None),
			_uberResponseDict.get('revisions_required', False),
			_uberResponseDict.get('revisions_required_date', ''),
			_uberResponseDict.get('revisions_required_comment', ''),
			_uberResponseDict.get('updated', None),
			_uberResponseDict.get('lastuser', None),
			_uberResponseDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteUberResponse(_dbConnection, _uberResponseDict, doCommit=True):
	sql = '''DELETE FROM wf_uber_response WHERE id=%s'''
	args = (_uberResponseDict.get('id', None),)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteUberResponsesForTask(_dbConnection, _jobTaskDict, doCommit=True):
	sql = '''DELETE FROM wf_uber_response WHERE job_task_id=%s'''
	args = (_jobTaskDict.get('id', None),)
	_dbConnection.executeSQLCommand(sql, args, doCommit)


#   Uber Saved Sets.

def getUberSavedSetNames(_dbConnection, _community, _username, _uberGroupCode):
	sql = []
	args = []
	sql.append("SELECT * FROM wf_uber_saved_set WHERE (group_code=%s) AND (community=%s) AND (username=''")
	args.append(_uberGroupCode)
	args.append(_community)
	if _username:
		sql.append(" OR username=%s")
		args.append(_username)
	sql.append(") ORDER BY descr ASC")
	return _dbConnection.executeSQLQuery(''.join(sql), tuple(args))

def matchUberSavedSetByDescr(_dbConnection, _community, _username, _descr):
	sql = '''SELECT * FROM wf_uber_saved_set WHERE community=%s AND username=%s AND lower(descr)=%s'''
	args = (_community, _username, _descr.strip().lower())
	return _dbConnection.executeSQLQuery(sql, args)

def getUberSavedSet(_dbConnection, _uberGroupId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_uber_saved_set', _uberGroupId, _key='id')

def getUberSavedSetItemsForSavedSetId(_dbConnection, _uberSavedSetId):
	return lookupTableSvc.getEntityListByKey(_dbConnection, 'wf_uber_saved_set_item', _uberSavedSetId, _key='saved_set_id')

def createUberSavedSet(_dbConnection, _uberSavedSetDict, doCommit=True):
	sql = '''INSERT INTO wf_uber_saved_set (community,username,group_code,descr,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
	args = (_uberSavedSetDict.get('community', 'default'),
			_uberSavedSetDict.get('username', None),
			_uberSavedSetDict.get('group_code', None),
			_uberSavedSetDict.get('descr', '').strip(),
			_uberSavedSetDict.get('created', None),
			_uberSavedSetDict.get('updated', None),
			_uberSavedSetDict.get('lastuser', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
	return _dbConnection.getLastSequenceNbr('wf_uber_saved_set')

def deleteUberSavedSet(_dbConnection, _uberSavedSetId, doCommit=True):
	sql = '''DELETE FROM wf_uber_saved_set WHERE id=%s'''
	args = (_uberSavedSetId,)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createUberSavedSetItem(_dbConnection, _uberSavedSetItemDict, doCommit=True):
	sql = '''INSERT INTO wf_uber_saved_set_item (saved_set_id,question_code,repeat_seq,response,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
	args = (_uberSavedSetItemDict.get('saved_set_id', None),
			_uberSavedSetItemDict.get('question_code', None),
			_uberSavedSetItemDict.get('repeat_seq', None),
			_uberSavedSetItemDict.get('response', None),
			_uberSavedSetItemDict.get('created', None),
			_uberSavedSetItemDict.get('updated', None),
			_uberSavedSetItemDict.get('lastuser', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteUberSavedSetItemsForSavedSetId(_dbConnection, _uberSavedSetId, doCommit=True):
	sql = '''DELETE FROM wf_uber_saved_set_item WHERE saved_set_id=%s'''
	args = (_uberSavedSetId,)
	_dbConnection.executeSQLCommand(sql, args, doCommit)


	#   Admin.

def createQuestion(_dbConnection, _questionDict, doCommit=True):
	sql = '''INSERT INTO wf_uber_question (code,descr,display_text,header_text,cols_offset,cols_label,cols_prompt,required,wrap,encrypt,data_type,data_type_attributes,job_action_types,identifier_code,show_codes,hide_codes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_questionDict.get('code', None),
			_questionDict.get('descr', None),
			_questionDict.get('display_text', None),
			_questionDict.get('header_text', None),
			_questionDict.get('cols_offset', None),
			_questionDict.get('cols_label', None),
			_questionDict.get('cols_prompt', None),
			_questionDict.get('required', None),
			_questionDict.get('wrap', None),
			_questionDict.get('encrypt', None),
			_questionDict.get('data_type', None),
			_questionDict.get('data_type_attributes', None),
			_questionDict.get('job_action_types', None),
			_questionDict.get('identifier_code', None),
			_questionDict.get('show_codes', None),
			_questionDict.get('hide_codes', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateQuestion(_dbConnection, _questionDict, doCommit=True):
	sql = '''UPDATE wf_uber_question SET code=%s,descr=%s,display_text=%s,header_text=%s,cols_offset=%s,cols_label=%s,cols_prompt=%s,required=%s,wrap=%s,encrypt=%s,data_type=%s,data_type_attributes=%s,job_action_types=%s,identifier_code=%s,show_codes=%s,hide_codes=%s WHERE id=%s'''
	args = (_questionDict.get('code', None),
			_questionDict.get('descr', None),
			_questionDict.get('display_text', None),
			_questionDict.get('header_text', None),
			_questionDict.get('cols_offset', None),
			_questionDict.get('cols_label', None),
			_questionDict.get('cols_prompt', None),
			_questionDict.get('required', None),
			_questionDict.get('wrap', None),
			_questionDict.get('encrypt', None),
			_questionDict.get('data_type', None),
			_questionDict.get('data_type_attributes', None),
			_questionDict.get('job_action_types', None),
			_questionDict.get('identifier_code', None),
			_questionDict.get('show_codes', None),
			_questionDict.get('hide_codes', None),
			_questionDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def removeUberOptionsForQuestion(_dbConnection, _questionDict, doCommit=True):
	sql = "DELETE FROM wf_uber_option WHERE uber_question_id = %s"
	_dbConnection.executeSQLCommand(sql, (_questionDict.get('id', 0),), doCommit)

def createOption(_dbConnection, _optionDict, doCommit=True):
	sql = '''INSERT INTO wf_uber_option (uber_question_id,code,descr,display_text,seq,show_codes,hide_codes) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
	args = (_optionDict.get('uber_question_id', None),
			_optionDict.get('code', None),
			_optionDict.get('descr', None),
			_optionDict.get('display_text', None),
			_optionDict.get('seq', None),
			_optionDict.get('show_codes', None),
			_optionDict.get('hide_codes', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createGroup(_dbConnection, _groupDict, doCommit=True):
	sql = '''INSERT INTO wf_uber_group (code,descr,display_text,cols_offset,cols_label,repeating,repeating_table,required,wrap,filler,children) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_groupDict.get('code', None),
			_groupDict.get('descr', None),
			_groupDict.get('display_text', None),
			_groupDict.get('cols_offset', None),
			_groupDict.get('cols_label', None),
			_groupDict.get('repeating', None),
			_groupDict.get('repeating_table', None),
			_groupDict.get('required', None),
			_groupDict.get('wrap', None),
			_groupDict.get('filler', None),
			_groupDict.get('children', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateGroup(_dbConnection, _groupDict, doCommit=True):
	sql = '''UPDATE wf_uber_group SET code=%s,descr=%s,display_text=%s,cols_offset=%s,cols_label=%s,repeating=%s,repeating_table=%s,required=%s,wrap=%s,filler=%s,children=%s WHERE id=%s'''
	args = (_groupDict.get('code', None),
			_groupDict.get('descr', None),
			_groupDict.get('display_text', None),
			_groupDict.get('cols_offset', None),
			_groupDict.get('cols_label', None),
			_groupDict.get('repeating', None),
			_groupDict.get('repeating_table', None),
			_groupDict.get('required', None),
			_groupDict.get('wrap', None),
			_groupDict.get('filler', None),
			_groupDict.get('children', None),
			_groupDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
