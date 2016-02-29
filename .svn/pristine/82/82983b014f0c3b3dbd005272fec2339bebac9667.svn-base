# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.encryptionUtils as encyptionlib

def getNPI(_dbConnection, _jobTaskId):
	sql = "SELECT * FROM wf_npi WHERE job_task_id = %s"
	args = (_jobTaskId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	if qry:
		qry[0]['npi_password'] = encyptionlib.decrypt(qry[0]['npi_password'])
		return qry[0]
	return None


def createNPI(_dbConnection, _npiDict, doCommit):
	sql = '''INSERT INTO wf_npi (job_task_id,npi_nbr,does_not_have_npi,npi_username,npi_password,agree,complete,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
	args = (_npiDict.get('jobTaskId',None),
	 		_npiDict.get('npi_nbr',-1),
	 		_npiDict.get('does_not_have_npi',''),
	 		_npiDict.get('npi_username',''),
	 		encyptionlib.encrypt(_npiDict.get('npi_password','')),
	        _npiDict.get('agree',''),
	        True,
	        _npiDict.get('created',''),
	        _npiDict.get('updated',''),
	        _npiDict.get('lastuser',''),)
	_dbConnection.executeSQLCommand(sql, args, doCommit)


def updateNPI(_dbConnection, _npiDict, doCommit=False):
	sql = '''UPDATE wf_npi SET npi_nbr=%s,does_not_have_npi=%s,npi_username=%s,npi_password=%s,agree=%s,updated=%s,lastuser=%s WHERE job_task_id = %s'''
	args = (_npiDict.get('npi_nbr',0),
	 		_npiDict.get('does_not_have_npi',''),
			_npiDict.get('npi_username',''),
	 		encyptionlib.encrypt(_npiDict.get('npi_password',None)),
	        _npiDict.get('agree',None),
	        _npiDict.get('updated',None),
	        _npiDict.get('lastuser',None),
	        _npiDict.get('jobTaskId',None),)
	_dbConnection.executeSQLCommand(sql, args, doCommit)
