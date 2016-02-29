# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import base64

def getFileRepo(_dbConnection, _jobTaskDict, _seqNbr):
	sql = "SELECT id,job_task_id,seq_nbr,version_nbr,deleted,file_name,content_type,pages,created,updated,lastuser FROM wf_file_repo WHERE job_task_id = %s AND seq_nbr = %s AND deleted = 'f'"
	qry = _dbConnection.executeSQLQuery(sql, (_jobTaskDict.get('id',None), _seqNbr))
	return qry[0] if qry else None

def getFileRepoForVersion(_dbConnection, _jobTaskDict, _seqNbr, _versionNbr):
	sql = "SELECT id,job_task_id,seq_nbr,version_nbr,deleted,file_name,content_type,pages,created,updated,lastuser FROM wf_file_repo WHERE job_task_id = %s AND seq_nbr = %s AND version_nbr = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_jobTaskDict.get('id',None), _seqNbr, _versionNbr))
	return qry[0] if qry else None

def getLastFileRepo(_dbConnection, _jobTaskDict, _seqNbr):
	sql = "SELECT id,job_task_id,seq_nbr,version_nbr,deleted,file_name,content_type,pages,created,updated,lastuser FROM wf_file_repo WHERE job_task_id = %s AND seq_nbr = %s ORDER BY id DESC"
	qry = _dbConnection.executeSQLQuery(sql, (_jobTaskDict.get('id',None), _seqNbr))
	return qry[0] if qry else None

def getFileRepoForJobAction(_dbConnection, _jobActionId):
	sql = '''SELECT REPO.id,REPO.job_task_id,TASK.task_code,REPO.seq_nbr,REPO.version_nbr,REPO.deleted,REPO.file_name,REPO.content_type,REPO.pages,REPO.created,REPO.updated,REPO.lastuser
		FROM wf_file_repo AS REPO
			JOIN wf_job_task AS TASK ON REPO.job_task_id = TASK.id
		WHERE (TASK.job_action_id = %s) OR
			(TASK.id IN (SELECT primary_job_task_id FROM wf_job_task AS TASK2 WHERE (TASK2.job_action_id = %s) AND (TASK2.primary_job_task_id IS NOT NULL)))
		ORDER BY TASK.task_code, REPO.seq_nbr ASC, REPO.version_nbr DESC'''
	return _dbConnection.executeSQLQuery(sql, (_jobActionId, _jobActionId))

def getFileRepoContent(_dbConnection, _jobTaskDict, _seqNbr):
	sql = "SELECT id,file_name,content,pages FROM wf_file_repo WHERE job_task_id = %s AND seq_nbr = %s AND deleted = 'f'"
	qry = _dbConnection.executeSQLQuery(sql, (_jobTaskDict.get('id',None), _seqNbr))
	return _decodeResult(qry)

def getFileRepoContentForVersion(_dbConnection, _jobTaskDict, _seqNbr, _versionNbr):
	sql = "SELECT id,file_name,content,pages FROM wf_file_repo WHERE job_task_id = %s AND seq_nbr = %s AND version_nbr = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_jobTaskDict.get('id',None), _seqNbr, _versionNbr))
	return _decodeResult(qry)

def _decodeResult(_qryList):
	if _qryList:
		qryZero = _qryList[0]
		qryZero['content'] = _decodeContent(qryZero.get('content',''))
		return qryZero
	return None

def createFileRepo(_dbConnection, _fileRepoDict, doCommit=True):
	sql = '''INSERT INTO wf_file_repo (job_task_id,seq_nbr,version_nbr,pdf_version_nbr,pages,deleted,file_name,content,content_type,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
	encodedContent = _encodeContent(_fileRepoDict.get('content',''))
	args = (_fileRepoDict.get('job_task_id',None),
			_fileRepoDict.get('seq_nbr',None),
			_fileRepoDict.get('version_nbr',None),
	        _fileRepoDict.get('pdf_version_nbr',None),
			_fileRepoDict.get('pages',None),
			_fileRepoDict.get('deleted',False),
			_fileRepoDict.get('file_name',None),
			encodedContent,
			_fileRepoDict.get('content_type',''),
			_fileRepoDict.get('created',''),
			_fileRepoDict.get('updated',''),
			_fileRepoDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def setFileRepoDeleted(_dbConnection, _fileRepoDict, doCommit=True):
	sql = '''UPDATE wf_file_repo SET deleted=%s WHERE id = %s'''
	args = (_fileRepoDict.get('deleted',False),
			_fileRepoDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def obliterateFileRepoForSeqNbr(_dbConnection, _fileRepoDict, doCommit=True):
	sql = '''DELETE FROM wf_file_repo WHERE job_task_id=%s AND seq_nbr=%s'''
	args = (_fileRepoDict.get('job_task_id',0), _fileRepoDict.get('seq_nbr',0))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def _encodeContent(_content):
	return base64.b64encode(str(_content))

def _decodeContent(_content):
	return base64.b64decode(str(_content))
