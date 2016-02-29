# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.completionService as completionSvc
import MPSAppt.services.terminationService as terminationSvc


class AbstractCompletionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


class CompletionHandler(AbstractCompletionHandler):
	logger = logging.getLogger(__name__)

	#   GET renders an HTML fragment that is shown inside the current frame.

	def get(self, **kwargs):
		try:
			self._getImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

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

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassCompletion)
			container.loadInstance()

			if (not container.hasViewPermission()) and (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['include_termination'] = container.containerDict.get('config',{}).get('termination',False)
			context['termination_types'] = terminationSvc.TerminationService(connection).getTerminationTypes()
			context['termination_type_id'] = container.completionDict.get('termination_type_id',-1)
			context['date_format'] = "M/D/YYYY"
			context['data-confirm-msg'] = 'Please confirm. You cannot undo this action.'
			context.update(container.getEditContext(self.getSitePreferences()))
			self._convertOneDate(context, 'effective')
			self._convertOneDate(context, 'scheduled')
			self.render("completion.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def _convertOneDate(self, _context, _key):
		value = _context.get(_key, '')
		if value:
			_context[_key] = self.convertMDYToDisplayFormat(value)


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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassCompletion)
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

			#   Date inputs must be valid dates, or the magic phrase 'now'.

			formData = tornado.escape.json_decode(self.request.body)
			self.validateFormData(formData)

			#   Find or create the Job Task.
			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreateJobTask(jobAction, container, now, username)

			terminationTypeId = None if not formData.get('termination_type',None) else formData.get('termination_type',-1)
			completionDict = {}
			completionDict['job_task_id'] = jobTask.get('id',None)
			completionDict['effective_date'] = formData.get('effectiveDate','')
			completionDict['scheduled_date'] = formData.get('scheduledDate','')
			completionDict['complete'] = False
			completionDict['termination_type_id'] = terminationTypeId
			completionDict['created'] = now
			completionDict['updated'] = now
			completionDict['lastuser'] = username
			completionSvc.CompletionService(connection).handleSubmit(jobAction, jobTask, completionDict, container, self.getProfile(), formData, now, username)

			self.updateRosterStatusForJobAction(connection, jobAction)
			responseDict = self.getPostResponseDict("Scheduled for Completion")
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _formData):
		jErrors = []

		fieldValue = _formData.get('effective_date','')
		try:
			_formData['effectiveDate'] = self.parseDate(fieldValue, 'Effective Date')
		except Exception, e:
			jErrors.append({'code':'effective_date', 'field_value': fieldValue, 'message': "Invalid Effective Date"})

		fieldValue = _formData.get('scheduled_date','')
		try:
			_formData['scheduledDate'] = self.parseDate(fieldValue, 'Scheduled Date')
		except Exception, e:
			jErrors.append({'code':'scheduled_date', 'field_value': fieldValue, 'message': "Invalid Scheduled Date"})

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def parseDate(self, _displayValue, _fieldDescr):

		#   Verify that the given date is one of:
		#       - a valid year-month-day, or
		#       - the magic phrase 'now', or
		#       - a blank value, which implies 'now'
		#
		#   An objection is thrown if a valid value is not found.
		#   Otherwise, the valid date in YYYY-MM-DD format is returned.

		strippedValue = _displayValue.strip()
		if not strippedValue:
			return self.getNow()
		if strippedValue.upper() == 'NOW':
			return self.getNow()

		try:
			parsed = dateUtils.flexibleDateMatch(_displayValue, self.getSiteYearMonthDayFormat())
			return "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
		except Exception, e:
			raise excUtils.MPSValidationException("Invalid %s" % _fieldDescr)

	def getNow(self):
		return dateUtils.formatUTCDateOnly()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/completion/complete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompletionHandler),
]
