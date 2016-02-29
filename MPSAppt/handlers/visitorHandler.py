# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.core.constants as constants
import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.handlers.uberFormHelper as uberHelper
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.evaluationsService as evaluationsSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.fileRepoService as fileUploadSvc
import MPSAppt.services.jobActionResolverService as jaResolverSvc
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.uberContainerService as uberContainerSvc
import MPSAppt.services.uberDisplayService as uberDisplaySvc
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSAppt.core.packetMaster as packetMeister
import MPSCore.utilities.stringUtilities as stringUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper
import MPSCore.utilities.exceptionUtils as excUtils

kBadVisitorMessage = "Unable to identify visitor"
kRedirectURL = '/appt/visitor/unauthorized'

class AbstractVisitorHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	@mpsExceptionWrapper(kBadVisitorMessage)
	def verifyVisitorRequest(self):

		#   Verify that an incoming visitor request specifies a valid site.
		#   Site must be on the request header.

		payload = self.getInitialPayload()
		payload['profileSite'] = payload.get('site','')
		responseDict =  self.postToAuthSvc("/siteprofiledetailbypass", payload, "Unable verify user credentials")

		userProfile = {}
		userProfile['userPermissions'] = self._visitorPermissions()

		visitorProfile = {}
		visitorProfile['siteProfile'] = responseDict
		visitorProfile['userProfile'] = userProfile
		self.setProfile(visitorProfile)
		return responseDict

	def _visitorPermissions(self):
		userPermissions = {}
		userPermissions['appcode'] = self.getEnvironment().getAppCode()
		userPermissions['code'] = 'apptVisitor'
		userPermissions['descr'] = 'Visitor'
		return [userPermissions]

	def resolveNames(self, _evaluatorDict):
		firstName = _evaluatorDict.get('first_name','')
		middleName = _evaluatorDict.get('middle_name','')
		lastName = _evaluatorDict.get('last_name','')
		suffix = _evaluatorDict.get('suffix','')
		_evaluatorDict['full_name'] = stringUtils.constructFullName(firstName, lastName, middleName, suffix)
		_evaluatorDict['last_comma_first'] = stringUtils.constructLastCommaFirstName(firstName, lastName)


class UnauthorizedHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	#   Render the "You're a Bad Bad Person" screen.

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):

		#   Try to log out, no biggie if we can't.
		try:
			payload = { 'mpsid': self.getCookie('mpsid') }
			self.clear_cookie('mpsid')
			self.postToAuthSvc("/logout", payload)
		except Exception:
			pass

		#   Render the Unauthorized page, no questions asked.

		self.setProfile({})
		context = self.getInitialTemplateContext(self.getEnvironment())
		self.render("unauthorized.html", context=context, skin=context['skin'])


class CandidatePacketHandler(AbstractVisitorHandler):
	logger = logging.getLogger(__name__)

	#   Download the ePacket associated with this Candidate.

	def get(self, **kwargs):
		try:
			self._getImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger, _optionalOverrideRedirect=kRedirectURL)

	def _getImpl(self, **kwargs):
		self.verifyVisitorRequest()

		#   Email Key is required.

		emailKey = kwargs.get('key', '')
		if not emailKey:
			raise excUtils.MPSValidationException(kBadVisitorMessage)

		connection = self.getConnection()
		try:
			#   Find the Evaluator record for the given key.
			#   This will guide us to the Job Task and the associated Job Action.

			evalSvc = evaluationsSvc.EvaluationsService(connection)
			evaluatorDict = evalSvc.getEvaluatorByEmailKey(emailKey)
			if not evaluatorDict:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			taskId = evaluatorDict.get('job_task_id', 0)
			jobTask = lookupTableSvc.getEntityByKey(connection, 'wf_job_task', taskId, _key='id')
			if not jobTask:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			jobActionId = jobTask.get('job_action_id', 0)
			taskCode = jobTask.get('task_code', '')

			#   Load the Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobActionId)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskCode, constants.kContainerClassEvaluations)

			#   Assemble information and generate the Solicitation Packet.

			siteProfile = self.getProfile().get('siteProfile',{})
			sitePreferences = siteProfile.get('sitePreferences', {})
			site = siteProfile.get('site','')

			candidate = jaService.getCandidateDict(jobAction)
			title = jaService.getTitle(jobAction)
			department = positionSvc.getDepartment(connection, jobAction.get('position_id',0))

			templateLoader = self.getEnvironment().getTemplateLoader()
			templateName = sitePreferences.get('packettoc', 'packetTOC.html')
			templatePath = self.buildFullPathToSiteTemplate(templateName)
			packetCode = container.getConfigDict().get('packet_code', taskCode)

			context = {
				"packet_title": container.getConfigDict().get('title',''),
				"candidate_name": candidate.get('full_name',''),
				"title": title.get('descr',''),
				"department": department.get('full_descr',''),
				"profile": self.getProfile(),
				"handler": self,
			}
			packetGenerator = packetMeister.PacketMaster(connection,packetCode,container.getDescr(),workflow,templateLoader,templatePath,context,container.getConfigDict())
			packetGenerator.generatePacket()
			self.redirect(packetGenerator.getUxPath())

		finally:
			self.closeConnection()


