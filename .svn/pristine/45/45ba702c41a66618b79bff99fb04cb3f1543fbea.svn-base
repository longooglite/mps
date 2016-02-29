# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import os
import shutil


import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.npiService as npiSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils
import MPSCore.utilities.PDFUtils as pdfUtils

class AbstractNPIHandler(absHandler.AbstractHandler):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassNPI)
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
			formData = tornado.escape.json_decode(self.request.body)
			container.loadInstance()
			existingNPIDict = container.getDataDict({})

			npiDict = {}
			npiDict['agree'] = stringUtils.interpretAsTrueFalse(formData.get('agree',"off"))
			npiDict['does_not_have_npi'] = stringUtils.interpretAsTrueFalse(formData.get('nodohavenpi',"off"))
			npiDict['npi_username'] = formData.get('npi_username','')
			npiDict['npi_password'] = formData.get('npi_password','')
			npiDict['npi_nbr'] = formData.get('npi_nbr',"")
			npiDict['created'] = now
			npiDict['updated'] = now
			npiDict['lastuser'] = username
			if formData.get('npi_password','').find('*') >= 0:
				formData['npi_password'] = existingNPIDict.get('npi_password','')

			self.validateFormData(npiDict)
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)
			npiDict['jobTaskId'] = jobTask.get('id',-1)

			npiSvc.NPIService(connection).handleSubmit(jobAction, jobTask, npiDict, container, self.getProfile(), now, username)

			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, npiDict):
		jErrors = []
		if not npiDict.get('agree',False):
			jErrors.append({'code':"agree", 'field_value':"", 'message': "Required"})
		if not npiDict.get('does_not_have_npi',False):
			if not npiDict.get('npi_nbr','').strip():
				jErrors.append({'code':"npi_nbr", 'field_value':"", 'message': "Required"})
			if not npiDict.get('npi_username','').strip():
				jErrors.append({'code':"npi_username", 'field_value':"", 'message': "Required"})
			if not npiDict.get('npi_password','').strip():
				jErrors.append({'code':"npi_password", 'field_value':"", 'message': "Required"})
			if not self.luhn_check(npiDict.get('npi_nbr','').strip()):
				jErrors.append({'code':"npi_nbr", 'field_value':"", 'message': "Invalid NPI number"})
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def luhn_check(self,input):
		if not len(input) == 10 and input.isdigit():
			return False
		first = input[0:1]
		if (first != "1" and first != "2"):
			return False
		input = '80840' + input
		i,sum = 0,0
		while i < 13:
			sum += int(input[i:i+1])
			i += 2
		delta = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
		i = 1
		while i < 14:
			sum += delta[int(input[i:i+1])]
			i += 2
		returnVal = ((sum * 9) % 10) == int(input[14:15])
		return returnVal

class CompleteHandler(AbstractNPIHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._impl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['complete'] = True
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassNPI)
			if not container.hasEditPermission() and not container.hasViewPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			appointment = jaService.getAppointment(jobAction.get('appointment_id',-1))
			if not appointment:
				responseDict = self.getPostResponseDict('Unable to locate appointment')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			templateName = container.containerDict.get('config',{}).get('form','')
			form = self.buildFullPathToSiteTemplate(templateName)
			person = personSvc.PersonService(connection).getPerson(jobAction.get('person_id'))
			candidate_name = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			path = self.buildFullPathToSiteTemplate(container.getConfigDict().get('npipdf',''),self.getProfile().get('siteProfile',{}).get('site',''))
			pdfPath = self.CopyNPIFormToTmp(path)
			fillePdfPath = pdfUtils.autofillPDF(pdfPath,container.getConfigDict().get('formfillPDFMapping',[]))
			appendData = '(' + person.get('username','') + ') ' + candidate_name
			nameAddedPdfPath = pdfUtils.appendToPDFFooter(fillePdfPath,appendData,container.getConfigDict().get('pdfUserNamePageNbrs',[]))
			container.getConfigDict()['npipdf'] = nameAddedPdfPath

			container.loadInstance()
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['candidate_name'] = candidate_name
			npiDict = container.getNPI()
			if not self.hasPermission("canViewNPIPassword"):
				npipassword = ''
				for each in npiDict.get('npi_password',''):
					npipassword += '*'
				npiDict['npi_password'] = npipassword
			context['npi'] = npiDict
			context['npi_pdf_form'] = container.getConfigDict().get('npipdf','')
			context['form'] = form
			context.update(container.getEditContext(self.getSitePreferences()))

			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load(context['form'])
			variableContent = template.generate(context=context)

			prologue = self.render_string("genericPrologue.html", context=context, skin=context['skin'])
			epilogue = self.render_string("genericEpilogue.html", context=context, skin=context['skin'])
			self.finish(''.join([prologue, variableContent, epilogue]))

		finally:
			self.closeConnection()

	def CopyNPIFormToTmp(self,pdfPath):
		unmodFileName = coreEnvUtils.CoreEnvironment().generateUniqueId() + '.pdf'
		destPath = "%s%s%s%s%s" % (os.sep,"tmp",os.sep,"pdf",os.sep)
		try:
			os.makedirs(destPath)
		except Exception,e:
			pass
		shutil.copyfile(pdfPath,destPath + unmodFileName)
		return destPath + unmodFileName


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/npi/complete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
	(r"/appt/jobaction/npi/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
]
