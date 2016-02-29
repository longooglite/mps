# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getLookupTable(_dbConnection, _tableName, _orderBy='code'):
	sql = '''SELECT * FROM %s ORDER BY %s''' % (_tableName, _orderBy)
	return _dbConnection.executeSQLQuery(sql)

def getEntityByKey(_dbConnection, _tableName, _keyValue, _key):
	resultList = getEntityListByKey(_dbConnection, _tableName, _keyValue, _key)
	if len(resultList) != 1:
		return None
	return resultList[0]

def getEntityListByKey(_dbConnection, _tableName, _keyValue, _key, _orderBy=None):
	sql = "SELECT * FROM %s WHERE %s = " % (_tableName, _key)
	sql += "%s"
	if _orderBy:
		sql += " ORDER BY "
		sql += _orderBy
	return _dbConnection.executeSQLQuery(sql, (_keyValue,))

def getStaticLookupDiscreteValue(_dbConnection, _lookupKey, _code, _keyCol):
	sql = "SELECT * FROM cv_static_lookup WHERE lookup_key = %s AND " +  _keyCol + " = %s"
	args = (_lookupKey, _code)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry[0] if qry else None


def workflowMetatrackExists(_dbConnection, _workflow_id, _metatrack_id):
	whereClause = '''workflow_id = %i and metatrack_id = %i''' % (_workflow_id, _metatrack_id)
	return _dbConnection.getRowCount('wf_workflow_metatrack', _whereClause=whereClause)

def getCodeDescrListByKey(_dbConnection, _tableName, _keyValue, _key, _code, _descr ):
	sql = "SELECT %s,%s FROM %s WHERE %s = '%s' ORDER BY UPPER(%s)" % (_code,_descr,_tableName, _key,_keyValue,_descr)
	return _dbConnection.executeSQLQuery(sql, ())

def getAllStaticLookupData(_dbConnection):
	sql = "SELECT * FROM cv_static_lookup ORDER BY lookup_key, seq, code, id"
	return _dbConnection.executeSQLQuery(sql)

def addStaticItem(_dbConnection, _itemDict, doCommit=True):
	sql = '''INSERT INTO cv_static_lookup (lookup_key,code,descr,alt_descr,seq) VALUES (%s,%s,%s,%s,%s)'''
	args = (_itemDict.get('lookup_key',None),
			_itemDict.get('code',None),
			_itemDict.get('descr',None),
			_itemDict.get('alt_descr',None),
			_itemDict.get('seq',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateStaticItem(_dbConnection, _itemDict, doCommit=True):
	sql = '''UPDATE cv_static_lookup SET lookup_key=%s,code=%s,descr=%s,alt_descr=%s,seq=%s WHERE id=%s'''
	args = (_itemDict.get('lookup_key',None),
			_itemDict.get('code',None),
			_itemDict.get('descr',None),
			_itemDict.get('alt_descr',None),
			_itemDict.get('seq',None),
			_itemDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateStaticItemSequence(_dbConnection, _itemDict, doCommit=True):
	sql = '''UPDATE cv_static_lookup SET seq=%s WHERE id=%s'''
	args = (_itemDict.get('seq',None), _itemDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