class AbstractEvaluatorResponseHandler(AbstractVisitorHandler):
	logger = logging.getLogger(__name__)

	#   Common code for soliciting an evaluator's feedback.
	#   GET renders an HTML page allowing the Evaluator enter his response.

	def _impl(self, **kwargs):
		self.verifyVisitorRequest()

		#   Email Key is required.

		emailKey = kwargs.get('key', '')
		if not emailKey:
			raise excUtils.MPSValidationException(kBadVisitorMessage)

		connection = self.getConnection()
		try:
			#   Find the Evaluator record for the given key.
			#   This will guide us to the Job Task and the associated Job Action.

			evalSvc = evaluationsSvc.EvaluationsService(connection)
			evaluatorDict = evalSvc.getEvaluatorByEmailKey(emailKey)
			if not evaluatorDict:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			taskId = evaluatorDict.get('job_task_id', 0)
			jobTask = lookupTableSvc.getEntityByKey(connection, 'wf_job_task', taskId, _key='id')
			if not jobTask:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			jobActionId = jobTask.get('job_action_id', 0)
			taskCode = jobTask.get('task_code', '')
			evaluatorId = evaluatorDict.get('id',0)
			emailKey = evaluatorDict.get('emailed_key','')

			#   Load the Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobActionId)
			resolvedJobAction = jaResolverSvc.JobActionResolverService(connection,self.profile.get('siteProfile',{}).get('sitePreferences',{})).resolve(jobAction)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskCode, constants.kContainerClassEvaluations)

			now = self.getEnvironment().formatUTCDate()
			username = self.getUserProfileUsername()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Do not allow uploads if the Task or Job Action is Frozen or Complete.
			#   This essentially means that we are past the point in the workflow where we want the Evaluator's feedback.

			if (jobTask.get('frozen', False)) or \
				(jobAction.get('frozen', False)) or \
				(jobAction.get('complete', False)):
				raise excUtils.MPSValidationException('We are no longer accepting responses for this candidate.')

			#   Render the page.
			container.loadInstance()
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['taskcode'] = taskCode
			context['jobactionid'] = jobActionId
			context['appointment_type'] = resolvedJobAction.get('job_action_type',{}).get('descr','')
			context['department_descr'] = resolvedJobAction.get('department',{}).get('descr','')
			context['department_full_descr'] = resolvedJobAction.get('department',{}).get('full_descr', context['department_descr'])
			context['title_descr'] = resolvedJobAction.get('title',{}).get('descr','')
			context['evaluatorid'] = evaluatorId

			if kwargs.get('responseType', 'file') == 'form':
				context.update(container.getEditContextForm(int(evaluatorId), self.getSitePreferences(), _isVisitor=True))
				self.executeCustomUberHook(container,context,evaluatorId)
				self.render('visitorUberForm.html', context=context, skin=context['skin'])
			else:
				context.update(container.getEditContextFile(int(evaluatorId), self.getSitePreferences()))
				context['upload_url'] = "/appt/visitor/evaluator/upload/%s" % (emailKey,)
				self.render('visitorFileUpload.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def executeCustomUberHook(self,container,context,evaluatorId):
		customHook = container.getConfigDict().get('customUberHook','')
		if customHook:
			try:
				importString = "import MPSAppt.modules.%s as mangler" % (customHook)
				exec importString
				manglerInstance = eval('mangler.UberContentMangler()')
				manglerInstance.mangleContent(self.dbConnection,context,container,evaluatorId)
			except Exception,e:
				pass

class EvaluatorUploadHandler(AbstractEvaluatorResponseHandler):
	logger = logging.getLogger(__name__)

	#   GET renders an HTML page allowing the Evaluator to upload his evaluation.

	def get(self, **kwargs):
		try:
			self._getImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger, _optionalOverrideRedirect=kRedirectURL)

	def _getImpl(self, **kwargs):
		kwargs['responseType'] = 'file'
		self._impl(**kwargs)


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postImpl(self, **kwargs):
		self.verifyVisitorRequest()

		#   Email Key is required.

		emailKey = kwargs.get('key', '')
		if not emailKey:
			raise excUtils.MPSValidationException(kBadVisitorMessage)

		connection = self.getConnection()
		try:
			#   Find the Evaluator record for the given key.
			#   This will guide us to the Job Task and the associated Job Action.

			evalSvc = evaluationsSvc.EvaluationsService(connection)
			evaluatorDict = evalSvc.getEvaluatorByEmailKey(emailKey)
			if not evaluatorDict:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			taskId = evaluatorDict.get('job_task_id', 0)
			jobTask = lookupTableSvc.getEntityByKey(connection, 'wf_job_task', taskId, _key='id')
			if not jobTask:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			jobActionId = jobTask.get('job_action_id', 0)
			taskCode = jobTask.get('task_code', '')
			evaluatorId = evaluatorDict.get('id',0)
			emailKey = evaluatorDict.get('emailed_key','')

			#   Load the Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobActionId)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskCode, constants.kContainerClassEvaluations)

			now = self.getEnvironment().formatUTCDate()
			username = self.getUserProfileUsername()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Do not allow uploads if the Task or Job Action is Frozen or Complete.
			#   This essentially means that we are past the point in the workflow where we want the Evaluator's feedback.

			if (jobTask.get('frozen', False)) or \
				(jobAction.get('frozen', False)) or \
				(jobAction.get('complete', False)):
				raise excUtils.MPSValidationException('We are no longer accepting responses for this candidate.')

			#   Check the uploaded file.

			fileData = self.request.files.get('file_data', [])
			if not fileData:
				raise excUtils.MPSValidationException("No file provided")

			fileObject = fileData[0]
			message,pages,pdfversion = self.validatePDFOrImageContent(fileObject,container)
			if message:
				raise excUtils.MPSValidationException()

			fileContents = fileObject.body
			filename = fileObject.filename
			fileContentType = fileObject.content_type

			#   File Upload.

			self.resolveNames(evaluatorDict)
			username = evaluatorDict.get('full_name','')
			now = self.getEnvironment().formatUTCDate()

			activityLogFlag = container.getConfigDict().get('activityLog',{}).get('enabled', False)
			container.getConfigDict().get('activityLog',{})['enabled'] = False

			fileRepoDict = {}
			fileRepoDict['job_task_id'] = jobTask.get('id',None)
			fileRepoDict['seq_nbr'] = evaluatorId
			fileRepoDict['pages'] = pages
			fileRepoDict['pdf_version_nbr'] = pdfversion
			fileRepoDict['file_name'] = filename
			fileRepoDict['content'] = bytearray(fileContents)
			fileRepoDict['content_type'] = fileContentType
			fileRepoDict['created'] = now
			fileRepoDict['updated'] = now
			fileRepoDict['lastuser'] = username
			fileUploadSvc.FileRepoService(connection).handleUpload(jobAction, jobTask, fileRepoDict, container, self.getProfile(), now, username, doCommit=False)

			evaluatorDict = {}
			evaluatorDict['job_task_id'] = jobTask.get('id',None)
			evaluatorDict['id'] = evaluatorId
			evaluatorDict['uploaded'] = True
			evaluatorDict['uploaded_date'] = now
			evaluatorDict['uploaded_username'] = username
			evaluatorDict['uploaded_comment'] = ''
			evaluatorDict['uploaded_file_repo_seq_nbr'] = evaluatorId
			evaluatorDict['created'] = now
			evaluatorDict['updated'] = now
			evaluatorDict['lastuser'] = username
			container.getConfigDict().get('activityLog',{})['enabled'] = activityLogFlag
			evaluationsSvc.EvaluationsService(connection).handleFileUpload(jobAction, jobTask, evaluatorDict, container, self.getProfile(), {}, now, username)

			responseDict = {}
			responseDict['success'] = True
			responseDict['successMsg'] = 'File Uploaded'
			responseDict['filename'] = filename
			responseDict['escapedResponseStr'] = tornado.escape.json_encode(responseDict)
			context = {}
			context['responseDict'] = responseDict
			self.render("uploadResult.html", context=context, skin='default')

		finally:
			self.closeConnection()


