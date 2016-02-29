# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.core.constants as constants
import MPSAppt.handlers.abstractHandler as absHandler
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.departmentService as departmentSvc


class AbstractIdentifyCandidateHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _ldapLookup(self, _community, _username):
		payload = self.getInitialPayload()
		payload['community'] = _community
		payload['username'] = _username
		return self.postToAuthSvc('/ldapsearch', payload, "Unknown username")

	def _disableCommunityPrompt(self, _promptList):
		for promptDict in _promptList:
			if promptDict.get('code', '') == 'community':
				promptDict['enabled'] = False

class CandidateHandler(AbstractIdentifyCandidateHandler):
	logger = logging.getLogger(__name__)

	#   GET renders an HTML fragment that is shown inside the current frame.

	def get(self, **kwargs):
		try:
			self._getImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			workflowServ = workflowSvc.WorkflowService(connection)
			workflow = workflowServ.getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassIdentifyCandidate)

			if (not container.hasViewPermission()) and (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			relatedWorkflows = container.getConfigDict().get('relatedWorkFlows',[])
			if relatedWorkflows:
				relatedJobActions = jaService.getRelatedJobActionDicts(jobactionid)
				if relatedJobActions:
					for relatedJADict in relatedJobActions:
						relatedWorkflow = workflowServ.getWorkflowForJobAction(relatedJADict,self.getProfile().get('userProfile()',{}))
						if relatedWorkflow:
							wfcode = relatedWorkflow.mainContainer.code
							for config in relatedWorkflows:
								if wfcode == config.get('workflowcode',''):
									config['inProgress'] = True

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['relatedWorkflows'] = relatedWorkflows
			context['submitURL'] = '/appt/jobaction/identifycandidate/'+jobactionid+'/'+taskcode
			context.update(container.getEditContext(self.getSitePreferences()))

			context['community'] = community
			communityList = self.getSiteCommunityList()
			if len(communityList) > 1:
				context['promptCommunity'] = True
				context['communityList'] = communityList
			else:
				self._disableCommunityPrompt(context.get('prompts', []))

			self.render("identifyCandidate.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.
			wfService = workflowSvc.WorkflowService(connection)
			workflow = wfService.getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassIdentifyCandidate)
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			now = self.getEnvironment().formatUTCDate()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)
			self.validateFormData(formData, container, connection)

			#   Find or create the Job Task.

			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Assemble form data.

			personDict = {}
			personDict['id'] = jobAction.get('person_id', 0)
			personDict['community'] = formData.get('community', 'default')
			if not personDict['community']:
				personDict['community'] = 'default'
			personDict['username'] = formData.get('username', '')
			personDict['first_name'] = formData.get('first_name', '')
			personDict['middle_name'] = formData.get('middle_name', '')
			personDict['last_name'] = formData.get('last_name', '')
			personDict['suffix'] = formData.get('suffix', '')
			personDict['email'] = formData.get('email', '')
			personDict['employee_nbr'] = formData.get('employee_nbr', '')
			personDict['created'] = now
			personDict['updated'] = now
			personDict['lastuser'] = username

			#   Create associated workflows and process the form data.

			try:
				relatedWorkFlowCodes = self.getRelatedWorkflows(formData)
				if relatedWorkFlowCodes:
					wfService.createRelatedWorkflows(jobAction, relatedWorkFlowCodes, self.getProfile(), now, username, doCommit=False)

				personSvc.PersonService(connection).handleIdentifyCandidate(jobAction, jobTask, personDict, container, self.getProfile(), now, username, doCommit=False)
				connection.performCommit()

			except Exception, e:
				try: connection.performRollback()
				except Exception, e1: pass
				raise e

			#   Update the Roster status, which will reload the workflow.
			#   Grant Candidate access, if requested.

			workflow = self.updateRosterStatusForJobAction(connection, jobAction)
			container = workflow.getContainer(taskcode)
			if container.shouldGrantCandidateAccess():
				self.grantCandidateAccess(personDict)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def getRelatedWorkflows(self,formData):
		relatedWorkflows = []
		for key in formData:
			if key.startswith('relatedworkflow_'):
				relatedWorkflow = formData.get(key,None)
				if relatedWorkflow:
					relatedWorkflows.append(relatedWorkflow)
		return relatedWorkflows

	def validateFormData(self, _formData, _container, connection):
		jErrors = []

		#   Verify required fields.

		relatedWorkflows = _container.getConfigDict().get('relatedWorkFlows',[])
		if relatedWorkflows:
			selectedWorkflows = self.getRelatedWorkflows(_formData)
			if not selectedWorkflows:
				if not _formData.get('relatedworkflows_None','') == 'true':
					jErrors.append({'code':'relatedworkflows_None', 'field_value': '', 'message': "Please confirm that the candidate will not require additional workflows"})

		myPromptList = []
		for eachDict in _container.getConfigDict().get('prompts', []):
			myPromptList.append(eachDict.copy())
		communityList = self.getSiteCommunityList()
		if len(communityList) < 2:
			self._disableCommunityPrompt(myPromptList)

		usernamePromptDict = {}
		for  promptDict in myPromptList:
			if promptDict.get('enabled', False):
				code = promptDict.get('code', '')
				if code == 'username':
					usernamePromptDict = promptDict

				if promptDict.get('required', False):
					value = _formData.get(code, '').strip()
					if not value:
						jErrors.append({'code':code, 'field_value': '', 'message': "Required"})


		#   Lookup Username in LDAP, if:
		#   - username was entered,
		#   - the task definition instructs us to, and
		#   - the site is configured for LDAP authentication

		community = 'default'
		username = ''
		if usernamePromptDict:
			community =  _formData.get('community', 'default').strip()
			if not community:
				community = 'default'
			username =  _formData.get('username', '').strip()
			if (username) and (usernamePromptDict.get('ldapsearch', False)):
				sitePreferences = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})
				if sitePreferences.get('auth','').lower() == 'ldap':
					try:
						responseDict = self._ldapLookup(community, username)
						username = username.lower()
						_formData['username'] = username
					except Exception, e:
						jErrors.append({'code':'username', 'field_value': username, 'message': "Not found"})

		if username:
			#	when doing internal secondaries, the faculty that was chosen for the secondary must have a primary with some department
			if _container.getConfigDict().get('departmentIdentifier','') == 'personsprimary':
				theDepartment = departmentSvc.DepartmentService(connection).getPrimaryDepartmentForPersonByUniqueName(community, username)
				if not theDepartment:
					jErrors.append({'code':'username', 'field_value': '', 'message': _container.getConfigDict().get('noPrimaryDeptMsg',"Secondary appointments can only be created for faculty that has a primary appointment.")})

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


class LDAPSearchHandler(AbstractIdentifyCandidateHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassIdentifyCandidate)
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   Execute the search.

			formData = tornado.escape.json_decode(self.request.body)
			community = formData.get('community', 'default')
			if not community:
				community = 'default'
			username = formData.get('username', '')
			try:
				responseDict = self._ldapLookup(community, username)
			except Exception, e:
				raise excUtils.MPSValidationException("Not found")

			#   Return a dictionary of user data as specified by the Task.

			userDataDict = []
			for configPromptDict in container.getConfigDict().get('prompts', []):
				if configPromptDict.get('enabled', False):
					ldapField = configPromptDict.get('ldapfield', '')
					if ldapField:
						code = configPromptDict.get('code', '')
						value = ''.join(responseDict.get(ldapField, ''))
						field = {'code':code, 'value': value}
						userDataDict.append(field)

			responseDict = self.getPostResponseDict()
			responseDict['replacements'] = userDataDict
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/identifycandidate/search/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", LDAPSearchHandler),
	(r"/appt/jobaction/identifycandidate/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CandidateHandler),
]
