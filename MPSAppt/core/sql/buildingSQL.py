# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getAllBuildings(_dbConnection, _includeInactive=True, _orderByDescr=False):
	sql = []
	sql.append("SELECT * FROM wf_building")
	if not _includeInactive:
		sql.append("WHERE active = 't'")
	if _orderByDescr:
		sql.append("ORDER BY UPPER(descr)")
	else:
		sql.append("ORDER BY code")
	return _dbConnection.executeSQLQuery(' '.join(sql))

def getBuilding(_connection, _buildingId):
	sql = "SELECT * FROM wf_building WHERE id=%s"
	args = (_buildingId,)
	qry = _connection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def createBuilding(_dbConnection, _buildingDict, doCommit=True):
	sql = '''INSERT INTO wf_building (code,descr,active,address_lines,city,state,country,postal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_buildingDict.get('code', None),
			_buildingDict.get('descr', None),
			_buildingDict.get('active', None),
			_buildingDict.get('address_lines', None),
			_buildingDict.get('city', None),
			_buildingDict.get('state', None),
			_buildingDict.get('country', None),
			_buildingDict.get('postal', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateBuilding(_dbConnection, _buildingDict, doCommit=True):
	sql = '''UPDATE wf_building SET code=%s,descr=%s,active=%s,address_lines=%s,city=%s,state=%s,country=%s,postal=%s WHERE id=%s'''
	args = (_buildingDict.get('code', None),
			_buildingDict.get('descr', None),
			_buildingDict.get('active', None),
			_buildingDict.get('address_lines', None),
			_buildingDict.get('city', None),
			_buildingDict.get('state', None),
			_buildingDict.get('country', None),
			_buildingDict.get('postal', None),
			_buildingDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