class EvaluatorFormHandler(AbstractEvaluatorResponseHandler):
	logger = logging.getLogger(__name__)

	#   GET renders an HTML page allowing the Evaluator to upload his evaluation.

	def get(self, **kwargs):
		try:
			self._getImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger, _optionalOverrideRedirect=kRedirectURL)

	def _getImpl(self, **kwargs):
		kwargs['responseType'] = 'form'
		self._impl(**kwargs)


class AbstractEvaluatorFormResponseHandler(EvaluatorFormHandler):
	logger = logging.getLogger(__name__)

	def _formSubmitDraftPrintImpl(self, **kwargs):
		isPrint = kwargs.get('print', False)
		if not isPrint:
			self.writePostResponseHeaders()
		self.verifyVisitorRequest()

		#   Email Key is required.

		emailKey = kwargs.get('key', '')
		if not emailKey:
			raise excUtils.MPSValidationException(kBadVisitorMessage)

		connection = self.getConnection()
		try:
			#   Find the Evaluator record for the given key.
			#   This will guide us to the Job Task and the associated Job Action.

			evalSvc = evaluationsSvc.EvaluationsService(connection)
			evaluatorDict = evalSvc.getEvaluatorByEmailKey(emailKey)
			if not evaluatorDict:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			taskId = evaluatorDict.get('job_task_id', 0)
			jobTask = lookupTableSvc.getEntityByKey(connection, 'wf_job_task', taskId, _key='id')
			if not jobTask:
				raise excUtils.MPSValidationException(kBadVisitorMessage)

			jobActionId = jobTask.get('job_action_id', 0)
			taskCode = jobTask.get('task_code', '')

			#   Load the Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobActionId)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskCode, constants.kContainerClassEvaluations)

			now = self.getEnvironment().formatUTCDate()
			username = self.getUserProfileUsername()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Do not allow uploads if the Task or Job Action is Frozen or Complete.
			#   This essentially means that we are past the point in the workflow where we want the Evaluator's feedback.

			if (jobTask.get('frozen', False)) or \
				(jobAction.get('frozen', False)) or \
				(jobAction.get('complete', False)):
				raise excUtils.MPSValidationException('We are no longer accepting responses for this candidate.')

			#   Manufacture an uber container for this evaluator.

			groupCode = container.getConfigDict().get('questionGroupCode', '')
			containerCode = emailKey

			jaResolver = jaResolverSvc.JobActionResolverService(connection, self.getProfile().get('siteProfile', {}).get('sitePreferences', {}))
			jaContext = jaResolver.resolve(jobAction)
			titleCode = jaContext.get('title', {}).get('code', '')

			containerService = uberContainerSvc.UberContainerService(connection)
			uberContainer = containerService.createUberContainer(workflow, containerCode, groupCode, titleCode)

			#   Find the Evaluator-specific Job Task.

			evaluatorJobTask = jaService.getOrCreateJobTask(jobAction, uberContainer, now, containerCode)
			jobTaskCache = workflow.getJobTaskCache()
			jobTaskCache[containerCode] = evaluatorJobTask

			#   Do Print or data.

			if isPrint:
				uberDispSvc = uberDisplaySvc.UberDisplayService(connection)
				context = self.getInitialTemplateContext(self.getEnvironment())
				context['candidateName'] = jaContext.get('person', {}).get('full_name', '')
				context['header'] = container.getConfigDict().get('printHeader', container.getHeader())
				context['uberContent'] = uberDispSvc.getContent(uberContainer, self.getSitePreferences())
				context.update(container.getEditContextForm(evaluatorDict.get('id',0), self.getSitePreferences(), _isVisitor=False))
				self.executeCustomUberHook(container,context,None)

				loader = self.getEnvironment().getTemplateLoader()
				template = loader.load('uberPrint.html')
				html = template.generate(context=context)
				pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.getEnvironment(), setFooter=True, prefix = 'uberOut_')
				self.redirect(pdf)

			else:
				#   Validate form data.

				helper = uberHelper.UberFormHelper(self)
				formData, repeatingGroupData = helper.processUberFormData(uberContainer, **kwargs)

				#   Construct data and persist.

				isDraft = kwargs.get('draft', False)
				if isDraft:
					evaluatorDict['uploaded'] = False
					evaluatorDict['uploaded_date'] = ''
					evaluatorDict['uploaded_username'] = ''
					evaluatorDict['uploaded_comment'] = ''
				else:
					evaluatorDict['uploaded'] = True
					evaluatorDict['uploaded_date'] = now
					evaluatorDict['uploaded_username'] = username
					evaluatorDict['uploaded_comment'] = ''

				insertList, updateList, deleteList = helper.identifyDataChanges(uberContainer, formData, repeatingGroupData)
				uberSvc.UberService(connection).handleSubmit(jobAction, evaluatorJobTask, insertList, updateList, deleteList, uberContainer, isDraft, self.getProfile(), now, username, doCommit=False)
				evalSvc.handleFormSubmission(jobAction, jobTask, evaluatorDict, container, isDraft, self.getProfile(), formData, now, username, doCommit=True)
				self.updateRosterStatusForJobAction(connection, jobAction)

				#   UberForm components can be shared across Job Actions.
				#   If this Job Action is related to other Job Actions, update their roster statuses as well.

				relatedJobActionIds = jaService.getRelatedJobActions(jobAction.get('id', 0))
				for relatedId in relatedJobActionIds:
					self.updateRosterStatusForJobAction(connection, { 'id': relatedId })

				responseDict = {}
				responseDict['success'] = True
				responseDict['successMsg'] = 'Assessment saved' if isDraft else 'Assessment submitted'
				self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


