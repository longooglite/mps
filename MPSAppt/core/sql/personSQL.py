# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupTableSvc

def getPerson(_dbConnection, _personId):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_person', _personId, _key='id')

def getPersonByCommunityUserName(_dbconnection, _personDict):
	sql = '''SELECT * FROM wf_person WHERE community = %s AND lower(username) = lower(%s)'''
	qry = _dbconnection.executeSQLQuery(sql, (_personDict.get('community', 'default'), _personDict.get('username','')))
	return None if not qry else qry[0]

def removeOrphan(_dbconnection,_personDict):
	#orphaned persons cause no harm. Try to delete, pass on fail
	sql = "DELETE FROM wf_person WHERE id = %s"
	args = (_personDict.get('id',-1),)
	try:
		_dbconnection.executeSQLCommand(sql,args)
	except Exception,e:
		pass

def createPerson(_dbConnection, _personDict, doCommit=True):
	sql = '''INSERT INTO wf_person (community,username,first_name,middle_name,last_name,suffix,email,employee_nbr,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	community = _personDict.get('community', 'default')
	username = _personDict.get('username','').lower()
	firstName = _personDict.get('first_name','')
	middleName = _personDict.get('middle_name','')
	lastName = _personDict.get('last_name','')
	suffix = _personDict.get('suffix','')
	email = _personDict.get('email','')
	employee_nbr = _personDict.get('employee_nbr','')
	created = _personDict.get('created','')
	updated = _personDict.get('updated','')
	lastuser = _personDict.get('lastuser','')

	args = (community, username, firstName, middleName, lastName, suffix, email, employee_nbr, created, updated, lastuser)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updatePerson(_dbConnection, _personDict, doCommit=True):
	sql = '''UPDATE wf_person SET username=%s,first_name=%s,middle_name=%s,last_name=%s,suffix=%s,email=%s,employee_nbr=%s,updated=%s,lastuser=%s WHERE id=%s'''

	id = _personDict.get('id',0)
	username = _personDict.get('username','').lower()
	firstName = _personDict.get('first_name','')
	middleName = _personDict.get('middle_name','')
	lastName = _personDict.get('last_name','')
	suffix = _personDict.get('suffix','')
	email = _personDict.get('email','')
	employee_nbr = _personDict.get('employee_nbr','')
	updated = _personDict.get('updated','')
	lastuser = _personDict.get('lastuser','')

	args = (username, firstName, middleName, lastName, suffix, email, employee_nbr, updated, lastuser, id)
	_dbConnection.executeSQLCommand(sql, args, doCommit)


def personExists(_dbconnection, _personDict):
	sql = '''SELECT COUNT(*) AS count FROM wf_person WHERE id = %s'''
	qry = _dbconnection.executeSQLQuery(sql,(_personDict.get('id',-1),))
	return qry[0]['count']

