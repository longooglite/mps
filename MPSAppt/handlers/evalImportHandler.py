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
#   Import an Evaluator.
################################################################################

class EvalImportHandler(absHandler.AbstractEvalHandler):
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
			context.update(container.getEditContextImport(self.getSitePreferences()))

			self.render("evalImport.html", context=context, skin=context['skin'])

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
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)

			if (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			now = self.getEnvironment().formatUTCDate()
			nbrImported = 0
			formData = tornado.escape.json_decode(self.request.body)
			if container.getConfigDict().get('internalEvaluatorImport',False):
				keys = []
				for key in formData:
					if formData.get(key) == 'true':
						keys.append(int(key))
				if len(keys) > 0:
					jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)
					for key in keys:
						try:
							evaluationsSvc.EvaluationsService(connection).importInternalEvaluator(jobAction, jobTask, container, key, self.getProfile(), now, username)
							nbrImported += 1
						except Exception, e:
							pass
			else:
				importList = self.identifyImports(formData)
				if importList:

					#   Find or create the Job Task.

					jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

					#   Import the Evaluators.

					for twoTuple in importList:
						srcTaskCode = twoTuple[0]
						srcIdx = twoTuple[1]
						try:
							evaluationsSvc.EvaluationsService(connection).importEvaluator(jobAction, jobTask, container, srcTaskCode, srcIdx, self.getProfile(), now, username)
							nbrImported += 1
						except Exception, e:
							pass

			if nbrImported:
				self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict("%i Evaluators imported" % nbrImported)
			responseDict['success'] = True
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def identifyImports(self, _formData):
		#   Return a list of 2-tuples.
		#   Each 2-tuple contains a task code and a row index number.

		importList = []
		for key in _formData.keys():
			if key.startswith('import|'):
				splits = key.split('|')
				if len(splits) == 3:
					try:
						taskCode = splits[1]
						if taskCode:
							idx = int(splits[2])
							twoTuple = (taskCode, idx)
							importList.append(twoTuple)
					except Exception, e:
						pass

		return importList


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/evaluations/import/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", EvalImportHandler),
]
