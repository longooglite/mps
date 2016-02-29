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
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.qaService as qaSVC
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.dateUtilities as dateUtils

class CompleteHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
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

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassQuestionsAndAnswers)

			if (not container.hasViewPermission()) and (not container.hasEditPermission()):
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			jobTask = jaService.getJobTask(jobAction,container)
			if jobTask is None:
				jobTask = {}
			qaService = qaSVC.QAService(connection)
			container.loadInstance()
			questions = container.getQA().get('questionsAndAnswers',{})
			responses = qaService.getResponsesToQuestions(jobTask.get('id',0),taskcode)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context.update(container.getCommonEditContext(self.getSitePreferences()))
			context['prompts'] = container.getPrompts()
			date_responses = self.convertDatesForUI(context['prompts'],container,questions,responses)
			context["date_responses"] = date_responses
			context['questionAndAnswers'] = questions
			context['dateFieldIdentifiers'] = container.getConfigDict().get('dateFieldIdentifiers',{})
			context['question_responses'] = responses
			context['save_as_draft_url'] = container.getDataDict({}).get('save_as_draft_url','')
			self.render("QAForm.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def convertDatesForUI(self,prompts,container,questions,responses):
		date_responses = {}
		for question in questions:
			if question.get('code','') in container.getConfigDict().get('dateFieldIdentifiers',''):
				dateFormat = prompts.get(question.get('code','')).get('date_format','')
				if dateFormat:
					datePref = self.getDateFormat(dateFormat)
					if datePref:
						response = responses.get(question.get('id',-1))
						if response:
							dateString = response.get('text_response','')
							formattedValue = dateUtils.parseDate(dateString,datePref)
							responses.get(question.get('id',-1))['text_response'] = formattedValue
							date_responses[question.get('code','')] = formattedValue
					prompts[question.get('code','')]['date_format'] = dateUtils.mungeDatePatternForDisplay(datePref)
		return date_responses


	def getDateFormat(self,configFormat):
		if configFormat.upper() == 'Y/M/D':
			return  self.getSiteYearMonthDayFormat()
		elif configFormat.upper() == 'M/Y':
			return self.getSiteYearMonthFormat()
		return self.getSiteYearMonthDayFormat()


	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		saveAsDraft = kwargs.get('draft',False)

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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassQuestionsAndAnswers)
			if not container.hasEditPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			now = self.getEnvironment().formatUTCDate()
			qaService = qaSVC.QAService(connection)

			formData = tornado.escape.json_decode(self.request.body)
			qas = qaService.getQuestionsAndOptionsForTask(container.getCode())
			if not saveAsDraft:
				self.validateFormData(formData,qas,container.containerDict.get('config'),container.getPrompts())

			qaSvcDataList = self.getDataForSubmissionToQAService(taskcode,formData,qas,now,username)
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)
			qaService.handleSubmit(jobAction, jobTask, qaSvcDataList, container, self.getProfile(), now, username, not saveAsDraft, doCommit=True)
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = self.getSuccessMessage(container,saveAsDraft)
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def getSuccessMessage(self,container,isDraft):
		if isDraft:
			return container.containerDict.get('successMsgDraft','')
		else:
			return container.containerDict.get('successMsg','')


	def getDataForSubmissionToQAService(self,taskCode,formData,questionsAndPrompts,now,username):
		qaList = []
		for qp in questionsAndPrompts:
			questionCode = qp.get('code','')
			options = qp.get('options',[])
			if options:
				for opt in options:
					qaItem = self.getNewQAItem(taskCode,questionCode,now,username)
					optCode = opt.get('code','')
					qaItem['optioncode'] = optCode
					qaItem['textresponse'] = ''
					if formData.has_key('opt_' + questionCode):
						selected_value = formData.get('opt_' + questionCode,'')
						if selected_value == opt.get('option_text',''):
							qaItem['textresponse'] = formData.get(optCode,'')
							qaList.append(qaItem)
			else:
				if formData.get(questionCode,''):
					qaItem = self.getNewQAItem(taskCode,questionCode,now,username)
					qaItem['textresponse'] = formData.get(questionCode,'')
					qaList.append(qaItem)
		return qaList

	def getNewQAItem(self,taskCode,questioncode,now,username):
		return {"taskcode":taskCode,"questioncode":questioncode,"optioncode":"","textresponse":"","created":now,"updated":now,"lastuser":username}

	def validateFormData(self, responses, qas, configDict, prompts, saveAsDraft = False):
		jErrors = []
		if not saveAsDraft:
			for q in qas:
				if q.get('code','') in configDict.get('dateFieldIdentifiers',[]):
					fieldValue = responses.get(q.get('code',''))
					if fieldValue:
						format = self.getDateFormat(prompts.get(q.get('code',{})).get('date_format',''))
						parsed = dateUtils.flexibleDateMatch(fieldValue, format)
						responses[q.get('code','')] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
				if q.get('options',[]):
					foundResponse = False
					currentCode = ''
					for option in q.get('options',[]):
						currentCode = 'opt_' + q.get('code','')
						if responses.get(currentCode,'') and responses.get(currentCode,'') == option.get('option_text',''):
							if option.get('text_required',True):
								currentCode = option.get('code','')
								if responses.get(currentCode,'').strip():
									foundResponse = True
									break
							else:
								foundResponse = True
								break
					if not foundResponse:
						jErrors.append({'code':currentCode, 'field_value': '', 'message': "Required"})
				else:
					foundResponse = True
					currentCode = q.get('code','')
					if q.get('required',True):
						if not responses.get(currentCode):
							foundResponse = False
					if not foundResponse:
						jErrors.append({'code':currentCode, 'field_value': '', 'message': "Required"})
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

class DraftHandler(CompleteHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			kwargs['draft'] = True
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/qa/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", CompleteHandler),
	(r"/appt/jobaction/qadraft/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", DraftHandler),
]
