# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getAllEvaluators(_dbConnection, _includeInactive=True):
	sql = []
	sql.append("SELECT * FROM wf_internal_evaluator")
	if not _includeInactive:
		sql.append("WHERE active = 't'")
	sql.append("ORDER BY UPPER(last_name),UPPER(first_name),UPPER(email_address)")
	return _dbConnection.executeSQLQuery(' '.join(sql))

def getEvaluator(_connection, _evaluatorId):
	sql = "SELECT * FROM wf_internal_evaluator WHERE id=%s"
	args = (_evaluatorId,)
	qry = _connection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def createEvaluator(_dbConnection, _evaluatorDict, doCommit=True):
	sql = '''INSERT INTO wf_internal_evaluator (first_name,last_name,email_address,active) VALUES (%s,%s,%s,%s)'''
	args = (_evaluatorDict.get('first_name', None),
			_evaluatorDict.get('last_name', None),
			_evaluatorDict.get('email_address', None),
			_evaluatorDict.get('active', None),)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateEvaluator(_dbConnection, _evaluatorDict, doCommit=True):
	sql = '''UPDATE wf_internal_evaluator SET first_name=%s,last_name=%s,email_address=%s,active=%s WHERE id=%s'''
	args = (_evaluatorDict.get('first_name', None),
			_evaluatorDict.get('last_name', None),
			_evaluatorDict.get('email_address', None),
			_evaluatorDict.get('active', None),
	        _evaluatorDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
