# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def createJobPosting(_dbconnection, _jobPostingDict, doCommit=True):
	sql = "INSERT INTO wf_job_posting (job_task_id,date_posted,posting_number,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s)"
	args = (_jobPostingDict.get('job_task_id',-1),
	        _jobPostingDict.get('date_posted',''),
	        _jobPostingDict.get('posting_number',''),
	        _jobPostingDict.get('created',''),
	        _jobPostingDict.get('updated',''),
	        _jobPostingDict.get('lastuser',''),)
	_dbconnection.executeSQLCommand(sql,args,doCommit)


def updateJobPosting(_dbconnection, _jobPostingDict, doCommit=True):
	sql = "UPDATE wf_job_posting SET date_posted = %s,posting_number = %s, updated = %s,lastuser = %s WHERE job_task_id = %s"
	args = (_jobPostingDict.get('date_posted',''),_jobPostingDict.get('posting_number',''),_jobPostingDict.get('updated',''),_jobPostingDict.get('lastuser',''),_jobPostingDict.get('job_task_id',''),)
	_dbconnection.executeSQLCommand(sql,args,doCommit)


def getJobPosting(_dbconnection,jobTaskId):
	sql = "SELECT * FROM wf_job_posting WHERE job_task_id = %s"
	args = (jobTaskId,)
	qry = _dbconnection.executeSQLQuery(sql,args)
	if len(qry) > 0:
		return qry[0]
	return None


