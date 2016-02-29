# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getServiceAndRank(_dbConnection, _jobTaskId):
	sql = "SELECT * FROM wf_service_rank WHERE job_task_id = %s"
	args = (_jobTaskId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	if qry:
		return qry[0]

def getBuildings(_dbConnection):
	sql = "SELECT * FROM wf_building ORDER BY UPPER(descr)"
	args = ()
	return _dbConnection.executeSQLQuery(sql,args)

def updateServiceAndRank(_dbConnection,_jobTaskDict, _serviceAndRankDict, doCommit=True):
	sql = '''UPDATE wf_service_rank SET building_descr = %s, room = %s,spc = %s,floor = %s,reception = %s,address_lines = %s,city = %s,
	state = %s,country = %s,postal = %s,phone = %s,fax = %s,email = %s,membership_category = %s,updated = %s,lastuser = %s WHERE job_task_id = %s'''
	args = (_serviceAndRankDict.get('building_descr',''),
	        _serviceAndRankDict.get('room',''),
	        _serviceAndRankDict.get('spc',''),
	        _serviceAndRankDict.get('floor',''),
	        _serviceAndRankDict.get('reception',''),
	        _serviceAndRankDict.get('address_lines',''),
	        _serviceAndRankDict.get('city',''),
	        _serviceAndRankDict.get('state',''),
	        _serviceAndRankDict.get('country',''),
	        _serviceAndRankDict.get('postal',''),
	        _serviceAndRankDict.get('phone',''),
	        _serviceAndRankDict.get('fax',''),
	        _serviceAndRankDict.get('email',''),
	        _serviceAndRankDict.get('membership_category',''),
	        _serviceAndRankDict.get('updated',''),
	        _serviceAndRankDict.get('lastuser',''),
			_jobTaskDict.get('id',-1),)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

def createServiceAndRank(_dbConnection,_jobTaskDict, _serviceAndRankDict, doCommit=True):
	sql = '''INSERT INTO wf_service_rank (job_task_id,building_descr,room,spc,floor,reception,address_lines,city,
	state,country,postal,phone,fax,email,membership_category,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_jobTaskDict.get('id',-1),
	        _serviceAndRankDict.get('building_descr',''),
	        _serviceAndRankDict.get('room',''),
	        _serviceAndRankDict.get('spc',''),
	        _serviceAndRankDict.get('floor',''),
	        _serviceAndRankDict.get('reception',''),
	        _serviceAndRankDict.get('address_lines',''),
	        _serviceAndRankDict.get('city',''),
	        _serviceAndRankDict.get('state',''),
	        _serviceAndRankDict.get('country',''),
	        _serviceAndRankDict.get('postal',''),
	        _serviceAndRankDict.get('phone',''),
	        _serviceAndRankDict.get('fax',''),
	        _serviceAndRankDict.get('email',''),
	        _serviceAndRankDict.get('membership_category',''),
	        _serviceAndRankDict.get('created',''),
	        _serviceAndRankDict.get('updated',''),
	        _serviceAndRankDict.get('lastuser',''),)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

