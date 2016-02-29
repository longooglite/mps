# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def createPosition(_dbConnection, _positionDict, doCommit=True):
	sql = '''INSERT INTO wf_position (department_id,title_id,pcn,is_primary,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
	args = (_positionDict.get('department_id', None),
		_positionDict.get('title_id', None),
		_positionDict.get('pcn', None),
		_positionDict.get('is_primary', True),
		_positionDict.get('created', None),
		_positionDict.get('updated', None),
		_positionDict.get('lastuser', None)
	)
	_dbConnection.executeSQLCommand(sql, args, doCommit)
	return _dbConnection.getLastSequenceNbr('wf_position')

def deletePosition(_dbConnection,_pcnId):
	sql = "DELETE FROM wf_position WHERE id = %s"
	args = (_pcnId,)
	_dbConnection.executeSQLCommand(sql,args)

def getPcn(_dbConnection, _pcnId):
	sql = '''SELECT * FROM wf_pcn WHERE id = %s'''
	args = (_pcnId,)
	return _dbConnection.executeSQLQuery(sql, args)

def updatePcnSequence(_dbConnection, _pcnDict, doCommit=True):
	sql = '''UPDATE wf_pcn SET seq = %s WHERE id = %s'''
	args = (_pcnDict.get('seq', None), _pcnDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getPostionById(_dbConnection, _id):
	sql = "SELECT * FROM wf_position WHERE id = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_id,))
	return qry[0] if qry else None

def getPostionFromPCN(_dbConnection, _pcn):
	sql = "SELECT * FROM wf_position WHERE pcn = %s"
	return _dbConnection.executeSQLQuery(sql, (_pcn,))

def getPositionsForDepartment(_dbConnection,_departmentId):
	sql = "SELECT * FROM wf_position WHERE department_id = %s order by pcn"
	args = (_departmentId,)
	return _dbConnection.executeSQLQuery(sql,args)

def getDepartment(_dbConnection,departmentId):
	sql = 'SELECT * FROM wf_department WHERE id = %s'
	departmentList =  _dbConnection.executeSQLQuery(sql,(departmentId,))
	if departmentList:
		return departmentList[0]
	return {}

def updateTitle(_dbConnection, _positionDict, doCommit=True):
	positionId = _positionDict.get('id',None)
	titleId = _positionDict.get('title_id',None)
	updated = _positionDict.get('updated', None)
	lastuser = _positionDict.get('lastuser', None)

	sql = '''UPDATE wf_position SET title_id=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (titleId, updated, lastuser, positionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updatePrimaryStatus(_dbConnection,_positionDict,_isPrimary):
	sql = "UPDATE wf_position set is_primary = %s WHERE id = %s"
	args = (_isPrimary,_positionDict.get('id',-1),)
	_dbConnection.executeSQLCommand(sql,args)