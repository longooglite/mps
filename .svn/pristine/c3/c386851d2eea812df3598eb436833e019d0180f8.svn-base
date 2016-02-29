# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getJointPromotions(_dbConnection, _jobTaskId):
	sql = "SELECT * FROM wf_joint_promotion WHERE job_task_id = %s"
	args = (_jobTaskId,)
	return _dbConnection.executeSQLQuery(sql,args)

def deleteAllJointPromotions(_dbConnection,jobTaskId,doCommit=True):
	sql = "DELETE FROM wf_joint_promotion WHERE job_task_id = %s"
	args = (jobTaskId,)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

def createJointPromotion(_dbConnection, _jointPromotionsDict, _job_TaskId, username,now, doCommit=True):
	sql = 'INSERT INTO wf_joint_promotion (job_task_id,title_id,position_id,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s)'
	args = (_job_TaskId,_jointPromotionsDict.get('title',0),_jointPromotionsDict.get('position',0),now,now,username)
	_dbConnection.executeSQLCommand(sql,args,doCommit)
