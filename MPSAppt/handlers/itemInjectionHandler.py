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
import MPSAppt.services.itemInjectionService as itemInjectorService
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import json

class ItemInjectionHandler(absHandler.AbstractHandler):
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
			self.handleGetException(e, self.logger)

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
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassItemInjector)
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

			formData = tornado.escape.json_decode(self.request.body)

			injectionDict = {}
			injectionDict['job_task_id'] = jobTask.get('id',-1)
			injectionDict['task_codes'] = self.getTaskCodes(formData,container)
			injectionDict['created'] = now
			injectionDict['updated'] = now
			injectionDict['lastuser'] = username

			itemInjectorService.ItemInjectionService(connection).handleSubmit(jobAction,jobTask,injectionDict,container,self.getProfile())

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def getTaskCodes(self,formData,container):
		selectedTaskCodes = {}
		injectibles = container.containerDict.get('config',{}).get('items',{})
		numItems = len(injectibles)
		i = 1
		while i <= numItems:
			key = 'set' + str(i)
			if formData.get(key,'') == 'selected':
				selectedTaskCodes[key] = injectibles.get(key,[])
			i+=1
		return json.dumps(selectedTaskCodes)


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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassItemInjector)
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

			container.loadInstance()
			config = container.containerDict.get('config',{})
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['items'] = self.getItems(workflow,container)
			context.update(container.getEditContext(self.getSitePreferences()))
			self.render("itemInjector.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

	def getItems(self,workflow,container):
		returnVal = []
		descriptors = container.containerDict.get('config',{}).get('itemdescriptors')
		taskCodes = container.injectedItemDict.get('task_codes',None)
		previouslyInjectedItemDict = {}
		if taskCodes:
			previouslyInjectedItemDict = json.loads(container.injectedItemDict.get('task_codes'))
		numItems = len(descriptors)
		i = 0
		while i < numItems:
			i += 1
			key = 'set%i' % (i)
			descriptor = descriptors.get(key,[])
			selected = False
			if previouslyInjectedItemDict.get(key,None):
				selected = True
			returnVal.append({"descr":descriptor,"value":key,"selected":selected})
		return returnVal

# #   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/injectitems/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", ItemInjectionHandler),

]
