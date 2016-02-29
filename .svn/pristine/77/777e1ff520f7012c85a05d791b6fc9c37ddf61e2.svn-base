# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getQuestionsAndOptionsForTask(_dbconnection,taskCode):
	sql = '''SELECT q.id as quest_id,
	q.code AS quest_code,
	q.active AS quest_active,
	q.prompt AS quest_prompt,
	q.required AS quest_required,
	q.identifier_code AS quest_identifier_code,
	q.nbr_rows AS quest_nbr_rows,
	o.id as opt_id,
	o.code AS opt_code,
	o.active AS opt_active,
	o.option_text AS opt_text,
	o.has_text AS opt_has_text,
	o.text_title AS opt_text_title,
	o.text_required AS opt_text_required,
	o.nbr_rows AS opt_nbr_rows
	FROM wf_question q LEFT OUTER JOIN wf_question_option o ON q.id = o.question_id
	WHERE q.task_code = %s ORDER BY q.seq ASC,o.seq ASC;'''
	args = (taskCode,)
	qry = _dbconnection.executeSQLQuery(sql,args)
	return qry

def getQuestionsAndOptionsForTaskAndIdentifierCode(_dbconnection,taskCode,identifierCode):
	sql = '''SELECT q.id as quest_id,
	q.code AS quest_code,
	q.active AS quest_active,
	q.prompt AS quest_prompt,
	q.required AS quest_required,
	q.identifier_code AS quest_identifier_code,
	q.nbr_rows AS quest_nbr_rows,
	o.id as opt_id,
	o.code AS opt_code,
	o.active AS opt_active,
	o.option_text AS opt_text,
	o.has_text AS opt_has_text,
	o.text_title AS opt_text_title,
	o.text_required AS opt_text_required,
	o.nbr_rows AS opt_nbr_rows
	FROM wf_question q LEFT OUTER JOIN wf_question_option o ON q.id = o.question_id
	WHERE q.task_code = %s AND identifier_code = %s ORDER BY q.seq ASC,o.seq ASC;'''
	args = (taskCode,identifierCode,)
	qry = _dbconnection.executeSQLQuery(sql,args)
	return qry


def insertResponseToOption(_dbconnection,_job_task_id,_questionid,_optionid,_textresponse,created,updated,lastuser,isComplete,doCommit=True):
	sql = "INSERT INTO wf_question_response (job_task_id,text_response,question_id,question_option_id,created,updated,lastuser,complete) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (_job_task_id,_textresponse,_questionid,_optionid,created,updated,lastuser,isComplete)
	_dbconnection.executeSQLCommand(sql,args,doCommit)

def deleteResponsesToQuestions(_dbconnection,jobTaskId,doCommit=True):
	sql = "DELETE FROM wf_question_response WHERE job_task_id = %s"
	args = (jobTaskId,)
	_dbconnection.executeSQLCommand(sql,args,doCommit)

def getResponsesToQuestions(_dbconnection,job_task_id,task_code):
	sql = "SELECT * FROM wf_question_response WHERE job_task_id = %s AND question_id IN(SELECT id FROM wf_question WHERE task_code = %s);"
	args = (job_task_id,task_code,)
	return _dbconnection.executeSQLQuery(sql,args)

def getResponseToSingleQuestion(_dbconnection,job_task_id,question_id):
	sql = "SELECT * FROM wf_question_response WHERE job_task_id = %s AND question_id = %s;"
	args = (job_task_id,question_id,)
	return _dbconnection.executeSQLQuery(sql,args)


def getQuestion(_dbconnection,questioncode):
	sql = "SELECT * FROM wf_question WHERE code = %s"
	args = (questioncode,)
	qry = _dbconnection.executeSQLQuery(sql,args)
	return qry[0] if qry else None

def getOption(_dbconnection,promptcode):
	sql = "SELECT * FROM wf_question_option WHERE code = %s"
	args = (promptcode,)
	qry = _dbconnection.executeSQLQuery(sql,args)
	return qry[0] if qry else None
