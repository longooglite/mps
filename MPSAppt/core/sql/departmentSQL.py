# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.constants as constants
import MPSAppt.services.lookupTableService as lookupTableSvc

def getDepartment(_dbConnection, _id):
	return lookupTableSvc.getEntityByKey(_dbConnection, 'wf_department', _id, _key='id')

def getAllDepartments(_dbConnection,excludeNullParents = True, sortOrder = 'upper(descr)'):
	if excludeNullParents:
		sql = '''SELECT * FROM wf_department WHERE parent_id IS NOT NULL ORDER BY %s''' % (sortOrder)
	else:
		sql = '''SELECT * FROM wf_department ORDER BY %s''' % (sortOrder)
	return _dbConnection.executeSQLQuery(sql,())

def getDepartmentChair(_dbConnection,_deptId):
	sql = "SELECT * FROM wf_department_chair WHERE department_id = %s"
	args = (_deptId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def getRootDepartment(_dbConnection):
	sql = '''SELECT * FROM wf_department WHERE parent_id IS NULL'''
	resultList = _dbConnection.executeSQLQuery(sql)
	if len(resultList) != 1:
		return None
	return resultList[0]

def deleteAllDepartmentsForUser(_dbConnection, _community, _username, doCommit=True):
	sql = '''DELETE FROM wf_username_department WHERE community = %s AND username = %s'''
	args = (_community, _username)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def addDepartmentForUser(_dbConnection, _community, _username, _departmentCode, doCommit=True):
	sql = '''INSERT INTO wf_username_department (community,username, department_id) VALUES (%s,%s,(SELECT id FROM wf_department WHERE code = %s))'''
	args = (_community, _username, _departmentCode)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getDepartmentForJobAction(_dbConnection,_jobAction):
	sql = '''SELECT wf_department.id,wf_department.code,wf_department.active,wf_department.descr,wf_department.parent_id,wf_department.pcn_id,
	wf_department.cc_acct_cd,wf_department.email_address,wf_department.header_image,wf_department.address_lines,
	wf_department.city,wf_department.state,wf_department.postal,wf_department.address_suffix
	FROM wf_position,wf_department WHERE wf_position.department_id = wf_department.id AND wf_position.id = %s'''
	args = (_jobAction.get('position_id',-1),)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def getDepartmentsForUser(_dbConnection, _community, _username):
	sql = '''SELECT DEPT.* FROM wf_username_department AS JOYNE
			JOIN wf_department AS DEPT ON DEPT.id = JOYNE.department_id
			WHERE JOYNE.community = %s AND JOYNE.username = %s ORDER BY DEPT.code'''
	args = (_community, _username)
	return _dbConnection.executeSQLQuery(sql,args)

def getDepartmentChairs(_dbConnection):
	sql = "SELECT * FROM wf_department_chair ORDER BY department_id ASC, seq ASC"
	args = ()
	return _dbConnection.executeSQLQuery(sql,args)

def getPrimaryDepartmentForPerson(_dbConnection,_personId):
	sql = '''SELECT DEPT.id,DEPT.code,DEPT.descr,DEPT.active,DEPT.parent_id,DEPT.pcn_id,DEPT.cc_acct_cd,DEPT.email_address,
	DEPT.header_image,DEPT.address_lines,DEPT.city,DEPT.state,DEPT.postal,DEPT.address_suffix
	FROM wf_department DEPT,wf_appointment APPT, wf_position POS, wf_appointment_status APPTSTAT
	WHERE APPT.person_id = %s AND
	APPT.position_id = POS.id AND
	POS.department_id = DEPT.id AND
	POS.is_primary = 't' AND
	APPT.appointment_status_id = APPTSTAT.id AND
	APPTSTAT.code = %s;'''
	args = (_personId,constants.kAppointStatusFilled,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def getPrimaryDepartmentForPersonByUniqueName(_dbConnection, _community, _username):
	sql = '''SELECT DEPT.id,DEPT.code,DEPT.descr,DEPT.active,DEPT.parent_id,DEPT.pcn_id,DEPT.cc_acct_cd,DEPT.email_address,
	DEPT.header_image,DEPT.address_lines,DEPT.city,DEPT.state,DEPT.postal,DEPT.address_suffix
	FROM wf_department DEPT,wf_appointment APPT, wf_position POS, wf_appointment_status APPTSTAT, wf_person PERS
	WHERE PERS.community = %s AND
	PERS.username = %s AND
	PERS.id = APPT.person_id AND
	APPT.position_id = POS.id AND
	POS.department_id = DEPT.id AND
	POS.is_primary = 't' AND
	APPT.appointment_status_id = APPTSTAT.id AND
	APPTSTAT.code = %s;'''
	args = (_community, _username, constants.kAppointStatusFilled)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def createDepartment(_dbConnection, _departmentDict, doCommit=True):
	sql = '''INSERT INTO wf_department (code,descr,active,parent_id,pcn_id,cc_acct_cd,email_address,header_image,address_lines,city,state,postal,address_suffix) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_departmentDict.get('code', None),
			_departmentDict.get('descr', None),
			_departmentDict.get('active', None),
			_departmentDict.get('parent_id', None),
			_departmentDict.get('pcn_id', None),
			_departmentDict.get('cc_acct_cd', None),
			_departmentDict.get('email_address', None),
			_departmentDict.get('header_image', None),
			_departmentDict.get('address_lines', None),
			_departmentDict.get('city', None),
			_departmentDict.get('state', None),
			_departmentDict.get('postal', None),
			_departmentDict.get('address_suffix', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateDepartment(_dbConnection, _departmentDict, doCommit=True):
	sql = '''UPDATE wf_department SET code=%s,descr=%s,active=%s,parent_id=%s,pcn_id=%s,cc_acct_cd=%s,email_address=%s,header_image=%s,address_lines=%s,city=%s,state=%s,postal=%s,address_suffix=%s WHERE id=%s'''
	args = (_departmentDict.get('code', None),
			_departmentDict.get('descr', None),
			_departmentDict.get('active', None),
			_departmentDict.get('parent_id', None),
			_departmentDict.get('pcn_id', None),
			_departmentDict.get('cc_acct_cd', None),
			_departmentDict.get('email_address', None),
			_departmentDict.get('header_image', None),
			_departmentDict.get('address_lines', None),
			_departmentDict.get('city', None),
			_departmentDict.get('state', None),
			_departmentDict.get('postal', None),
			_departmentDict.get('address_suffix', None),
			_departmentDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createPCN(_dbConnection, _pcnDict, doCommit=True):
	sql = '''INSERT INTO wf_pcn (code,seq) VALUES (%s,%s)'''
	args = (_pcnDict.get('code', None),
			_pcnDict.get('seq', 0))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteAllChairsForDepartment(_dbConnection, _departmentDict, doCommit=True):
	sql = '''DELETE FROM wf_department_chair WHERE department_id = %s'''
	args = (_departmentDict.get('id', 0),)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def createDepartmentChair(_dbConnection, _chairDict, doCommit=True):
	sql = '''INSERT INTO wf_department_chair (department_id,chair_with_degree,chair_signature,chair_titles,seq) VALUES (%s,%s,%s,%s,%s)'''
	args = (_chairDict.get('department_id', None),
			_chairDict.get('chair_with_degree', None),
			_chairDict.get('chair_signature', None),
			_chairDict.get('chair_titles', None),
			_chairDict.get('seq', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
