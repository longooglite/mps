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
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.evaluationsService as evaluationsSvc
import MPSAppt.modules.academicEvaluators as acadEvaluators

################################################################################
#   Send an Evaluator Email.
################################################################################

class EvalSendHandler(absHandler.AbstractEvalHandler):
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
			today = dateUtils.formatUTCDateOnly()
			context['current_date'] = dateUtils.parseDate(today,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('ymdformat',''))
			context.update(container.getEditContextSend(int(evaluatorid), self.getSitePreferences()))

			#   Assemble parts and pieces to render the page.

			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load(context.get('emailTemplateName', ''))
			variableContent = template.generate(context=context, skin=context['skin'])

			prologue = self.render_string("evalSendPrologue.html", context=context, skin=context['skin'])
			epilogue = self.render_string("evalSendEpilogue.html", context=context, skin=context['skin'])
			self.finish(''.join([prologue, variableContent, epilogue]))

		finally:
			self.closeConnection()


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postImpl(self, **kwargs):
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

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   Date inputs must be valid dates.

			formData = tornado.escape.json_decode(self.request.body)
			self.validateFormData(formData)

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Send email.

			evaluatorDict = {}
			evaluatorDict['job_task_id'] = jobTask.get('id',None)
			evaluatorDict['id'] = evaluatorid
			evaluatorDict['emailed'] = True
			evaluatorDict['emailed_date'] = now
			evaluatorDict['emailed_due_date'] = formData.get('return_date','')
			evaluatorDict['emailed_username'] = username
			evaluatorDict['created'] = now
			evaluatorDict['updated'] = now
			evaluatorDict['lastuser'] = username
			evaluationsSvc.EvaluationsService(connection).handleSendEmail(jobAction, jobTask, evaluatorDict, container, self.getProfile(), formData, now, username)

			responseDict = self.getPostResponseDict("Nothing to see here, move along...")
			responseDict['success'] = True
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _formData):
		jErrors = []

		fieldValue = _formData.get('return_date','').strip()
		if not fieldValue:
			jErrors.append({'code':'return_date', 'field_value': '', 'message': "Required"})
		else:
			self.parseDate(_formData, 'return_date', jErrors)

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def parseDate(self, _formData, _key, _jErrors):
		value = _formData.get(_key, '')
		if not value:
			_formData[_key] = ''
		try:
			parsed = dateUtils.flexibleDateMatch(value, self.getSiteYearMonthDayFormat())
			_formData[_key] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
		except Exception, e:
			_jErrors.append({'code':_key, 'field_value': value, 'message': "Invalid date"})


################################################################################
#   Download a sample Solicitation Letter.
################################################################################

class EvalLetterHandler(absHandler.AbstractEvalHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)
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

			#   Find the first non-Declined Evaluator.
			#   Generate HTML Letter for that Evaluator.

			evaluatorDict = self._findFirstEvaluator(container)
			if not evaluatorDict:
				raise excUtils.MPSValidationException("No Evaluators found")
			evaluatorid = evaluatorDict.get('id',0)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['taskcode'] = taskcode
			context['jobactionid'] = jobactionid
			context['evaluatorid'] = evaluatorid
			context.update(container.getEditContextSend(int(evaluatorid), self.getSitePreferences(), _isPDF=True))

			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load(context.get('emailTemplateName', ''))
			html = template.generate(context=context, skin=context['skin'])

			#   Turn the HTML into a PDF.

			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.getEnvironment(), setFooter=False, prefix = 'sampleSolicitationLetter_')
			self.redirect(pdf)

		finally:
			self.closeConnection()

	def _findFirstEvaluator(self, _container):
		_container.loadInstance()
		for evaluatorDict in _container.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				return evaluatorDict
		return None


################################################################################
#   Download the Reviewers List.
################################################################################

class EvalReviewersListHandler(absHandler.AbstractEvalHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)
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

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)
			evaluators = evaluationsSvc.EvaluationsService(connection).getReviewersForReviewersList(jobTask.get('id',-1))
			pdfContent = acadEvaluators.getExternalReviewersList(evaluators.get('evaluatorsReceived',[]),evaluators.get('evaluatorsDeclined',[]),evaluators.get('evaluatorTypeDict',{}),evaluators.get('evalSourceDict',{}),self.getEnvironment())
			path = self.getEnvironment().createGeneratedOutputFilePath("eval_", '.pdf')
			if pdfContent[0]:
				f = open(path,'wb')
				f.write(pdfContent[0])
				f.flush()
				f.close()
				self.redirect(self.getEnvironment().getUxGeneratedOutputFilePath(path))
			else:
				html = '''<html><body>There's nothing to show on the external reviewers list</body></html>'''
				pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.getEnvironment(), setFooter=False, prefix = 'reviewersList_')
				self.redirect(pdf)

		finally:
			self.closeConnection()



#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/evaluations/send/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalSendHandler),
	(r"/appt/jobaction/evaluations/letter/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", EvalLetterHandler),
	(r"/appt/jobaction/evaluations/reviewers/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", EvalReviewersListHandler),
]
