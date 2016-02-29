# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import uuid
import MPSAppt.core.constants as constants
import MPSCore.utilities.stringUtilities as stringUtils

	#   Job Actions.

def getJobAction(_dbConnection,_jobactionid):
	sql = "SELECT * FROM wf_job_action WHERE id = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_jobactionid,))
	return qry[0] if qry else None

def getJobActionForApptId(_dbConnection, _apptId):
	sql = "SELECT * FROM wf_job_action WHERE appointment_id = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_apptId,))
	return qry[0] if qry else None

def getJobActionForPersonIdAndJobActionTypeId(_dbConnection,_personid,_jobActionTypeId):
	sql = "SELECT * FROM wf_job_action WHERE person_id = %s AND job_action_type_id = %s"
	args = (_personid,_jobActionTypeId)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry[0] if qry else None

def getJobActionType(_dbConnection, jobActionDict):
	sql = '''SELECT wf_job_action_type.id,wf_job_action_type.code, wf_job_action_type.descr FROM wf_job_action,wf_workflow,wf_job_action_type
	WHERE wf_job_action.id = %s AND wf_job_action.workflow_id = wf_workflow.id AND wf_workflow.job_action_type_id = wf_job_action_type.id;'''
	args = (jobActionDict.get('id',-1),)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry[0] if qry else None

def getJobActionTypes(_dbConnection):
	sql = '''SELECT * FROM wf_job_action_type WHERE active = 't' ORDER BY code'''
	return _dbConnection.executeSQLQuery(sql,())

