# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import json

import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.serviceAndRankService as SRSvc

class ServiceAndRankHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassServiceAndRank)
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

			now = self.getEnvironment().formatUTCDate()
			formData = tornado.escape.json_decode(self.request.body)

			#   Find or create the Job Task.

			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			srDict = {}
			srDict['building_descr'] = formData.get('building_list','')
			srDict['room'] = formData.get('room','')
			srDict['spc'] = formData.get('spc','')
			srDict['floor'] = formData.get('floor','')
			srDict['reception'] = formData.get('reception','')
			address_lines = formData.get('address_lines','')
			if type(address_lines) is unicode:
				address_lines = [address_lines]
			srDict['address_lines'] = json.dumps(address_lines)
			srDict['city'] = formData.get('city','')
			srDict['state'] = formData.get('state_list','')
			srDict['country'] = formData.get('country_list','')
			srDict['postal'] = formData.get('postal','')
			srDict['phone'] = formData.get('phone','')
			srDict['fax'] = formData.get('fax','')
			srDict['email'] = formData.get('email','')
			srDict['lastuser'] = username
			srDict['created'] = now
			srDict['updated'] = now
			srDict['membership_category'] = formData.get('membership_category_list','')

			self.validateSR(srDict,container.containerDict.get('config',{}).get('prompts',{}))

			SRSvc.ServiceAndRankService(connection).handleSubmit(jobAction,jobTask,srDict,container,self.getProfile(),now,username,True)
			responseDict = self.getPostResponseDict("")
			responseDict['redirect'] = "/appt/jobaction/%s" % jobactionid
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()

	def validateSR(self,srDict,prompts):
		jErrors = []
		for prompt in prompts:
			if prompt.get('required',False):
				value = srDict.get(prompt.get('code',''))
				if prompt.get('data_type','') == 'repeatingtext':
					value = self.stripRepeatingText(value)
				if not value:
					jErrors.append({ 'code': prompt.get('code',''), 'field_value': '', 'message': 'Required' })

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def stripRepeatingText(self,jsonData):
		if jsonData:
			listData = ''
			data = json.loads(jsonData)
			for each in data:
				listData += each
			return listData
		return ''


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

		jobactionid = kwargs.get('jobactionid', '')

		connection = self.getConnection()
		try:

			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassServiceAndRank)
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
			context['submitURL'] = '/appt/jobaction/serviceandrank/'+jobactionid+'/'+taskcode

			context.update(container.getEditContext(self.getSitePreferences()))
			self.render("serviceAndRank.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/serviceandrank/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", ServiceAndRankHandler),
]
