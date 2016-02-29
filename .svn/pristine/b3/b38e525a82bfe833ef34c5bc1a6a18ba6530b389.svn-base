# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.fieldLevelRevisionsService as revisionsService
import MPSAppt.utilities.environmentUtils as envUtils

class AbstractFieldLevelRevisionsHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


class FieldLevelRevisionsHandler(AbstractFieldLevelRevisionsHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def get(self, **kwargs):
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

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassUberForm)

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			formData = tornado.escape.json_decode(self.request.body)
			comment = formData.get('comment','')
			fieldname = formData.get('name','')
			enabled = formData.get('enabled',True)
			revisionDict = {'jobactionId':jobAction.get('id'),"task_code":taskcode,"fieldname":fieldname,"comment":comment,"enabled":enabled}

			frService = revisionsService.FieldLevelRevisions(connection)
			frService.handleSubmit(jobAction, jobTask, revisionDict, container, self.getProfile(), now, username)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = ''

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

class FieldLevelRevisionsNotificationHandler(AbstractFieldLevelRevisionsHandler):
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
		self.verifyAnyPermission(['revisions_notify'])

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			now = self.getEnvironment().formatUTCDate()

			containerCode = workflow.getMainContainer().getContainerDict().get('config',{}).get('FLRR_Container','Renee')
			container = workflow.getContainer(containerCode)
			if not container:
				self.redirect("/appt")
				return

			frService = revisionsService.FieldLevelRevisions(connection)
			frService.handleNotifySubmit(jobAction,{"task_code":"revisions"}, container, self.getProfile(), now, username)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = ''
			responseDict['redirect'] = '/appt/jobaction/%s' % str(jobactionid)

			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['revisions_notify'])

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())

			frService = revisionsService.FieldLevelRevisions(connection)
			revisions = frService.getFieldLevelRevisionsForJobAction(jobAction)
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['revisionsList'] = self.getRevisionsList(revisions,workflow)
			context['job_action_id'] = jobAction.get('id',-1)
			self.render("fieldRevisions.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def getRevisionsList(self,revisions,workflow):
		itemList = []
		for revision in revisions:
			if not revision.get('when_notified',''):
				container = workflow.getContainer(revision.get('task_code',''))
				if container:
					container.loadInstance()
					item = container.getRevisionsRequiredDescriptors(revision.get('field_name',''))
					if item:
						item['comment'] = revision.get('comment','')
						itemList.append(item)
		return itemList

#   AJAX call from UI to determine whether or not to display the revisions available for notification button
class FieldLevelRevisionsAvailableHandler(AbstractFieldLevelRevisionsHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		ableToNotify = True
		try:
			self.verifyAnyPermission(['revisions_notify'])
		except:
			ableToNotify = False

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			revisions = None
			if ableToNotify:
				frService = revisionsService.FieldLevelRevisions(connection)
				revisions = frService.getFieldLevelRevisionsReadyForNotificationForJobAction(jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['revisionsAvailable'] = True if revisions else False
			responseDict['successMsg'] = ''

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/fieldlevelrevisions/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", FieldLevelRevisionsHandler),
	(r"/appt/jobaction/revisionsnotification/(?P<jobactionid>[^/]*)", FieldLevelRevisionsNotificationHandler),
	(r"/appt/jobaction/revisionsavailable/(?P<jobactionid>[^/]*)", FieldLevelRevisionsAvailableHandler),
]
