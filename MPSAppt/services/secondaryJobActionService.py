# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime
import MPSCore.utilities.dateUtilities as dateUtils

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as jobactionSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.workflowService as wfService
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.core.constants as constants

class SecondaryJobActionService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)


	def createSecondaryJointPromotions(self,jsPromotion,_jobActionDict,_completionContainer, _now, _username,doCommit=False):
		titleService = titleSvc.TitleService(self.connection)
		personDict = personSvc.PersonService(self.connection).getPerson(_jobActionDict.get('person_id',0))
		titleDict = titleService.getTitle(jsPromotion.get('title_id'))
		positionDict = positionSvc.getPostionById(self.connection,jsPromotion.get('position_id',0))
		workflowDict = wfService.WorkflowService(self.connection).getWorkflowById(_jobActionDict.get('workflow_id',-1))
		if titleDict and personDict and workflowDict and positionDict:
			appointmentId = self.createSecondaryAppointment(personDict,positionDict,titleDict,_completionContainer.completionDict.get('effective_date',''),_username,_now,doCommit)
			if appointmentId:
				jobActionType = lookupTableSvc.getEntityByKey(self.connection,"wf_job_action_type",constants.kJobActionTypePromotion)
				return self.createSecondaryJobAction(appointmentId,personDict,positionDict,_jobActionDict,workflowDict,jobActionType,_username,_now,doCommit)


	def createSecondaryJobActions(self,secondaryAppt,_jobActionDict, _workflow, _completionContainer, _now, _username, doCommit=False):
		personDict = personSvc.PersonService(self.connection).getPerson(_jobActionDict.get('person_id',-1))
		activeContainer = _workflow.getContainer(secondaryAppt.get('determineActiveContainer',''))
		if activeContainer:
			if activeContainer.containerDict.get('enabled',False):
				approvalContainer = _workflow.getContainer(secondaryAppt.get('approvalContainer',''))
				if approvalContainer:
					approvalContainer.loadInstance()
					if approvalContainer.isComplete():
						deptTitleContainer = _workflow.getContainer(secondaryAppt.get('deptTitleContainer',''))
						if deptTitleContainer:
							deptTitleContainer.loadInstance()
							departmentTitleDict = deptTitleContainer.confirmedTitleDict
							newJobAction = self._createSecondary(departmentTitleDict,_jobActionDict,_completionContainer,personDict,_now,_username,doCommit)
							return newJobAction


	def _createSecondary(self,departmentTitleDict,_jobActionDict,_completionContainer,_personDict,_now,_username,doCommit=False):
		titleDict = lookupTableSvc.getEntityByKey(self.connection,'wf_title', departmentTitleDict.get('title_id',-1),'id')
		departmentDict = deptSvc.DepartmentService(self.connection).getDepartment(departmentTitleDict.get('department_id',-1))
		positionId = self.createSecondaryPosition(titleDict,departmentDict,_username,_now,doCommit)
		positionDict = positionSvc.getPostionById(self.connection,positionId)
		appointmentId = self.createSecondaryAppointment(_personDict,positionDict,titleDict,_completionContainer.completionDict.get('effective_date',''),_username,_now,doCommit)
		workflowDict = wfService.WorkflowService(self.connection).getWorkflowById(_jobActionDict.get('workflow_id',-1))
		jobActionType = lookupTableSvc.getEntityByKey(self.connection,"wf_job_action_type",constants.kJobActionTypeSecondaryApptJoint)
		newJobAction = self.createSecondaryJobAction(appointmentId,_personDict,positionDict,_jobActionDict,workflowDict,jobActionType,_username,_now,doCommit)
		return newJobAction

	def createSecondaryJobAction(self,_appointmentId,_personDict,_positionDict,_jobActionDict,_workflowDict,jobActionType,_username,_now,doCommit = False):
		params = {}
		params['personDict'] = _personDict
		params['positionDict'] = _positionDict
		params['workflowDict'] = _workflowDict
		params['now'] = _now
		params['username'] = _username
		jaSvc = jobactionSvc.JobActionService(self.connection)
		jobActionDict = jaSvc._getJobActionDict(_appointmentId,params)
		jobActionDict['workflow_json'] = _jobActionDict.get('workflow_json')
		jobActionDict['complete'] = True
		jobActionDict['frozen'] = True
		jobActionDict['current_status'] = 'Complete'
		jobActionDict['primary_job_action_id'] = _jobActionDict.get('id',-1)
		jobActionDict['job_action_type_id'] = jobActionType.get('id',-1)
		jobActionDict['completed'] = _now
		jaId =  jaSvc.createJobAction(jobActionDict,doCommit)
		return jaSvc.getJobAction(jaId,ignoreAliasing=True)

	def createSecondaryAppointment(self,_personDict,_positionDict,_titleDict,_startDate,_username,_now,doCommit = False):
		appointStatus = lookupTableSvc.getEntityByKey(self.connection,"wf_appointment_status",constants.kAppointStatusFilled)
		params = {}
		params['personDict'] = _personDict
		params['positionDict'] = _positionDict
		params['titleDict'] = _titleDict
		params['now'] = _now
		params['username'] = _username
		params['start_date'] = _startDate
		params['appointment_status'] = appointStatus
		jaSvc = jobactionSvc.JobActionService(self.connection)
		appointmentDict = jaSvc._getAppointmentDict(params)
		appointmentId = jaSvc.createAppointment(appointmentDict,doCommit)
		return appointmentId


	def createSecondaryPosition(self,_titleDict,_departmentDict,_username,_now,doCommit = False):
		positionDict = {}
		positionDict['department_id'] = _departmentDict.get('id', None)
		positionDict['title_id'] = _titleDict.get('id', None)
		positionDict['is_primary'] = False
		positionDict['created'] = _now
		positionDict['updated'] = _now
		positionDict['lastuser'] = _username
		positionId = positionSvc.createPosition(self.connection,positionDict,_departmentDict,doCommit)
		return positionId