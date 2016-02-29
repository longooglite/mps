# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.confirmTitleService as confirmTitleSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.titleService as titleSVC
import MPSAppt.services.departmentService as deptSvc

import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractConfirmTitleHandler(absHandler.AbstractHandler):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassConfirmTitle)
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
			container.loadInstance()

			confirmedTitleDict = {}
			confirmedTitleDict['title_id'] = formData.get('track_title_list',None)
			confirmedTitleDict['department_id'] = formData.get('department_list',None)
			confirmedTitleDict['job_task_id'] = jobTask.get('id',-1)
			confirmedTitleDict['created'] = now
			confirmedTitleDict['updated'] = now
			confirmedTitleDict['lastuser'] = username
			confirmTitleSvc.ConfirmedTitleService(connection).handleSubmit(jobAction, jobTask, confirmedTitleDict, container, self.getProfile(), now, username)

			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			container.setIsLoaded(False)
			container.loadInstance()
			if container.isComplete():
				responseDict['successMsg'] = container.containerDict.get('successMsg','')
			else:
				responseDict['successMsg'] = "Title cannot be left open"

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

class CompleteHandler(AbstractConfirmTitleHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassConfirmTitle)
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
			titleId = container.confirmedTitleDict.get('title_id','')
			departmentId = container.confirmedTitleDict.get('department_id','')

			secondaryAppointmentMode = container.getConfigDict().get('secondaryAppointmentMode',False)
			if secondaryAppointmentMode:
				titlesList = titleSVC.TitleService(connection).getTitlesByTrack()
				departmentList = deptSvc.DepartmentService(connection).getDepartmentHierarchy(['NoUserRestriction'], _excludeInactive=True)
			else:
				titleDict = lookupTableSvc.getEntityByKey(connection, 'wf_title', appointment.get('title_id',0), _key='id')
				titlesList,metatrackId = titleSVC.TitleService(connection).getTitlesOnEquivalentMetaTrack(titleDict)
				departmentList = {}

			selectedTitleId = appointment.get('title_id',0) if not titleId else titleId
			selectedDepartmentId = appointment.get('dept_id',0) if not departmentId else departmentId

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['track_title_selection'] = titlesList
			context['department_selection'] = departmentList
			context['selected_appt_dept_id'] = selectedDepartmentId
			context['selected_appt_title_id'] = selectedTitleId
			context['secondary_appointment_mode'] = secondaryAppointmentMode
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context.update(container.getEditContext(self.getSitePreferences()))
			self.render("confirmTitle.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self._impl(**kwargs)



#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/confirmtitle/complete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
	(r"/appt/jobaction/confirmtitle/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
]
