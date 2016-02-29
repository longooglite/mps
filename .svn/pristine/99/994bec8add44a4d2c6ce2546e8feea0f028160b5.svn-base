# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractEvalHandler as absHandler
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.jobActionResolverService as jaResolverSvc
import MPSAppt.services.uberContainerService as uberContainerSvc
import MPSAppt.handlers.uberFormHelper as uberHelper
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.uberDisplayService as uberDisplaySvc
import MPSAppt.services.evaluationsService as evaluationsSvc
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.dateUtilities as dateUtils


################################################################################
#   Manipulate an Evaluator's Form Evaluation.
################################################################################

class EvalFormHandler(absHandler.AbstractEvalHandler):
	logger = logging.getLogger(__name__)


	#   GET renders an HTML fragment that is shown inside the current work frame.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Evaluator is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		evaluatorid = kwargs.get('evaluatorid', '')
		if not jobactionid or not taskcode or not evaluatorid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)

			if (not container.hasViewPermission()) and (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['taskcode'] = taskcode
			context['jobactionid'] = jobactionid
			context['evaluatorid'] = evaluatorid
			context.update(container.getEditContextForm(int(evaluatorid), self.getSitePreferences(), _isVisitor=False))
			self.executeCustomUberHook(container,context,evaluatorid)
			self.render('uber.html', context=context, skin=context['skin'])
		finally:
			self.closeConnection()


class AbstractEvalFormHandler(absHandler.AbstractEvalHandler):
	logger = logging.getLogger(__name__)

	#   POST implementation, used for both 'Save' and 'Save as Draft'.

	def _formSubmitDraftPrintImpl(self, **kwargs):
		isPrint = kwargs.get('print', False)
		if not isPrint:
			self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Evaluator is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		evaluatorid = kwargs.get('evaluatorid', '')
		if not jobactionid or not taskcode or not evaluatorid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			now = self.getEnvironment().formatUTCDate()
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Must find Evaluator.

			container.loadInstance()
			evaluatorDict = container.findEvaluatorById(int(evaluatorid))
			if not evaluatorDict:
				raise excUtils.MPSValidationException("Evaluator not found")

			#   Manufacture an uber container for this evaluator.

			groupCode = container.getConfigDict().get('questionGroupCode', '')
			containerCode = evaluatorDict.get('emailed_key', '')

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
				self.getUpdatedDisplayDate(context)
				loader = self.getEnvironment().getTemplateLoader()
				template = loader.load('uberPrint.html')
				self.executeCustomUberHook(container,context,evaluatorid)
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

				evalSvc = evaluationsSvc.EvaluationsService(connection)
				insertList, updateList, deleteList = helper.identifyDataChanges(uberContainer, formData, repeatingGroupData)
				uberSvc.UberService(connection).handleSubmit(jobAction, evaluatorJobTask, insertList, updateList, deleteList, uberContainer, isDraft, self.getProfile(), now, username, doCommit=False)
				evalSvc.handleFormSubmission(jobAction, jobTask, evaluatorDict, container, isDraft, self.getProfile(), formData, now, username, doCommit=True)
				self.updateRosterStatusForJobAction(connection, jobAction)

				#   UberForm components can be shared across Job Actions.
				#   If this Job Action is related to other Job Actions, update their roster statuses as well.

				relatedJobActionIds = jaService.getRelatedJobActions(jobAction.get('id', 0))
				for relatedId in relatedJobActionIds:
					self.updateRosterStatusForJobAction(connection, { 'id': relatedId })

				responseDict = self.getPostResponseDict("Evalation saved")
				responseDict['success'] = True
				self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def getUpdatedDisplayDate(self,context):
		uber = context.get('uber_instance',{})
		if uber:
			rawUpdated = uber.get('uber',{}).get('updated','')
			if rawUpdated:
				localizedUpdated = dateUtils.localizeUTCDate(rawUpdated,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('timezone','US/Eastern'))
				formattedUpdated= dateUtils.parseDate(localizedUpdated,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('ymdhmformat',''))
				context['updatedate_display'] = formattedUpdated


class EvaluatorFormSubmitHandler(AbstractEvalFormHandler):
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


class EvaluatorFormDraftHandler(AbstractEvalFormHandler):
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


class EvaluatorFormPrintHandler(AbstractEvalFormHandler):
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
	(r"/appt/jobaction/evaluations/form/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalFormHandler),
	(r"/appt/jobaction/evaluations/submit/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvaluatorFormSubmitHandler),
	(r"/appt/jobaction/evaluations/draft/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvaluatorFormDraftHandler),
	(r"/appt/jobaction/evaluations/print/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvaluatorFormPrintHandler),
]
