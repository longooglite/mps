# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc


class AbstractApprovalHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

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
			container = self.validateTaskCode(workflow, taskcode, kwargs.get('containerClassName', ''))

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
			if container.getConfigDict().get('data-confirm-msg',''):
				context['data-confirm-msg'] = 'Please confirm. You cannot undo this action.'
			self.convertDatesForUI(container.approvalDict,container)
			context.update(container.getEditContext(self.getSitePreferences()))
			self.render(kwargs.get('htmlFilename', ''), context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def convertDatesForUI(self,itemDict,container):
		for item in container.getConfigDict().get('prompts',{}):
			if item.get('data_type','') == 'date':
				dateFormat = item.get('date_format','')
				if dateFormat:
					datePref = self.getDateFormat(dateFormat)
					if datePref:
						dateString = itemDict.get(item.get('code',''),'')
						if dateString:
							formattedValue = dateUtils.parseDate(dateString,datePref)
							itemDict[item.get('code','')] = formattedValue
					item['date_format'] = dateUtils.mungeDatePatternForDisplay(datePref)

	def getDateFormat(self,configFormat):
		if configFormat.upper() == 'Y/M/D':
			return  self.getSiteYearMonthDayFormat()
		elif configFormat.upper() == 'M/Y':
			return self.getSiteYearMonthFormat()

		return self.getSiteYearMonthDayFormat()

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
			container = self.validateTaskCode(workflow, taskcode, kwargs.get('containerClassName', ''))
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict(kwargs.get('blockedMessage', 'Operation not permitted'))
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#	when doing internal secondaries, the faculty that was chosen for the secondary must have a primary with some department
			if container.getConfigDict().get('departmentIdentifier','') == 'personsprimary':
				theDepartment = container.getDepartment()
				if not theDepartment:
					responseDict = self.getPostResponseDict(container.getConfigDict().get('noPrimaryDeptMsg','Secondary appointments can only be created for faculty that has a primary appointment.'))
					responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
					self.write(tornado.escape.json_encode(responseDict))
					return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   Validate input.

			formData = kwargs.get('formData', {})
			self.validateFormData(container, formData)

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Extend a Revisions Required request with named Tasks to freeze.

			revisionsRequiredTaskNameList = kwargs.get('revisionsRequiredTaskNameList', [])
			if revisionsRequiredTaskNameList:
				container.getConfigDict().get('revisionsRequiredFreeze',{}).get('unfreezeTasks',{}).extend(revisionsRequiredTaskNameList)

			approvalDict = {}
			approvalDict['job_task_id'] = jobTask.get('id',None)
			approvalDict['approval'] = kwargs.get('approvalConstant','')
			approvalDict['approval_date'] = formData.get('approval_date','')
			approvalDict['vote_for'] = formData.get('vote_for', 0)
			approvalDict['vote_against'] = formData.get('vote_against', 0)
			approvalDict['vote_abstain'] = formData.get('vote_abstain', 0)
			approvalDict['created'] = now
			approvalDict['updated'] = now
			approvalDict['lastuser'] = username

			import MPSAppt.services.approvalService as approvalSvc
			actionString = '''approvalSvc.ApprovalService(connection).%s(jobAction, jobTask, approvalDict, container, self.getProfile(), formData, now, username)''' % kwargs.get('approvalServiceMethodName','')
			exec actionString
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = self.getSuccessMsg(kwargs.get('approvalServiceMethodName',''),container)
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def getSuccessMsg(self,methodName,container):
		if methodName == 'handleDeny':
			return container.containerDict.get('statusMsgDeny','')
		elif methodName == 'handleSubmit':
			return container.containerDict.get('successMsg','')
		elif methodName == 'handleRevisions':
			return container.containerDict.get('successMsgRevisions','')
		elif methodName == 'handleApprove':
			return container.containerDict.get('successMsgApprove','')
		return ''

	def validateFormData(self, _container, _formData):
		jErrors = []

		configDict = _container.getConfigDict()
		if configDict.get('date', False):
			fieldValue = _formData.get('approval_date','').strip()
			if not fieldValue:
				if configDict.get('dateRequired', False):
					jErrors.append({'code':'approval_date', 'field_value': '', 'message': "Required"})
			else:
				self.parseDate(_formData, 'approval_date', jErrors)
		else:
			_formData['approval_date'] = ''

		self.validateInteger(_formData, 'vote_for', 'Vote For', jErrors)
		self.validateInteger(_formData, 'vote_against', 'Vote Against', jErrors)
		self.validateInteger(_formData, 'vote_abstain', 'Vote Abstain', jErrors)

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def parseDate(self, _formData, _key, _jErrors):
		value = _formData.get(_key, '')
		if not value:
			_formData[_key] = ''
		try:
			parsed = dateUtils.flexibleDateMatch(value, self.getSiteYearMonthDayFormat())
			_formData[_key] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
		except Exception, e:
			_jErrors.append({'code':_key, 'field_value': value, 'message': "Invalid date"})

	def validateInteger(self, _formData, _key, _label, _jErrors):
		if _formData.has_key(_key):
			value = _formData.get(_key, '0')
			if not value:
				_formData[_key] = 0
			try:
				_formData[_key] = int(_formData[_key])
			except Exception, e:
				_jErrors.append({'code':_key, 'field_value': value, 'message': "%s must be a number" % _label})


class SubmitHandler(AbstractApprovalHandler):
	logger = logging.getLogger(__name__)

	#   GET renders an HTML fragment that is shown inside the current frame.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['containerClassName'] = [constants.kContainerClassSubmit, constants.kContainerClassSubmitBackgroundCheck]
		kwargs['htmlFilename'] = "submit.html"
		self._getImpl(**kwargs)


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['containerClassName'] = [constants.kContainerClassSubmit, constants.kContainerClassSubmitBackgroundCheck]
		kwargs['approvalServiceMethodName'] = 'handleSubmit'
		kwargs['blockedMessage'] = 'Submission not allowed'
		kwargs['approvalConstant'] = constants.kApprovalSubmit
		kwargs['responseSuffix'] = ' Submitted'
		kwargs['formData'] = self.removeFormDataNoise()
		self._postImpl(**kwargs)


class ApproveHandler(AbstractApprovalHandler):
	logger = logging.getLogger(__name__)

	#   GET renders an HTML fragment that is shown inside the current frame.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['containerClassName'] = constants.kContainerClassApproval
		kwargs['htmlFilename'] = "approval.html"
		self._getImpl(**kwargs)


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['containerClassName'] = constants.kContainerClassApproval
		kwargs['approvalServiceMethodName'] = 'handleApprove'
		kwargs['blockedMessage'] = 'Approval not allowed'
		kwargs['approvalConstant'] = constants.kApprovalApprove
		kwargs['responseSuffix'] = ' Approved'
		kwargs['formData'] = self.removeFormDataNoise()
		self._postImpl(**kwargs)


class DenyHandler(AbstractApprovalHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['containerClassName'] = constants.kContainerClassApproval
		kwargs['approvalServiceMethodName'] = 'handleDeny'
		kwargs['blockedMessage'] = 'Denial not allowed'
		kwargs['approvalConstant'] = constants.kApprovalDeny
		kwargs['responseSuffix'] = ' Denied'
		kwargs['formData'] = self.removeFormDataNoise()
		self._postImpl(**kwargs)


class RevisionsHandler(AbstractApprovalHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['containerClassName'] = constants.kContainerClassApproval
		kwargs['approvalServiceMethodName'] = 'handleRevisions'
		kwargs['blockedMessage'] = 'Revisions not allowed'
		kwargs['approvalConstant'] = constants.kApprovalRevisionsRequired
		kwargs['responseSuffix'] = ' Revisions Required'
		kwargs['formData'] = self.removeFormDataNoise()
		kwargs['revisionsRequiredTaskNameList'] = self._getRevisionsRequiredTaskNames()
		self._postImpl(**kwargs)

	def _getRevisionsRequiredTaskNames(self):
		formData = self.removeFormDataNoise()
		return formData.keys()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/submit/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", SubmitHandler),
	(r"/appt/jobaction/approval/approve/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", ApproveHandler),
	(r"/appt/jobaction/approval/deny/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", DenyHandler),
	(r"/appt/jobaction/approval/revise/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", RevisionsHandler),
	(r"/appt/jobaction/approval/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", ApproveHandler),
]
