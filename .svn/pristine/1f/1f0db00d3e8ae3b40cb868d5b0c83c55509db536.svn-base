# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.fileRepoService as fileUploadSvc
import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.cvImporterService as cvImporter
import MPSAppt.services.personService as personSvc


class AbstractFileHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def getSuccessMsg(self, container,action):
		return container.containerDict.get('header',"") + " was " + action

class FileUploadHandler(AbstractFileHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):

		#   This POST handler is different from the 'normal' POST handlers for this application.
		#   It is submitted by the browser via a 'submit' button that POSTs through an IFRAME..
		#   It does not go through our normal jquery submission process.
		#   Therefore, some of the processing paradigms are different.

		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)
			self.doRedirect("An error occurred")

	def _postHandlerImpl(self, **kwargs):
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Sequence Number is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		seqnbr = kwargs.get('seqnbr', '')
		if not jobactionid or not taskcode or not seqnbr:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassFileUpload)
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				# File upload errors in MPSAppt go to uploadResult.html as a JS(json) object:
				jResponse = self._jsonUploadErrorResponse('Upload not allowed')
				self.render("uploadResult.html", context=jResponse, skin='default')
				#self.doFriendlyRedirect("Upload not allowed", jobactionid)
				return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			uniqname = ''
			uniqCommunity = ''
			candidate = personSvc.PersonService(connection).getPerson(workflow.jobActionDict.get('person_id',-1))
			if candidate:
				uniqname = candidate.get('username','')
				uniqCommunity = candidate.get('community', '')

			importFromCV = False
			if importFromCV and uniqname and uniqCommunity:
				filename,fileContents,fileContentType,pdfversion,pages = self.importCV(connection,uniqCommunity,uniqname,container)
			else:
				#   Must have a file of the proper type.
				fileData = self.request.files.get('file_data', [])
				if not fileData:
					# File upload errors in MPSAppt go to uploadResult.html as a JS(json) object:
					jResponse = self._jsonUploadErrorResponse('No file provided')
					self.render("uploadResult.html", context=jResponse, skin='default')
					return

				fileObject = fileData[0]
				message,pages,pdfversion = self.validatePDFOrImageContent(fileObject,container)
				if message:
					# File upload errors in MPSAppt go to uploadResult.html as a JS(json) object:
					jResponse = self._jsonUploadErrorResponse(message)
					self.render("uploadResult.html", context=jResponse, skin='default')
					return

				fileContents = fileObject.body
				filename = fileObject.filename
				fileContentType = fileObject.content_type

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			fileRepoDict = {}
			fileRepoDict['job_task_id'] = jobTask.get('id',None)
			fileRepoDict['seq_nbr'] = seqnbr
			fileRepoDict['pages'] = pages
			fileRepoDict['pdf_version_nbr'] = pdfversion
			fileRepoDict['file_name'] = filename
			fileRepoDict['content'] = bytearray(fileContents)
			fileRepoDict['content_type'] = fileContentType
			fileRepoDict['created'] = now
			fileRepoDict['updated'] = now
			fileRepoDict['lastuser'] = username
			fileUploadSvc.FileRepoService(connection).handleUpload(jobAction, jobTask, fileRepoDict, container, self.getProfile(), now, username)

			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict('File uploaded')
			responseDict['success'] = True
			responseDict['successMsg'] = self.getSuccessMsg(container,"uploaded")
			responseDict['escapedResponseStr'] = tornado.escape.json_encode(responseDict)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['responseDict'] = responseDict
			self.render("uploadResult.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def importCV(self,_connection,_uniqCommunity,_uniquename,_container):
		filename = '%s_cv.pdf' % (_uniquename)
		fileContentType = 'application/pdf'
		payload = self.getInitialPayload()
		payload['community'] = _uniqCommunity
		payload['username'] = _uniquename
		cvSubject = self.postToAuthSvc("/getuser", payload)

		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		uiPath,fullPath = cvImporter.CVImporterService(_connection).getCVForUser(cvSubject,context,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}),self.getEnvironment())
		pdffile = open(fullPath,'rb')
		fileContents = bytearray(pdffile.read())
		pdffile.close()
		message,pages,pdfversion = self.validatePDFOrImageContent(fileContents,_container)
		return filename,fileContents,fileContentType,pdfversion,pages

	def _jsonUploadErrorResponse(self, message):
		context = {}
		responseDict = {}
		responseDict['error'] = message
		responseDict['escapedResponseStr'] = tornado.escape.json_encode(responseDict)
		context['responseDict'] = responseDict
		return context


class FileDownloadHandler(AbstractFileHandler):
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
		#   Sequence Number is required.
		#   Version Number is optional.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		seqnbr = kwargs.get('seqnbr', '')
		versionnbr = kwargs.get('versionnbr', None)
		if not jobactionid or not taskcode or not seqnbr:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, [constants.kContainerClassFileUpload,constants.kContainerClassEvaluations])
			if not container.hasViewPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			jobTask = jaService.getJobTask(jobAction, container)
			if not jobTask:
				raise excUtils.MPSValidationException("Job Task not found")

			if versionnbr:
				content = fileUploadSvc.FileRepoService(connection).getFileRepoContentForVersion(jobTask, seqnbr, versionnbr)
			else:
				content = fileUploadSvc.FileRepoService(connection).getFileRepoContent(jobTask, seqnbr)

			env = envUtils.getEnvironment()
			f = None
			try:
				dstFilePath = env.createGeneratedOutputFileInFolderPath(content.get('file_name',''))
				f = open(dstFilePath, 'wb')
				f.write(bytearray(content.get('content',[])))
				f.flush()
			finally:
				if f:
					try: f.close()
					except Exception, e: pass

			self.writeJobActionLog(connection, jobAction, jobTask, container, constants.kJobActionLogVerbDownload, content.get('file_name',''))
			self.redirect(env.getUxGeneratedOutputFilePath(dstFilePath))

		finally:
			self.closeConnection()


class FileDeleteHandler(AbstractFileHandler):
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
		#   Sequence Number is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		seqnbr = kwargs.get('seqnbr', '')
		if not jobactionid or not taskcode or not seqnbr:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, [constants.kContainerClassFileUpload,constants.kContainerClassEvaluations])
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict("Delete not allowed")
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getJobTask(jobAction, container)
			fileRepoDict = fileUploadSvc.FileRepoService(connection).getFileRepo(jobTask, seqnbr)
			fileName = fileRepoDict.get('file_name','') if fileRepoDict else ''

			fileRepoDict = {}
			fileRepoDict['job_task_id'] = jobTask.get('id',None)
			fileRepoDict['seq_nbr'] = seqnbr
			fileRepoDict['file_name'] = fileName
			fileRepoDict['created'] = now
			fileRepoDict['updated'] = now
			fileRepoDict['lastuser'] = username
			fileUploadSvc.FileRepoService(connection).handleDelete(jobAction, jobTask, fileRepoDict, container, self.getProfile(), now, username)
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict('File deleted')
			responseDict['success'] = True
			responseDict['successMsg'] = self.getSuccessMsg(container,"deleted")

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


#   All URL mappings for this module.
urlMappings = [
	(r"/appt/jobaction/file/upload/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<seqnbr>[^/]*)", FileUploadHandler),
	(r"/appt/jobaction/file/download/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<seqnbr>[^/]*)/(?P<versionnbr>[^/]*)", FileDownloadHandler),
	(r"/appt/jobaction/file/download/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<seqnbr>[^/]*)", FileDownloadHandler),
	(r"/appt/jobaction/file/delete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<seqnbr>[^/]*)", FileDeleteHandler),
]