def createAppointment(_dbConnection, _appointmentDict ,doCommit=True):
	sql = '''INSERT INTO wf_appointment (person_id,title_id,position_id,start_date,end_date,appointment_status_id,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_appointmentDict.get('person_id',None),
			_appointmentDict.get('title_id',None),
			_appointmentDict.get('position_id',None),
			_appointmentDict.get('start_date',''),
			_appointmentDict.get('end_date',''),
			_appointmentDict.get('appointment_status_id',None),
			_appointmentDict.get('created',''),
			_appointmentDict.get('updated',''),
			_appointmentDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
	return _dbConnection.getLastSequenceNbr('wf_appointment')

def createJobAction(_dbConnection, _jobActionDict, doCommit=True):
	externalKey = _jobActionDict.get('external_key',None)
	if not externalKey:
		externalKey = uuid.uuid4().get_hex()

	sql = '''INSERT INTO wf_job_action (person_id,position_id,appointment_id,job_action_type_id,primary_job_action_id,current_status,workflow_id,workflow_json,complete,frozen,revisions_required,field_revisions_required,cancelation_comment,cancelation_user,cancelation_date,external_key,created,updated,completed,lastuser,proposed_start_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
	args = (_jobActionDict.get('person_id',None),
			_jobActionDict.get('position_id',None),
			_jobActionDict.get('appointment_id',None),
			_jobActionDict.get('job_action_type_id',None),
			_jobActionDict.get('primary_job_action_id',None),
			_jobActionDict.get('current_status',''),
			_jobActionDict.get('workflow_id',None),
			_jobActionDict.get('workflow_json',''),
			_jobActionDict.get('complete',False),
			_jobActionDict.get('frozen',False),
			_jobActionDict.get('revisions_required',False),
			_jobActionDict.get('field_revisions_required',False),
			_jobActionDict.get('cancelation_comment',''),
			_jobActionDict.get('cancelation_user',''),
			_jobActionDict.get('cancelation_date',''),
			externalKey,
			_jobActionDict.get('created',''),
			_jobActionDict.get('updated',''),
			_jobActionDict.get('completed',''),
			_jobActionDict.get('lastuser',''),
	        _jobActionDict.get('proposed_start_date',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
	return _dbConnection.getLastSequenceNbr('wf_job_action')

def updateJobActionRosterStatus(_dbConnection, _jobActionId, _currentStatus, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_action SET current_status=%s, updated=%s, lastuser=%s WHERE id=%s'''
	args = (_currentStatus,
			_updated,
			_username,
			_jobActionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateJobActionPerson(_dbConnection, _jobActionId, _personId, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_action SET person_id=%s, updated=%s, lastuser=%s WHERE id=%s'''
	args = (_personId, _updated, _username, _jobActionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateAppointmentPersonForJobAction(_dbConnection, _jobActionId, _personId, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_appointment SET person_id=%s, updated=%s, lastuser=%s WHERE id = (SELECT appointment_id FROM wf_job_action WHERE id=%s)'''
	args = (_personId, _updated, _username, _jobActionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateJobActionComplete(_dbConnection, _jobActionId, _completeBool, _json, _cancelationComment, _cancelationUser, _cancelationDate, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_action SET complete=%s, workflow_json=%s, cancelation_comment=%s,cancelation_user=%s,cancelation_date=%s, updated=%s, lastuser=%s WHERE id=%s'''
	args = (_completeBool, _json, _cancelationComment,_cancelationUser, _cancelationDate, _updated, _username, _jobActionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateJobActionFrozen(_dbConnection, _jobActionId, _frozenBool, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_action SET frozen=%s, updated=%s, lastuser=%s WHERE id=%s'''
	args = (_frozenBool, _updated, _username, _jobActionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateJobActionProposedStartDate(_dbConnection, _jobActionId, _startDate, doCommit=True):
	sql = "UPDATE wf_job_action SET proposed_start_date = %s WHERE id = %s"
	args = (_startDate,_jobActionId,)
	_dbConnection.executeSQLCommand(sql, args,doCommit)

def getCompletableJobActionsAsOf(_dbConnection, _now):
	sql = '''SELECT DISTINCT JA.id FROM wf_completion AS COMP
		JOIN wf_job_task AS TASK
			JOIN wf_job_action AS JA ON TASK.job_action_id = JA.id
		ON COMP.job_task_id = TASK.id
	WHERE JA.complete = 'f' AND COMP.complete = 'f' AND COMP.scheduled_date <= %s'''
	return _dbConnection.executeSQLQuery(sql, (_now,))

def updateJobActionRevisionsRequired(_dbConnection, _jobActionId, _revisionsRequiredBool, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_action SET revisions_required=%s, updated=%s, lastuser=%s WHERE id=%s'''
	args = (_revisionsRequiredBool, _updated, _username, _jobActionId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getCurrentJobActionsForUser(_dbConnection, _community, _username):
	sql = '''SELECT JA.* FROM wf_job_action AS JA
		JOIN wf_appointment AS APPT ON JA.appointment_id = APPT.id
		WHERE JA.person_id = (SELECT id FROM wf_person WHERE community = %s AND lower(username) = lower(%s))
		AND APPT.appointment_status_id = (SELECT id FROM wf_appointment_status WHERE code = 'INPROGRESS')
		ORDER BY JA.id'''
	return _dbConnection.executeSQLQuery(sql, (_community, _username))

def getCurrentJobActionsForPersonId(_dbConnection, _personId):
	sql = '''SELECT JA.* FROM wf_job_action AS JA
		JOIN wf_appointment AS APPT ON JA.appointment_id = APPT.id
		WHERE JA.person_id = %s
		AND APPT.appointment_status_id = (SELECT id FROM wf_appointment_status WHERE code = 'INPROGRESS')
		ORDER BY JA.id'''
	return _dbConnection.executeSQLQuery(sql, (_personId,))

def addCancelationComment(_dbConnection, _jobActionId, _cancelationComment, _cancelationUser, _cancelationDate,doCommit=True):
	sql = '''UPDATE wf_job_action SET cancelation_comment = %s,cancelation_user = %s,cancelation_date = %s WHERE id = %s'''
	args = (_cancelationComment,_cancelationUser,_cancelationDate,_jobActionId,)
	_dbConnection.executeSQLCommand(sql, args,doCommit)

def getRelatedJobActions(_dbConnection, _jobActionId):
	sql = "SELECT * FROM wf_related_job_actions WHERE job_action1_id = %s OR job_action2_id = %s ORDER BY job_action1_id,job_action2_id"
	args = (_jobActionId, _jobActionId)
	return _dbConnection.executeSQLQuery(sql, args)

def createRelatedJobAction(_dbConnection,_masterJAId, _childJAId, doCommit=True):
	sql = "INSERT INTO wf_related_job_actions (job_action1_id,job_action2_id) VALUES (%s,%s)"
	args = (_masterJAId, _childJAId)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

def removeRelatedJobActionsforJobAction(_dbConnection, _jobActionId,doCommit=True):
	sql = "DELETE FROM wf_related_job_actions WHERE job_action1_id = %s OR job_action2_id = %s"
	args = (_jobActionId,_jobActionId,)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

	#   Appointments.

def getAppointment(_dbConnection, _appointmentId):
	sql = "SELECT * FROM wf_appointment WHERE id = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_appointmentId,))
	return qry[0] if qry else None

def getAppointmentStatus(_dbConnection,_appointmentDict):
	sql = "SELECT code,descr FROM wf_appointment_status WHERE id = %s"
	args = (_appointmentDict.get('appointment_status_id',''),)
	qry = _dbConnection.executeSQLQuery(sql, args)
	return qry[0] if qry else None

def getAppointmentsForPerson(_dbConnection, _personId):
	sql = "SELECT * FROM wf_appointment WHERE person_id = %s ORDER BY start_date DESC,created DESC, id  DESC"
	qry = _dbConnection.executeSQLQuery(sql, (_personId,))
	return qry

def getAppointmentsForPosition(_dbConnection, _positionId):
	sql = "SELECT * FROM wf_appointment WHERE position_id = %s ORDER BY start_date DESC,created DESC, id DESC"
	qry = _dbConnection.executeSQLQuery(sql, (_positionId,))
	return qry

def getFilledAppointmentForPosition(_dbConnection, _positionId):
	sql = "SELECT * FROM wf_appointment WHERE position_id = %s AND appointment_status_id = (SELECT id FROM wf_appointment_status WHERE code = 'FILLED')"
	qry = _dbConnection.executeSQLQuery(sql, (_positionId,))
	return qry[0] if qry else None

def updateAppointmentStatus(_dbConnection, _appointmentId, _appointmentStatusCode, _startDate, _endDate, _updated, _username, doCommit=True):
	if _appointmentStatusCode <> constants.kAppointStatusAbandoned:
		sql = '''UPDATE wf_appointment SET appointment_status_id = (SELECT id FROM wf_appointment_status WHERE code = %s), start_date=%s, end_date=%s, updated=%s, lastuser=%s WHERE id=%s'''
		args = (_appointmentStatusCode, _startDate, _endDate, _updated, _username, _appointmentId)
	else:
		sql = '''UPDATE wf_appointment SET appointment_status_id = (SELECT id FROM wf_appointment_status WHERE code = %s), start_date=%s, updated=%s, lastuser=%s WHERE id=%s'''
		args = (_appointmentStatusCode, _startDate, _updated, _username, _appointmentId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateAppointmentTitle(_dbConnection,_appointmentId,_titleId,_updated, _username, doCommit=True):
	sql = '''UPDATE wf_appointment SET title_id = %s,updated = %s,lastuser = %s WHERE id = %s'''
	args = (_titleId,_updated,_username,_appointmentId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

	#   Job Tasks.

def getJobTasksForJobAction(_dbConnection, _jobActionId):
	sql = "SELECT * FROM wf_job_task WHERE job_action_id = %s ORDER BY task_code"
	return _dbConnection.executeSQLQuery(sql, (_jobActionId,))

def getJobTask(_dbConnection, _jobActionDict, _container):
	sql = "SELECT * FROM wf_job_task WHERE job_action_id = %s AND task_code = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_jobActionDict.get('id',None), _container.getCode()))
	return qry[0] if qry else None

def getJobTaskById(_dbConnection, _jobTaskId):
	sql = "SELECT * FROM wf_job_task WHERE id = %s"
	qry = _dbConnection.executeSQLQuery(sql, (_jobTaskId,))
	return qry[0] if qry else None

def createJobTask(_dbConnection, _jobTaskDict, doCommit=True):
	sql = '''INSERT INTO wf_job_task (job_action_id,task_code,primary_job_task_id,frozen,revisions_required_approval_task,created,updated,lastuser) VALUES (%s,%s,%s,%s,'',%s,%s,%s)'''
	args = (_jobTaskDict.get('job_action_id',None),
			_jobTaskDict.get('task_code',None),
			_jobTaskDict.get('primary_job_task_id',None),
			_jobTaskDict.get('frozen',False),
			_jobTaskDict.get('created',''),
			_jobTaskDict.get('updated',''),
			_jobTaskDict.get('lastuser',''))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateJobTaskFrozen(_dbConnection, _jobActionId, _jobTaskCode, _frozenBool, revisionsRequiredApprovalTask, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_task SET frozen=%s, revisions_required_approval_task = %s, updated=%s, lastuser=%s WHERE job_action_id=%s AND task_code=%s'''
	args = (_frozenBool, revisionsRequiredApprovalTask, _updated, _username, _jobActionId, _jobTaskCode)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def touchJobTask(_dbConnection, _jobTaskDict, _updated, _username, doCommit=True):
	sql = '''UPDATE wf_job_task SET updated=%s, lastuser=%s WHERE id=%s'''
	args = (_updated,
			_username,
			_jobTaskDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateJobTaskPrimaryJobTaskId(_dbConnection, _jobTaskDict, doCommit=True):
	sql = '''UPDATE wf_job_task SET primary_job_task_id=%s,updated=%s,lastuser=%s WHERE id=%s'''
	args = (_jobTaskDict.get('primary_job_task_id', None),
			_jobTaskDict.get('updated', None),
			_jobTaskDict.get('lastuser', None),
			_jobTaskDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)


	#   Job Action Log.

def createJobActionLog(_dbConnection, _jobActionLogDict, doCommit=True):
	sql = '''INSERT INTO wf_job_action_log (job_action_id,job_task_id,class_name,verb,item,message,created,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_jobActionLogDict.get('job_action_id',None),
			_jobActionLogDict.get('job_task_id',None),
			_jobActionLogDict.get('class_name',None),
			_jobActionLogDict.get('verb',None),
			_jobActionLogDict.get('item',None),
			_jobActionLogDict.get('message',None),
			_jobActionLogDict.get('created',None),
			_jobActionLogDict.get('lastuser',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)


	#   Candidate.

def getCandidate(_dbConnection, _personId):
	sql = '''SELECT * FROM wf_person WHERE id = %s'''
	return _dbConnection.executeSQLQuery(sql,(_personId,))


	#   Position

def positionIsInUseOnJobAction(_dbConnection,pcn_id):
	sql = 'SELECT COUNT(*) AS count FROM wf_job_action WHERE position_id = %s'
	args = (pcn_id,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry[0]

def positionIsInUseOnAppointment(_dbConnection,pcn_id):
	sql = 'SELECT COUNT(*) AS count FROM wf_appointment WHERE position_id = %s'
	args = (pcn_id,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry[0]

	#   Department special access

def getJobActionDepartmentalOverrides(_dbConnection,_jobActionId):
	sql = "SELECT * FROM wf_permission_override WHERE job_action_id = %s"
	args = (_jobActionId,)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return qry

def getJobActionDepartmentalOverride(_dbConnection,_jobActionId,_jobTaskCode,_departmentId):
	sql = "SELECT * FROM wf_permission_override WHERE job_action_id = %s AND job_task_code = %s AND department_id = %s"
	args = (_jobActionId,_jobTaskCode,_departmentId,)
	return _dbConnection.executeSQLQuery(sql,args)

def getAllOverridesForDepartmentList(_dbConnection,departmentIdList):
	inList = stringUtils.getSQLInClause(departmentIdList,False)
	if inList:
		sql = "SELECT * FROM wf_permission_override WHERE department_id IN%s" % (inList)
		return _dbConnection.executeSQLQuery(sql,())

def createJobActionDepartmentalOverride(_dbConnection,_jobActionId,_jobTaskCode,_departmentId,_access_allowed,doCommit=True):
	sql = "INSERT INTO wf_permission_override (job_action_id,job_task_code,department_id,access_allowed) VALUES (%s,%s,%s,%s)"
	args = (_jobActionId,_jobTaskCode,_departmentId,_access_allowed,)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

def updateJobActionDepartmentalOverride(_dbConnection,_overrideId,access_allowed,doCommit=True):
	sql = "UPDATE wf_permission_override SET _access_allowed = %s WHERE id = %s"
	args = (access_allowed,_overrideId,)
	_dbConnection.executeSQLCommand(sql,args,doCommit)

def removeJobActionOverride(_dbConnection,_jobactionId,_departmentId,containerCodes):
	inList = stringUtils.getSQLInClause(containerCodes,True)
	sql = "DELETE FROM wf_permission_override WHERE job_action_id = %s AND department_id = %s and job_task_code IN" + inList
	args = (_jobactionId,_departmentId,)
	_dbConnection.executeSQLCommand(sql,args)

def removeJobActionOverrideForTaskCode(_dbConnection,_jobactionId,_taskCode):
	sql = "DELETE FROM wf_permission_override WHERE job_action_id = %s AND job_task_code = %s"
	args = (_jobactionId,_taskCode,)
	_dbConnection.executeSQLCommand(sql,args)

def removeJobActionOverrides(_dbConnection,_jobactionId):
	sql = "DELETE FROM wf_permission_override WHERE job_action_id = %s"
	args = (_jobactionId,)
	_dbConnection.executeSQLCommand(sql,args)

def getPermissionOverridesForJobAction(_dbConnection,_jobactionId,_whiteblack,_deptList):
	deptInClause = stringUtils.getSQLInClauseFromDictList(_deptList,'id',False)
	args = (_jobactionId,_whiteblack,)
	if deptInClause:
		sql = "SELECT * FROM wf_permission_override WHERE job_action_id = %s and access_allowed = %s AND department_id IN" + deptInClause
	else:
		sql = "SELECT * FROM wf_permission_override WHERE job_action_id = %s and access_allowed = %s"
	return _dbConnection.executeSQLQuery(sql,args)

def unfreezeJobTaskById(_dbConnection,_jobTaskId):
	sql = "UPDATE wf_job_task set frozen = 'f' WHERE id = %s"
	args = (_jobTaskId,)
	_dbConnection.executeSQLCommand(sql,args)