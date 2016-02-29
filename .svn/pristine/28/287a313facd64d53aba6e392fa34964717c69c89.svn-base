# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getItemInjection(_dbConnection,job_task_id):
	sql = "SELECT * FROM wf_item_injection WHERE job_task_id = %s"
	args = (job_task_id,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	if len(qry) > 0:
		return qry[0]
	return None

def updateItemInjection(_dbConnection,_itemInjectionDict,doCommit=True):
	sql = "UPDATE wf_item_injection SET task_codes = %s, updated = %s,lastuser = %s WHERE job_task_id = %s"
	args = (_itemInjectionDict.get('task_codes',''),_itemInjectionDict.get('updated',''),_itemInjectionDict.get('lastuser',''),_itemInjectionDict.get('job_task_id',''),)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

def createItemInjection(_dbConnection,itemInjectionDict,doCommit=True):
	sql = "INSERT INTO wf_item_injection (job_task_id,task_codes,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s)"
	args = (itemInjectionDict.get('job_task_id',-1),
	        itemInjectionDict.get('task_codes',''),
	        itemInjectionDict.get('created',''),
	        itemInjectionDict.get('updated',''),
	        itemInjectionDict.get('lastuser',''),)
	_dbConnection.executeSQLCommand(sql,args,doCommit)
