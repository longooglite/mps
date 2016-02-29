# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.sql.emailSQL as emailSQL
import MPSAppt.services.fileRepoService as fileRepoSvc

def createEvaluator(_dbConnection, _evaluatorDict, doCommit=True):
	#   Only inserts Evaluator Demographic data.
	#   All other workflow-related columns are filled with default values.
	sql = '''INSERT INTO wf_evaluator
		(job_task_id,evaluator_source_id,evaluator_type_id,first_name,middle_name,last_name,suffix,email,phone,salutation,degree,titles,institution,reason,
		emailed,emailed_date,emailed_username,emailed_due_date,emailed_key,emailed_email_id,
		approved,approved_date,approved_username,approved_comment,
		uploaded,uploaded_date,uploaded_username,uploaded_comment,uploaded_file_repo_seq_nbr,
		declined,declined_date,declined_username,declined_comment,
		created,updated,lastuser,address_lines,city,state,postal,admission_date,program,country) VALUES
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
		False,'','','',%s,null,
		False,'','','',
		False,'','','',0,
		False,'','','',
		%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_evaluatorDict.get('job_task_id',None),
			_evaluatorDict.get('evaluator_source_id',None),
			_evaluatorDict.get('evaluator_type_id',None),
			_evaluatorDict.get('first_name',None),
			_evaluatorDict.get('middle_name',None),
			_evaluatorDict.get('last_name',None),
			_evaluatorDict.get('suffix',None),
			_evaluatorDict.get('email',None),
			_evaluatorDict.get('phone',None),
			_evaluatorDict.get('salutation',None),
			_evaluatorDict.get('degree',None),
			_evaluatorDict.get('titles_json',None),
			_evaluatorDict.get('institution',None),
			_evaluatorDict.get('reason',None),
			_evaluatorDict.get('emailed_key',None),
			_evaluatorDict.get('created',''),
			_evaluatorDict.get('updated',''),
			_evaluatorDict.get('lastuser',''),
	        _evaluatorDict.get('address_lines_json',''),
			_evaluatorDict.get('city',''),
			_evaluatorDict.get('state',''),
			_evaluatorDict.get('postal',''),
			_evaluatorDict.get('admission_date',''),
			_evaluatorDict.get('program',''),
			_evaluatorDict.get('country',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateEvaluatorDemographics(_dbConnection, _evaluatorDict, doCommit=True):
	#   Only updates Evaluator Demographic data.
	#   All other workflow-related columns are untouched.
	sql = '''UPDATE wf_evaluator SET evaluator_source_id=%s,evaluator_type_id=%s,first_name=%s,middle_name=%s,last_name=%s,
	suffix=%s,email=%s,phone=%s,salutation=%s,degree=%s,titles=%s,institution=%s,reason=%s,updated=%s,lastuser=%s,
	address_lines = %s,city = %s,state = %s,postal = %s,admission_date = %s,program = %s,country = %s
	WHERE id=%s'''
	args = (_evaluatorDict.get('evaluator_source_id',None),
			_evaluatorDict.get('evaluator_type_id',None),
			_evaluatorDict.get('first_name',None),
			_evaluatorDict.get('middle_name',None),
			_evaluatorDict.get('last_name',None),
			_evaluatorDict.get('suffix',None),
			_evaluatorDict.get('email',None),
			_evaluatorDict.get('phone',None),
			_evaluatorDict.get('salutation',None),
			_evaluatorDict.get('degree',None),
			_evaluatorDict.get('titles_json',None),
			_evaluatorDict.get('institution',None),
			_evaluatorDict.get('reason',None),
			_evaluatorDict.get('updated',''),
			_evaluatorDict.get('lastuser',''),
			_evaluatorDict.get('address_lines_json',''),
			_evaluatorDict.get('city',''),
			_evaluatorDict.get('state',''),
			_evaluatorDict.get('postal',''),
			_evaluatorDict.get('admission_date',''),
			_evaluatorDict.get('program',''),
			_evaluatorDict.get('country',''),
			_evaluatorDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateEvaluatorEmail(_dbConnection, _evalEmailDict, doCommit=True):
	#   Only updates Evaluator Email data.
	#   All other columns are untouched.
	sql = '''UPDATE wf_evaluator SET emailed=%s,emailed_date=%s,emailed_username=%s,emailed_due_date=%s,emailed_email_id=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_evalEmailDict.get('emailed',None),
			_evalEmailDict.get('emailed_date',None),
			_evalEmailDict.get('emailed_username',None),
			_evalEmailDict.get('emailed_due_date',None),
			_evalEmailDict.get('emailed_email_id',None),
			_evalEmailDict.get('updated',''),
			_evalEmailDict.get('lastuser',''),
			_evalEmailDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateEvaluatorApproval(_dbConnection, _evalApprovalDict, doCommit=True):
	#   Only updates Evaluator Approval data.
	#   All other columns are untouched.
	sql = '''UPDATE wf_evaluator SET approved=%s,approved_date=%s,approved_username=%s,approved_comment=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_evalApprovalDict.get('approved',None),
			_evalApprovalDict.get('approved_date',None),
			_evalApprovalDict.get('approved_username',None),
			_evalApprovalDict.get('approved_comment',None),
			_evalApprovalDict.get('updated',''),
			_evalApprovalDict.get('lastuser',''),
			_evalApprovalDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateEvaluatorUpload(_dbConnection, _evalUploadDict, doCommit=True):
	#   Only updates Evaluator Upload data.
	#   All other columns are untouched.
	sql = '''UPDATE wf_evaluator SET uploaded=%s,uploaded_date=%s,uploaded_username=%s,uploaded_comment=%s,uploaded_file_repo_seq_nbr=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_evalUploadDict.get('uploaded',None),
			_evalUploadDict.get('uploaded_date',None),
			_evalUploadDict.get('uploaded_username',None),
			_evalUploadDict.get('uploaded_comment',None),
			_evalUploadDict.get('uploaded_file_repo_seq_nbr',None),
			_evalUploadDict.get('updated',''),
			_evalUploadDict.get('lastuser',''),
			_evalUploadDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateEvaluatorDeclined(_dbConnection, _evalDeclinedDict, doCommit=True):
	#   Only updates Evaluator Declined data.
	#   All other columns are untouched.
	sql = '''UPDATE wf_evaluator SET declined=%s,declined_date=%s,declined_username=%s,declined_comment=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_evalDeclinedDict.get('declined',None),
			_evalDeclinedDict.get('declined_date',None),
			_evalDeclinedDict.get('declined_username',None),
			_evalDeclinedDict.get('declined_comment',None),
			_evalDeclinedDict.get('updated',''),
			_evalDeclinedDict.get('lastuser',''),
			_evalDeclinedDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteEvaluator(_dbConnection, _evaluatorDict, doCommit=True):
	#   Delete the identified Evaluator.
	evaluatorId = int(_evaluatorDict.get('id','0'))
	sql = '''DELETE FROM wf_evaluator WHERE id=%s'''
	_dbConnection.executeSQLCommand(sql, (evaluatorId,), doCommit)

	#   Delete any referenced Email.
	emailId = _evaluatorDict.get('emailed_email_id', '0')
	if emailId:
		emailSQL.deleteEmail(_dbConnection, emailId, doCommit)

	#   Obliterate any uploaded files.
	fileRepoDict = {}
	fileRepoDict['job_task_id'] = _evaluatorDict.get('job_task_id',0)
	fileRepoDict['seq_nbr'] = _evaluatorDict.get('uploaded_file_repo_seq_nbr',0)
	fileRepoSvc.FileRepoService(_dbConnection).obliterateFileRepoForSeqNbr(fileRepoDict, doCommit)
