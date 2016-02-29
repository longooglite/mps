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
import MPSAppt.services.evaluationsService as evaluationsSvc


################################################################################
#   Delete an Evaluator.
#   Decline an Evaluator.
#   Review an Evaluator.
################################################################################

class AbstractDeleteDeclineReviewHandler(absHandler.AbstractEvalHandler):
	logger = logging.getLogger(__name__)


	#   GET renders an HTML fragment that is shown inside the current work frame.

	def _getImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Evaluator is required.

		isDelete = kwargs.get('is_delete', False)
		isDecline = kwargs.get('is_decline', False)
		isReview = kwargs.get('is_review', False)
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

			if isDelete:
				context.update(container.getEditContextDelete(int(evaluatorid), self.getSitePreferences()))
			if isDecline:
				context.update(container.getEditContextDecline(int(evaluatorid), self.getSitePreferences()))
			if isReview:
				context.update(container.getEditContextReview(int(evaluatorid), self.getSitePreferences()))
			self.render(kwargs.get('htmlFilename',''), context=context, skin=context['skin'])

		finally:
			self.closeConnection()


	#   POST handles form submissions.

	def _impl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Evaluator Id is required.

		isDelete = kwargs.get('is_delete', False)
		isDecline = kwargs.get('is_decline', False)
		isReview = kwargs.get('is_review', False)
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

			if (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if isReview:
				if (not self.hasAnyPermission(container.getConfigDict().get('reviewPermissions',[]))):
					raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Delete the Evaluator.

			evaluatorDict = {}
			evaluatorDict['job_task_id'] = jobTask.get('id',None)
			evaluatorDict['id'] = evaluatorid
			evaluatorDict['updated'] = now
			evaluatorDict['lastuser'] = username
			self.getSpecificEvaluatorInfo(container, evaluatorDict, formData)

			actionString = '''evaluationsSvc.EvaluationsService(connection).%s(jobAction, jobTask, evaluatorDict, container, self.getProfile(), formData, now, username)''' % kwargs.get('serviceMethodName','')
			exec actionString
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict("Evaluator "  + kwargs.get('responseSuffix',''))
			responseDict['success'] = True
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def getSpecificEvaluatorInfo(self, _container, _evaluatorDict, _formdata):
		return {}


class EvalDeleteHandler(AbstractDeleteDeclineReviewHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = True
		kwargs['is_decline'] = False
		kwargs['is_review'] = False
		kwargs['htmlFilename'] = "evalDelete.html"
		self._getImpl(**kwargs)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = True
		kwargs['is_decline'] = False
		kwargs['is_review'] = False
		kwargs['serviceMethodName'] = 'handleDeleteEvaluator'
		kwargs['responseSuffix'] = 'deleted'
		self._impl(**kwargs)


class EvalDeclineHandler(AbstractDeleteDeclineReviewHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = False
		kwargs['is_decline'] = True
		kwargs['is_review'] = False
		kwargs['htmlFilename'] = "evalDecline.html"
		self._getImpl(**kwargs)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = False
		kwargs['is_decline'] = True
		kwargs['is_review'] = False
		kwargs['serviceMethodName'] = 'handleDeclineEvaluator'
		kwargs['responseSuffix'] = 'declined'
		self._impl(**kwargs)

	def getSpecificEvaluatorInfo(self, _container, _evaluatorDict, _formdata):
		_evaluatorDict['declined'] = True
		_evaluatorDict['declined_date'] = _evaluatorDict.get('updated', '')
		_evaluatorDict['declined_username'] = _evaluatorDict.get('lastuser', '')
		_evaluatorDict['declined_comment'] = ''

		commentKey = _container.getConfigDict().get('declineCommentCode', '')
		if commentKey:
			_evaluatorDict['declined_comment'] = _formdata.get(commentKey, '')


class EvalReviewHandler(AbstractDeleteDeclineReviewHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = False
		kwargs['is_decline'] = False
		kwargs['is_review'] = True
		kwargs['htmlFilename'] = "evalReview.html"
		self._getImpl(**kwargs)


class EvalReviewApprovedHandler(AbstractDeleteDeclineReviewHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = False
		kwargs['is_decline'] = False
		kwargs['is_review'] = True
		kwargs['serviceMethodName'] = 'handleApproveDenyEvaluator'
		kwargs['responseSuffix'] = 'approved'
		self._impl(**kwargs)

	def getSpecificEvaluatorInfo(self, _container, _evaluatorDict, _formdata):
		_evaluatorDict['approved'] = True
		_evaluatorDict['approved_date'] = _evaluatorDict.get('updated', '')
		_evaluatorDict['approved_username'] = _evaluatorDict.get('lastuser', '')
		_evaluatorDict['approved_comment'] = ''

		commentKey = _container.getConfigDict().get('reviewCommentCode', '')
		if commentKey:
			_evaluatorDict['approved_comment'] = _formdata.get(commentKey, '')


class EvalReviewDeniedHandler(AbstractDeleteDeclineReviewHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['is_delete'] = False
		kwargs['is_decline'] = False
		kwargs['is_review'] = True
		kwargs['serviceMethodName'] = 'handleApproveDenyEvaluator'
		kwargs['responseSuffix'] = 'denied'
		self._impl(**kwargs)

	def getSpecificEvaluatorInfo(self, _container, _evaluatorDict, _formdata):
		_evaluatorDict['approved'] = False
		_evaluatorDict['approved_date'] = _evaluatorDict.get('updated', '')
		_evaluatorDict['approved_username'] = _evaluatorDict.get('lastuser', '')
		_evaluatorDict['approved_comment'] = ''

		commentKey = _container.getConfigDict().get('reviewCommentCode', '')
		if commentKey:
			_evaluatorDict['approved_comment'] = _formdata.get(commentKey, '')


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/evaluations/delete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalDeleteHandler),
	(r"/appt/jobaction/evaluations/decline/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalDeclineHandler),
	(r"/appt/jobaction/evaluations/review/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalReviewHandler),
	(r"/appt/jobaction/evaluations/approve/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalReviewApprovedHandler),
	(r"/appt/jobaction/evaluations/deny/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalReviewDeniedHandler),
]