class EvaluatorFormSubmitHandler(AbstractEvaluatorFormResponseHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['draft'] = False
		kwargs['print'] = False
		self._formSubmitDraftPrintImpl(**kwargs)


class EvaluatorFormDraftHandler(AbstractEvaluatorFormResponseHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['draft'] = True
		kwargs['print'] = False
		self._formSubmitDraftPrintImpl(**kwargs)


class EvaluatorFormPrintHandler(AbstractEvaluatorFormResponseHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['draft'] = False
		kwargs['print'] = True
		self._formSubmitDraftPrintImpl(**kwargs)


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/visitor/unauthorized', UnauthorizedHandler),
	(r'/appt/visitor/candidate/packet/(?P<key>[^/]*)', CandidatePacketHandler),
	(r'/appt/visitor/evaluator/upload/(?P<key>[^/]*)', EvaluatorUploadHandler),
	(r'/appt/visitor/evaluator/form/(?P<key>[^/]*)', EvaluatorFormHandler),
	(r'/appt/visitor/evaluator/form/submit/(?P<key>[^/]*)', EvaluatorFormSubmitHandler),
	(r'/appt/visitor/evaluator/form/draft/(?P<key>[^/]*)', EvaluatorFormDraftHandler),
	(r'/appt/visitor/evaluator/form/print/(?P<key>[^/]*)', EvaluatorFormPrintHandler),
]
