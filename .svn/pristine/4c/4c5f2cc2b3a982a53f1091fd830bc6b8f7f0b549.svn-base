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
import MPSAppt.services.jobPostingService as jobPostingService
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractJobPostingHandler(absHandler.AbstractHandler):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassJobPosting)
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
			self.validateFormData(formData,container)

			jobPostingDict = {}
			jobPostingDict['posting_number'] = formData.get('posting_number','')
			jobPostingDict['date_posted'] = formData.get('date_posted','')
			jobPostingDict['job_task_id'] = jobTask.get('id',-1)
			jobPostingDict['created'] = now
			jobPostingDict['updated'] = now
			jobPostingDict['lastuser'] = username
			jobPostingService.JobPostingService(connection).handleSubmit(jobAction,jobTask,jobPostingDict,container,self.getProfile(),doCommit = True)
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _formData, _container):
		jErrors = []
		for  field_def in _container.getConfigDict().get('prompts', []):
			fieldValue = _formData.get(field_def.get('code',''),'')
			if field_def.get('data_type','').upper() == 'STRING':
				fieldValue = fieldValue.strip()
				if not fieldValue:
					jErrors.append({'code':field_def.get('code',''), 'field_value': fieldValue, 'message': "Required"})
			if field_def.get('data_type','').upper() == 'DATE':
				try:
					if field_def.get('required',True) or len(fieldValue) > 0:
						format = self.getDateFormat(field_def.get('date_format','M/D/Y').strip())
						parsed = dateUtils.flexibleDateMatch(fieldValue, format)
						_formData[field_def.get('code','')] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
				except Exception, e:
					jErrors.append({'code':field_def.get('code',''), 'field_value': fieldValue, 'message': "Invalid Date"})
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


	def getDateFormat(self,configFormat):
		if configFormat.upper() == 'Y/M/D':
			return  self.getSiteYearMonthDayFormat()
		elif configFormat.upper() == 'M/Y':
			return self.getSiteYearMonthFormat()
		return self.getSiteYearMonthDayFormat()


class CompleteHandler(AbstractJobPostingHandler):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassJobPosting)
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
			jobposting = container.getJobPosting()
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['jobposting'] = jobposting
			context['taskcode'] = taskcode
			context['remainingPostingDays'] = container.getRemainingPostingDays()
			context.update(container.getEditContext(self.getSitePreferences()))
			self.convertDatesForUI(jobposting,container)
			context['prompts'] = container.getDataDict({}).get('promptsDict',{})
			self.render("jobPosting.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self._impl(**kwargs)


	def convertDatesForUI(self,jobPostingDict,container):
		for item in container.getConfigDict().get('prompts',{}):
			if item.get('data_type','') == 'date':
				dateFormat = item.get('date_format','')
				if dateFormat:
					datePref = self.getDateFormat(dateFormat)
					if datePref:
						dateString = jobPostingDict.get(item.get('code',''),'')
						if dateString:
							formattedValue = dateUtils.parseDate(dateString,datePref)
							jobPostingDict[item.get('code','')] = formattedValue
					item['date_format'] = dateUtils.mungeDatePatternForDisplay(datePref)


# #   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/jobposting/complete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
	(r"/appt/jobaction/jobposting/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),

]
