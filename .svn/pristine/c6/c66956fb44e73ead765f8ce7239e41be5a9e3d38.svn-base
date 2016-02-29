# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.core.sql.workflowSQL as wfSQL
import MPSAppt.core.workflow as wf
import MPSAppt.services.jobActionService as jaSvc
import MPSAppt.services.jobActionResolverService as jaResolverService
import MPSAppt.services.departmentService as departmentSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.core.constants as constants

class WorkflowService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getComponents(self):
		return wfSQL.getComponents(self.connection)

	def getComponentByCode(self, _componentCode):
		return wfSQL.getComponentByCode(self.connection, _componentCode)

	def getTitleOverrides(self, _workflowCode, _titleCode):
		return wfSQL.getTitleOverrides(self.connection, _workflowCode, _titleCode)

	def getTitleOverrideForWorkflowComponentTitle(self, _workflowCode, _titleCode, _componentCode):
		return wfSQL.getTitleOverrideForWorkflowComponentTitle(self.connection, _workflowCode, _titleCode, _componentCode)

	def getWorkflow(self, _workflowCode):
		return wfSQL.getWorkflow(self.connection, _workflowCode)

	def getWorkflowById(self, _workflowId):
		return wfSQL.getWorkflowById(self.connection, _workflowId)

	def getWorkflows(self):
		return wfSQL.getWorkflows(self.connection)

	def getWorkflowForJobAction(self, _jobAction, _userProfile):

		#   Given a Job Action and a set of applicable User Profile,
		#   construct and return a Workflow instance.

		#   If the Job Action is complete, and an archived Workflow has been saved with it,
		#   use the archived data. Otherwise, build the workflow from the containers stored
		#   in the database.

		titleCode = ''
		overrideWorkflowCache = None
		if (_jobAction.get('complete', False)) and (_jobAction.get('workflow_json', '')):
			overrideWorkflowCache = json.loads(_jobAction.get('workflow_json', {}))
			workflowCode = overrideWorkflowCache.get('workflowContainerCode', '')
		else:
			#   Determine that name of the 'main container', which is the name of the workflow.
			#   The id of the workflow is in the Job Action, so simply retrieve that wf_workflow
			#   table record and grab its code.

			workflowDict = self.getWorkflowById(_jobAction.get('workflow_id', None))
			workflowCode = workflowDict.get('code', '')

			#   If a Title is specified in the Job Action's companion Appointment row, use it.
			#   Otherwise, we get the default Title for the Position attached to the Job Action.

			titleDict = jaSvc.JobActionService(self.connection).getTitle(_jobAction)
			if titleDict:
				titleCode = titleDict.get('code', '')


		#   We need a parameter block consisting of the applicable User Permissions
		#   (which was conveniently provided by the caller), and the code of the
		#   applicable Title, if any.

		parameterBlock = { 'userProfile': _userProfile, 'userPermissions': _userProfile.get('userProfile', {}).get('userPermissions', []), 'titleCode': titleCode }

		#   Department

		department = departmentSvc.DepartmentService(self.connection).getDepartmentForJobAction(_jobAction)

		#   Instantiate and build the Workflow.

		workflow = wf.Workflow(self.connection, _jobAction, department)
		workflow.buildWorkflow(workflowCode, parameterBlock, _overrideWorkflowCache=overrideWorkflowCache)
		return workflow

	def titleValidForWorkflow(self, _titleCode, _workflowCode):
		workflowCache = lookupSvc.getLookupTable(self.connection, 'wf_workflow', _key='code')
		workflowDict = workflowCache.get(_workflowCode, None)
		if not workflowDict:
			return False

		titleCache = lookupSvc.getLookupTable(self.connection, 'wf_title', _key='code')
		titleDict = titleCache.get(_titleCode, None)
		if not titleDict:
			return False

		trackCache = lookupSvc.getLookupTable(self.connection, 'wf_track')
		trackDict = trackCache.get(titleDict.get('track_id',None), None)
		if not trackDict:
			return False

		metatrackCache = lookupSvc.getLookupTable(self.connection, 'wf_metatrack')
		metatrackDict = metatrackCache.get(trackDict.get('metatrack_id',None), None)
		if not metatrackDict:
			return False

		return lookupSvc.workflowMetatrackExists(self.connection, workflowDict.get('id',None), metatrackDict.get('id',None))

	def getWorkflowEntriesForMetatackAndJAType(self,_metatrackId,_jobActionTypeList):
		wfdescriptions = wfSQL.getWorkflowEntriesForMetatackAndJAType(self.connection,_metatrackId,_jobActionTypeList)
		return wfdescriptions

	def getWorkflowEntriesForJATypes(self,_jobActionTypeList):
		wfdescriptions = wfSQL.getWorkflowEntriesForJATypes(self.connection,_jobActionTypeList)
		return wfdescriptions


	#   Related workflows

	def createRelatedWorkflows(self, _masterJobAction, _workflowCodes, _profile, _now, _username, doCommit=True):
		masterJobActionId = _masterJobAction.get('id',-1)
		sitePreferences = _profile.get('siteProfile',{}).get('sitePreferences',{})

		resolver = jaResolverService.JobActionResolverService(self.connection,sitePreferences)
		resolvedMasterJobAction = resolver.resolve(_masterJobAction)
		jaService = jaSvc.JobActionService(self.connection)
		relatedJobActions = jaService.getRelatedJobActionDicts(masterJobActionId)

		try:
			for workflowCode in _workflowCodes:
				workflowDict = self.getWorkflow(workflowCode)
				if workflowDict:
					if not self.workflowForJobActionExists(relatedJobActions,workflowDict):
						params = {}
						params['workflowDict'] = workflowDict
						params['positionDict'] = resolvedMasterJobAction.get('position',{})
						params['personDict'] = resolvedMasterJobAction.get('person',{})
						params['titleDict'] = resolvedMasterJobAction.get('title',{})
						params['username'] = _username
						appointStatus = lookupSvc.getEntityByKey(self.connection,"wf_appointment_status",constants.kAppointStatusInProgress)
						if appointStatus:
							params['now'] = _now
							params['appointment_status'] = appointStatus
							childJobActionId = jaService.createWorkflow(params, doCommit=False)
							jaService.createRelatedJobAction(masterJobActionId, childJobActionId, doCommit=False)

							childJobActionDict = jaService.getJobAction(childJobActionId)
							childWorkflow = self.getWorkflowForJobAction(childJobActionDict, _profile)
							initItemCodes = childWorkflow.getMainContainer().getConfigDict().get('initItemCodes',[])

							if initItemCodes:
								personDict = {}
								personId = childJobActionDict.get('person_id', 0)
								if personId:
									personDict = personSvc.PersonService(self.connection).getPerson(personId)
								jaService.initializeJobAction(childWorkflow, personDict, initItemCodes, _profile, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e


	def workflowForJobActionExists(self,relatedJobActions,workflowDict):
		jobActionType = workflowDict.get('job_action_type_id',-1)
		for ja in relatedJobActions:
			if ja.get('job_action_type_id') == jobActionType:
				return True
		return False

