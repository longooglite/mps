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
import MPSAppt.services.fileRepoService as fileUploadSvc


################################################################################
#   Manipulate an Evaluator's Evaluation.
################################################################################

class EvalFileHandler(absHandler.AbstractEvalHandler):
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
			context.update(container.getEditContextFile(int(evaluatorid), self.getSitePreferences()))
			self.write(tornado.escape.json_encode(context['eval_upload_item']))

		finally:
			self.closeConnection()


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		#self.writePostResponseHeaders()
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

			#   Must have a file of the proper type.

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

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   File Upload.

			activityLogFlag = container.getConfigDict().get('activityLog',{}).get('enabled', False)
			container.getConfigDict().get('activityLog',{})['enabled'] = False

			fileRepoDict = {}
			fileRepoDict['job_task_id'] = jobTask.get('id',None)
			fileRepoDict['seq_nbr'] = evaluatorid
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
			evaluatorDict['id'] = evaluatorid
			evaluatorDict['uploaded'] = True
			evaluatorDict['uploaded_date'] = now
			evaluatorDict['uploaded_username'] = username
			evaluatorDict['uploaded_comment'] = ''
			evaluatorDict['uploaded_file_repo_seq_nbr'] = evaluatorid
			evaluatorDict['created'] = now
			evaluatorDict['updated'] = now
			evaluatorDict['lastuser'] = username
			container.getConfigDict().get('activityLog',{})['enabled'] = activityLogFlag
			evaluationsSvc.EvaluationsService(connection).handleFileUpload(jobAction, jobTask, evaluatorDict, container, self.getProfile(), {}, now, username)

			responseDict = {}
			responseDict['success'] = True
			responseDict['successMsg'] = 'File Uploaded'
			responseDict['escapedResponseStr'] = tornado.escape.json_encode(responseDict)
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['responseDict'] = responseDict
			self.render("uploadResult.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/evaluations/upload/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalFileHandler),
]
