# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractEvalHandler as absHandler
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.evaluationsService as evaluationsSvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.mpsMath as mpsMath

################################################################################
#   Add an Evaluator.
#   Edit an Evaluator.
################################################################################

class AbstractAddEditHandler(absHandler.AbstractEvalHandler):
	logger = logging.getLogger(__name__)


	#   GET renders an HTML fragment that is shown inside the current work frame.

	def _getImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Evaluator is required for Edit.

		isAdd = kwargs.get('add', False)
		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		evaluatorid = kwargs.get('evaluatorid', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return
		if (not isAdd) and (not evaluatorid):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)

			if (not container.hasViewPermission()) and (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['taskcode'] = taskcode
			context['jobactionid'] = jobactionid
			context['is_add'] = isAdd
			context['states'] = lookupTableSvc.getCodeDescrListByKey(connection, 'cv_static_lookup', 'STATES', 'lookup_key', code='code',descr='descr')
			context['countries'] = lookupTableSvc.getCodeDescrListByKey(connection, 'cv_static_lookup', 'COUNTRIES', 'lookup_key', code='code',descr='descr')
			context['programs'] = lookupTableSvc.getCodeDescrListByKey(connection, 'cv_static_lookup', 'PROGRAMS', 'lookup_key', code='code',descr='descr')

			container.loadInstance()
			evaluatorDict = container.findEvaluatorById(mpsMath.getIntFromString(evaluatorid))
			self.convertDatesForUI(evaluatorDict,container)
			if isAdd:
				context.update(container.getEditContextAdd(self.getSitePreferences()))
			else:
				context['evaluatorid'] = evaluatorid
				context.update(container.getEditContextEdit(int(evaluatorid), self.getSitePreferences()))

			self.render("evalAddEdit.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def convertDatesForUI(self,evaluatorDict,container):
		for item in container.getConfigDict().get('prompts',{}):
			if item.get('data_type','') == 'date':
				dateFormat = item.get('date_format','')
				if dateFormat:
					datePref = self.getDateFormat(dateFormat)
					if datePref:
						dateString = evaluatorDict.get(item.get('code',''),'')
						if dateString:
							formattedValue = dateUtils.parseDate(dateString,datePref)
							evaluatorDict[item.get('code','')] = formattedValue
					item['date_format'] = dateUtils.mungeDatePatternForDisplay(datePref)


	#   POST handles form submissions.

	def _postImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Evaluator is required for Edit.

		isAdd = kwargs.get('add', False)
		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		evaluatorid = kwargs.get('evaluatorid', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return
		if (not isAdd) and (not evaluatorid):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassEvaluations)

			if (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)
			self.validateFormData(connection, formData, container)

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			#   Add the Evaluator.

			evaluatorDict = {}
			evaluatorDict['job_task_id'] = jobTask.get('id',None)
			if not isAdd:
				evaluatorDict['id'] = evaluatorid
			evaluatorDict['evaluator_source_id'] = formData.get('evaluator_source_id',None)
			evaluatorDict['evaluator_type_id'] = formData.get('evaluator_type_id',None)
			evaluatorDict['first_name'] = formData.get('first_name','')
			evaluatorDict['middle_name'] = formData.get('middle_name','')
			evaluatorDict['last_name'] = formData.get('last_name','')
			evaluatorDict['suffix'] = formData.get('suffix','')
			evaluatorDict['email'] = formData.get('email','')
			evaluatorDict['phone'] = formData.get('phone','')
			evaluatorDict['salutation'] = formData.get('salutation','')
			evaluatorDict['degree'] = formData.get('degree','')
			evaluatorDict['titles'] = formData.get('titles','')
			evaluatorDict['institution'] = formData.get('institution','')
			evaluatorDict['reason'] = formData.get('reason','')
			evaluatorDict['emailed_key'] = self.getEnvironment().generateUniqueId()
			evaluatorDict['address_lines'] = formData.get('address_lines','')
			evaluatorDict['city'] = formData.get('city','')
			evaluatorDict['state'] = formData.get('state','')
			evaluatorDict['postal'] = formData.get('postal','')
			evaluatorDict['country'] = formData.get('country','')
			evaluatorDict['admission_date'] = formData.get('admission_date','')
			evaluatorDict['program'] = formData.get('program','')
			evaluatorDict['created'] = now
			evaluatorDict['updated'] = now
			evaluatorDict['lastuser'] = username

			evaluationsSvc.EvaluationsService(connection).handleAddEditEvaluator(jobAction, jobTask, evaluatorDict, container, self.getProfile(), formData, now, username)
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict("Evaluator "  + kwargs.get('responseSuffix',''))
			responseDict['success'] = True
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


	def getDateFormat(self,configFormat):
		if configFormat.upper() == 'Y/M/D':
			return  self.getSiteYearMonthDayFormat()
		elif configFormat.upper() == 'M/Y':
			return self.getSiteYearMonthFormat()
		return self.getSiteYearMonthDayFormat()



	def validateFormData(self, _connection, _formData, _container):
		jErrors = []

		#   Check required fields.
		for  fieldDict in _container.getConfigDict().get('prompts', []):
			fieldCode = fieldDict.get('code', '')
			fieldValue = _formData.get(fieldCode, '')
			if type(fieldValue) is unicode or type(fieldValue) is str:
				fieldValue = _formData.get(fieldCode, '').strip()
				if (fieldDict.get('required', False)) and (fieldDict.get('enabled', True)):
					if not fieldValue:
						jErrors.append({ 'code': fieldCode, 'field_value': fieldValue, 'message': "Required" })

			if fieldDict.get('data_type','').upper() == 'LIST':
				if type(fieldValue) is str:
					_formData[fieldDict.get('code','')] = [fieldValue]
			else:
				#   assume string
				_formData[fieldDict.get('code','')] = fieldValue

			if fieldDict.get('data_type','').upper() == 'DATE':
				try:
					if (fieldDict.get('enabled',True) and fieldDict.get('required',True)) or len(fieldValue) > 0:
						format = self.getDateFormat(fieldDict.get('date_format','M/D/Y').strip())
						parsed = dateUtils.flexibleDateMatch(fieldValue, format)
						_formData[fieldDict.get('code','')] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
				except Exception, e:
					jErrors.append({'code':fieldDict.get('code',''), 'field_value': fieldValue, 'message': "Invalid Date"})


		#   Map evaluator_source
		value = _formData.get('evaluator_source', '')
		if value:
			sourceDict = lookupTableSvc.getEntityByKey(_connection, 'wf_evaluator_source', value, _key='code')
			if sourceDict:
				_formData['evaluator_source_id'] = sourceDict.get('id', 0)
			else:
				jErrors.append({ 'code': 'evaluator_source', 'field_value': value, 'message': "Unknown Evaluator Source" })

		#   Map evaluator_type
		value = _formData.get('evaluator_type', '')
		if value:
			typeDict = lookupTableSvc.getEntityByKey(_connection, 'wf_evaluator_type', value, _key='code')
			if typeDict:
				_formData['evaluator_type_id'] = typeDict.get('id', 0)
			else:
				jErrors.append({ 'code': 'evaluator_type', 'field_value': value, 'message': "Unknown Evaluator Type" })

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


class EvalAddHandler(AbstractAddEditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['add'] = True
		self._getImpl(**kwargs)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['add'] = True
		kwargs['responseSuffix'] = 'added'
		self._postImpl(**kwargs)


class EvalEditHandler(AbstractAddEditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['add'] = False
		self._getImpl(**kwargs)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['add'] = False
		kwargs['responseSuffix'] = 'changed'
		self._postImpl(**kwargs)


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/evaluations/add/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", EvalAddHandler),
	(r"/appt/jobaction/evaluations/edit/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<evaluatorid>[^/]*)", EvalEditHandler),
]
