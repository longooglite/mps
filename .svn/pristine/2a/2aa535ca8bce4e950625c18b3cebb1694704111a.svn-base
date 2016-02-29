# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import os

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.attestService as attestSvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.dateUtilities as dateUtils

class AbstractAttestHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _impl(self, **kwargs):
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
			container = self.validateTaskCode(workflow, taskcode, [constants.kContainerClassAttest, constants.kContainerClassPersonalInfoSummary])
			if not container.hasEditPermission() and not container.hasViewPermission():
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

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			container.loadInstance()
			attestDict = container.getAttestation()

			attestor_name,attestor_department = container.getNameAndDepartment()
			formData = tornado.escape.json_decode(self.request.body)
			self.validateFormData(formData,container)
			attestDict['job_task_id'] = jobTask.get('id',None)
			attestDict['attestor_name'] = attestor_name
			attestDict['attestor_department'] = attestor_department
			attestDict['complete'] = True
			attestDict['created'] = now
			attestDict['updated'] = now
			attestDict['lastuser'] = username
			attestSvc.AttestService(connection).handleSubmit(jobAction, jobTask, attestDict, container, self.getProfile(), now, username)

			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg')

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _formData, _container):
		jErrors = []
		for field_def in _container.getConfigDict().get('prompts', []):
			if (field_def.get('code','') == 'attest') and (field_def.get('enabled',False)):
				if not _formData.has_key('attest'):
					jErrors.append({'code':'attest', 'field_value': '', 'message': "Required"})
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


class CompleteHandler(AbstractAttestHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

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

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, [constants.kContainerClassAttest, constants.kContainerClassPersonalInfoSummary])
			if not container.hasEditPermission() and not container.hasViewPermission():
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

			container.loadInstance()
			attestation = container.getAttestation()
			attestation['attest'] = str(attestation.get('complete',False))
			templateName = container.containerDict.get('config',{}).get('form','')
			form = self.buildFullPathToSiteTemplate(templateName)
			now = self.getEnvironment().formatUTCDate()

			context = self.getInitialTemplateContext(envUtils.getEnvironment())

			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['attest'] = attestation
			context['form'] = form
			context.update(container.getEditContext(self.getSitePreferences()))

			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load(context['form'])
			variableContent = template.generate(context=context)

			prologue = self.render_string("attestPrologue.html", context=context, skin=context['skin'])
			epilogue = self.render_string("attestEpilogue.html", context=context, skin=context['skin'])
			self.finish(''.join([prologue, variableContent, epilogue]))

		finally:
			self.closeConnection()

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['complete'] = True
		self._impl(**kwargs)


class PrintHandler(AbstractAttestHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

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

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, [constants.kContainerClassAttest, constants.kContainerClassPersonalInfoSummary])
			if not container.hasEditPermission() and not container.hasViewPermission():
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

			container.loadInstance()
			attestation = container.getAttestation()
			attestation['attest'] = str(attestation.get('complete',False))
			templateName = container.containerDict.get('config',{}).get('form','')
			form = self.buildFullPathToSiteTemplate(templateName)
			now = self.getEnvironment().formatUTCDate()

			context = self.getInitialTemplateContext(envUtils.getEnvironment())

			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['attest'] = attestation
			context['form'] = form
			context['printtitle'] = container.getDescr()
			submitDate = attestation.get('updated','')
			if submitDate:
				submitDate = dateUtils.localizeUTCDate(submitDate,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('timezone',''))
				submitDate = dateUtils.parseDate(submitDate,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('ymdformat',''))
			context['submit_date'] = submitDate
			context.update(container.getEditContext(self.getSitePreferences(),True))

			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load(context['form'])
			variableContent = template.generate(context=context)
			prologue = self.render_string("attestProloguePrint.html", context=context, skin=context['skin'])
			epilogue = self.render_string("attestEpiloguePrint.html", context=context, skin=context['skin'])
			html = prologue+variableContent+epilogue
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.getEnvironment(), setFooter=True, prefix = 'uberOut_')
			self.redirect(pdf)

		finally:
			self.closeConnection()

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['complete'] = True
		self._impl(**kwargs)


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/attest/complete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
	(r"/appt/jobaction/attest/print/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", PrintHandler),
	(r"/appt/jobaction/attest/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
]
