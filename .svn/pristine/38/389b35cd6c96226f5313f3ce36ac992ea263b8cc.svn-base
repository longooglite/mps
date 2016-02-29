# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.backgroundCheckService as backgroundCheckSvc
import MPSAppt.core.sql.fileRepoSQL as fileRepoSQL
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils


class AbstractBackgroundCheckHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


	#   POST handles form submissions.

	def _postImpl(self, **kwargs):
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

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassBackgroundCheck)

			if (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)
			self.validateFormData(connection, formData, container)

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Find the Background Check.

			bcService = backgroundCheckSvc.BackgroundCheckService(connection)
			existingBackgroundCheck = bcService.getBackgroundCheck(jobTask.get('id',0))
			if (not existingBackgroundCheck):
				raise excUtils.MPSValidationException("Operation not permitted")

			#   Perform the requested operation.

			backgroundCheckDict = {}
			backgroundCheckDict['id'] = existingBackgroundCheck.get('id', 0)
			backgroundCheckDict['job_task_id'] = jobTask.get('id',None)
			self.fillBackgroundCheckDict(backgroundCheckDict, container, now, username)

			actionString = '''bcService.%s(jobAction, jobTask, backgroundCheckDict, container, self.getProfile(), formData, now, username)''' % kwargs.get('backgroundCheckServiceMethodName','')
			exec actionString
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict("CBC "  + kwargs.get('responseSuffix',''))
			responseDict['success'] = True
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _formData, _container):
		pass

	def fillBackgroundCheckDict(self, _backgroundCheckDict, _container, _now, _username):
		_backgroundCheckDict['status_date'] = _now
		_backgroundCheckDict['created'] = _now
		_backgroundCheckDict['updated'] = _now
		_backgroundCheckDict['lastuser'] = _username


################################################################################
#   Display the Background Check Overview frame.
################################################################################

class BackgroundCheckOverviewHandler(AbstractBackgroundCheckHandler):
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

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassBackgroundCheck)

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
			context.update(container.getEditContext(self.getSitePreferences()))

			self.render("backgroundCheckOverview.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()



################################################################################
#   Submission Handlers.
################################################################################

class SubmitHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleSubmit'
		kwargs['responseSuffix'] = ' Submitted'
		self._postImpl(**kwargs)

	def fillBackgroundCheckDict(self, _backgroundCheckDict, _container, _now, _username):
		super(SubmitHandler, self).fillBackgroundCheckDict(_backgroundCheckDict, _container, _now, _username)
		_backgroundCheckDict['submitted_date'] = _now



################################################################################
#   Decision Handlers.
################################################################################

class AcceptHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleAccept'
		kwargs['responseSuffix'] = ' Accepted'
		self._postImpl(**kwargs)


class AcceptWithFindingsHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleAcceptWithFindings'
		kwargs['responseSuffix'] = ' Accepted with Findings'
		self._postImpl(**kwargs)


class RejectHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleReject'
		kwargs['responseSuffix'] = ' Rejected'
		self._postImpl(**kwargs)



################################################################################
#   Stored Content Handlers.
################################################################################

class StoredContentHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassBackgroundCheck)
			if not container.hasViewPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   User must have access to the report.
			if not container.hasAnyPermission(container.getConfigDict().get('storedReportPermissions', [])):
				raise excUtils.MPSValidationException("Operation not permitted")

			container.loadInstance()
			content = fileRepoSQL._decodeContent(str(container.getBackgroundCheck().get('report_content', '')))

			env = envUtils.getEnvironment()
			dstFilePath = env.createGeneratedOutputFileInFolderPath('CBC')
			f = None
			try:
				f = open(dstFilePath, 'wb')
				f.write(bytearray(content))
				f.flush()
			finally:
				if f:
					try: f.close()
					except Exception, e: pass

			self.redirect(env.getUxGeneratedOutputFilePath(dstFilePath))

		finally:
			self.closeConnection()



################################################################################
#   Statusing Handlers.
################################################################################

class StatusingSubmissionErrorHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleSubmissionError'
		kwargs['responseSuffix'] = ' Submission Error'
		self._postImpl(**kwargs)

	def fillBackgroundCheckDict(self, _backgroundCheckDict, _container, _now, _username):
		super(StatusingSubmissionErrorHandler, self).fillBackgroundCheckDict(_backgroundCheckDict, _container, _now, _username)
		_backgroundCheckDict['submitted_date'] = _now
		_backgroundCheckDict['submitted_error'] = 'System-generated Submission error'


class StatusingInProgressHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleInProgress'
		kwargs['responseSuffix'] = ' In Progress'
		self._postImpl(**kwargs)


class StatusingCompleteHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleComplete'
		kwargs['responseSuffix'] = ' Completed'
		self._postImpl(**kwargs)

	def fillBackgroundCheckDict(self, _backgroundCheckDict, _container, _now, _username):
		super(StatusingCompleteHandler, self).fillBackgroundCheckDict(_backgroundCheckDict, _container, _now, _username)
		_backgroundCheckDict['completed_date'] = _now


class StatusingCompleteWithFindingsHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleCompleteWithFindings'
		kwargs['responseSuffix'] = ' Completed with Findings'
		self._postImpl(**kwargs)

	def fillBackgroundCheckDict(self, _backgroundCheckDict, _container, _now, _username):
		super(StatusingCompleteWithFindingsHandler, self).fillBackgroundCheckDict(_backgroundCheckDict, _container, _now, _username)
		_backgroundCheckDict['completed_date'] = _now
		_backgroundCheckDict['flagged'] = True


class StatusingWaiveHandler(AbstractBackgroundCheckHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['backgroundCheckServiceMethodName'] = 'handleWaive'
		kwargs['responseSuffix'] = ' Waived'
		self._postImpl(**kwargs)


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/backgroundcheck/submit/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", SubmitHandler),
	(r"/appt/jobaction/backgroundcheck/accept/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", AcceptHandler),
	(r"/appt/jobaction/backgroundcheck/acceptfindings/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", AcceptWithFindingsHandler),
	(r"/appt/jobaction/backgroundcheck/reject/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", RejectHandler),
	(r"/appt/jobaction/backgroundcheck/submissionerror/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", StatusingSubmissionErrorHandler),
	(r"/appt/jobaction/backgroundcheck/inprogress/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", StatusingInProgressHandler),
	(r"/appt/jobaction/backgroundcheck/complete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", StatusingCompleteHandler),
	(r"/appt/jobaction/backgroundcheck/completefindings/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", StatusingCompleteWithFindingsHandler),
	(r"/appt/jobaction/backgroundcheck/waive/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", StatusingWaiveHandler),
	(r"/appt/jobaction/backgroundcheck/storedreport/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", StoredContentHandler),
	(r"/appt/jobaction/backgroundcheck/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", BackgroundCheckOverviewHandler),
]
