# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import re
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.disclosureService as disclosureSvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.stringUtilities as stringUtils

class AbstractDisclosureHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


class DisclosureHandler(AbstractDisclosureHandler):
	logger = logging.getLogger(__name__)


	#   GET renders an HTML fragment that is shown inside the current work frame.

	def get(self, **kwargs):
		try:
			self._getImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getImpl(self, **kwargs):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassDisclosure)
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

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context.update(container.getEditContext(self.getSitePreferences()))

			#   Assemble parts and pieces to render the page.

			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load(context.get('templateName', ''))
			variableContent = template.generate(context=context, skin=context['skin'])

			prologue = self.render_string("disclosurePrologue.html", context=context, skin=context['skin'])
			epilogue = self.render_string("disclosureEpilogue.html", context=context, skin=context['skin'])
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassDisclosure)
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

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)
			isCrook = stringUtils.interpretAsTrueFalse(formData.get('crook', 'false'))
			offenses = []
			if isCrook:
				offenses = self.validateOffenses(formData, container, now, username)

			disclosureDict = {}
			disclosureDict['job_task_id'] = jobTask.get('id',None)
			disclosureDict['has_disclosures'] = isCrook
			disclosureDict['offenses'] = offenses
			disclosureDict['created'] = now
			disclosureDict['updated'] = now
			disclosureDict['lastuser'] = username
			disclosureSvc.DisclosureService(connection).handleSubmit(jobAction, jobTask, disclosureDict, container, self.getProfile(), now, username)

			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateOffenses(self, _formData, _container, _now, _username):
		reorgData = self.reorgOffenseFormData(_formData)
		self.removeEmptyOffenses(reorgData)

		jErrors = []
		if not reorgData:
			jErrors.append({'code':'crook', 'field_value': '', 'message': "At least one Offense is required"})
		else:
			requiredFieldList = self.getRequiredFieldList(_container)
			for offenseNbr in reorgData.keys():
				offenseDict = reorgData[offenseNbr]
				for fieldCode in requiredFieldList:
					val = offenseDict.get(fieldCode, '')
					if not val:
						key = "%s_%s" % (fieldCode, str(offenseNbr))
						jErrors.append({'code':key, 'field_value': '', 'message': "Required"})

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

		finalList = []
		newOffenseNbr = 0
		for formOffenseNbr in reorgData.keys():
			newOffenseNbr += 1
			formOffenseDict = reorgData[formOffenseNbr]
			for offenseKey in formOffenseDict.keys():
				offenseDict = {}
				offenseDict['offense_nbr'] = newOffenseNbr
				offenseDict['offense_key'] = offenseKey
				offenseDict['offense_value'] = formOffenseDict[offenseKey]
				offenseDict['created'] = _now
				offenseDict['updated'] = _now
				offenseDict['lastuser'] = _username
				finalList.append(offenseDict)
		return finalList

	def reorgOffenseFormData(self, _formData):

		#   Returns a dictionary of offense data from the submitted form data, organized by Offense Number.
		#   key = offense nbr (int)
		#   value = offense data field codes and values (dict)

		reorgData = {}
		pattern = r'(?P<offensekey>[^_]*)_(?P<offensenbr>[0-9]*$)'
		reObj = re.compile(pattern)

		for keyName in _formData.keys():
			match = reObj.match(keyName)
			if match:
				offenseKey = match.groupdict().get('offensekey','')
				offenseNbr = int(match.groupdict().get('offensenbr','0'))
				if (offenseKey) and (offenseNbr):
					offenseDict = reorgData.get(offenseNbr, None)
					if not offenseDict:
						offenseDict = {}
						reorgData[offenseNbr] = offenseDict
					offenseDict[offenseKey] = _formData.get(keyName, '').strip()
		return reorgData

	def removeEmptyOffenses(self, _reorgData):
		keysToDelete = []
		for offenseNbr in _reorgData.keys():
			offenseDict = _reorgData[offenseNbr]
			allBlank = True
			for val in offenseDict.values():
				if val:
					allBlank = False
			if allBlank:
				keysToDelete.append(offenseNbr)

		for offenseNbr in keysToDelete:
			del _reorgData[offenseNbr]

	def getRequiredFieldList(self, _container):
		required = []
		prompts = _container.getConfigDict().get('prompts', [])
		for each in prompts:
			if (each.get('enabled', False)) and (each.get('required', False)):
				required.append(each.get('code', ''))
		return required



#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/disclosure/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", DisclosureHandler),
]
