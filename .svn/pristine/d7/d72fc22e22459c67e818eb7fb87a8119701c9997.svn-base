# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.handlers.uberFormHelper as uberHelper
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.uberDisplayService as uberDisplaySvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.fieldLevelRevisionsService as fieldLevelRevisionsSvc

class AbstractUberFormHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	#   POST implementation, used for both 'Save' and 'Save as Draft'.

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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassUberForm)
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

			#   Validate form data.

			isDraft = kwargs.get('draft', False)
			isAddSavedSet = kwargs.get('addSavedSet', False)
			helper = uberHelper.UberFormHelper(self)
			formData, repeatingGroupData = helper.processUberFormData(container, **kwargs)

			#   Construct data and persist.

			responseDict = self.getPostResponseDict()
			if isAddSavedSet:
				savedSetDict = self.buildSavedSetDict(container, formData, now, community, username)
				savedSetItemList = self.buildSavedSetItems(container, formData, repeatingGroupData, now, username)
				uberSvc.UberService(connection).handleCreateSavedSet(jobAction, jobTask, savedSetDict, savedSetItemList, container, self.getProfile(), now, community, username)
				responseDict['success'] = True
				responseDict['successMsg'] = container.getConfigDict().get('savedSetsCreateSuccessMsg', '')
				responseDict['reloadForm'] = True
			else:
				insertList, updateList, deleteList = helper.identifyDataChanges(container, formData, repeatingGroupData)
				uberSvc.UberService(connection).handleSubmit(jobAction, jobTask, insertList, updateList, deleteList, container, isDraft, self.getProfile(), now, username)
				self.updateRosterStatusForJobAction(connection, jobAction)

				#   UberForm components can be shared across Job Actions.
				#   If this Job Action is related to other Job Actions, update their roster statuses as well.
				relatedJobActionIds = jaService.getRelatedJobActions(jobAction.get('id', 0))
				for relatedId in relatedJobActionIds:
					self.updateRosterStatusForJobAction(connection, { 'id': relatedId })

				responseDict['success'] = True
				responseDict['successMsg'] = container.containerDict.get('successMsg','')

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


	#   POST workers.

	def buildSavedSetDict(self, _container, _formData, _now, _community, _username):
		return {}

	def buildSavedSetItems(self, _container, _formData, _repeatingGroupData, _now, _username):
		return []


class UberHandler(AbstractUberFormHandler):
	logger = logging.getLogger(__name__)


	#   GET renders an HTML page allowing the user to interact with the Uber Form.

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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassUberForm)
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

			container.setIsLoaded(False)
			workflow.clearJobTaskCache()
			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode

			frService = fieldLevelRevisionsSvc.FieldLevelRevisions(connection)
			revisions = frService.getFieldLevelRevisionsForJobAction(jobAction,True)

			fieldLevelRevisable,canSeeFieldLevelRevisions = container.isFieldLevelRevisable(revisions)

			context['isFieldLevelRevisable'] = fieldLevelRevisable
			context['canSeeFieldLevelRevisions'] = canSeeFieldLevelRevisions

			context['RevisionsRequiredFieldNames'] = []
			revisionsList = []
			for revision in revisions:
				if taskcode == revision.get('task_code',''):
					revItem = {}
					revItem['name'] = revision.get('field_name','')
					revItem['comment'] = revision.get('comment','')
					revisionsList.append(revItem)
			context['RevisionsRequiredFieldNames'] = revisionsList

			context.update(container.getEditContext(self.getSitePreferences()))
			self.render("uber.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['draft'] = False
		self._impl(**kwargs)


class DraftHandler(AbstractUberFormHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['draft'] = True
		self._impl(**kwargs)


class AddSavedSetHandler(AbstractUberFormHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['draft'] = True
		kwargs['addSavedSet'] = True
		self._impl(**kwargs)

	def buildSavedSetDict(self, _container, _formData, _now, _community, _username):
		savedSetDict = {}
		savedSetDict['community'] = _community
		savedSetDict['username'] = _username
		savedSetDict['group_code'] = _container.getConfigDict().get('questionGroupCode', '')
		savedSetDict['descr'] = _formData.get('saved_set_name', '')
		savedSetDict['created'] = _now
		savedSetDict['updated'] = _now
		savedSetDict['lastuser'] = _username
		return savedSetDict

	def buildSavedSetItems(self, _container, _formData, _repeatingGroupData, _now, _username):

		#   Convert form responses in _formData and _repeatingGroupData into Saved Set Items.
		#   All responses are treated as 'Adds', we delete any existing responses prior to saving.

		insertList = []
		_container.loadInstance()
		uberInstance = _container.getUberInstance()
		questions = uberInstance.get('questions', {})

		#   First pass: responses to questions that are NOT in repeating groups.

		flatQuestionList = _container.flattenUberQuestions(questions)
		for uberQuestionDict in flatQuestionList:
			if not uberQuestionDict.get('repeating', False):
				code = uberQuestionDict.get('code', '')
				newResponseText = _formData.get(code, None)
				if newResponseText:
					responseDict = {}
					responseDict['question_code'] = code
					responseDict['repeat_seq'] = 0
					responseDict['response'] = newResponseText
					responseDict['created'] = _now
					responseDict['updated'] = _now
					responseDict['lastuser'] = _username
					insertList.append(responseDict)

		#   Second pass: responses to questions that ARE IN repeating groups.

		for uberGroupDict in _container.flattenUberRepeatingGroups(questions):
			groupCode = uberGroupDict.get('code', '')
			if groupCode:
				occurrencesForGroup = _repeatingGroupData[groupCode]
				for uberContainer in uberGroupDict.get('elements', []):
					if uberContainer.get('type', '') == uberSvc.kElementTypeQuestion:
						questionCode = uberContainer.get('code', '')
						if questionCode:
							for occurrenceNbr in sorted(occurrencesForGroup.keys()):
								occurrenceDict = occurrencesForGroup[occurrenceNbr]
								responseDict = {}
								responseDict['question_code'] = questionCode
								responseDict['repeat_seq'] = int(occurrenceNbr)
								responseDict['response'] = occurrenceDict.get(questionCode, '')
								responseDict['created'] = _now
								responseDict['updated'] = _now
								responseDict['lastuser'] = _username
								insertList.append(responseDict)

		return insertList


class ApplySavedSetHandler(AbstractUberFormHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Set Id is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		setid = kwargs.get('setid', '')
		if not jobactionid or not taskcode or not setid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassUberForm)
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

			#   Find the requested Saved Set.

			uberSoivice = uberSvc.UberService(connection)
			savedSetDict = uberSoivice.getUberSavedSet(setid)
			if not savedSetDict:
				raise excUtils.MPSValidationException("Saved set not found")

			#   Construct data and persist.

			uberSoivice.handleApplySavedSet(jobAction, jobTask, savedSetDict, container, self.getProfile(), now, username)
			self.updateRosterStatusForJobAction(connection, jobAction)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.getConfigDict().get('savedSetsApplySuccessMsg', '')
			responseDict['reloadForm'] = True

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


class DeleteSavedSetHandler(AbstractUberFormHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.
		#   Set Id is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		setid = kwargs.get('setid', '')
		if not jobactionid or not taskcode or not setid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassUberForm)
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

			#   Delete the specified Saved Set.

			savedSetDict = { 'id': setid }
			uberSvc.UberService(connection).handleDeleteSavedSet(jobAction, jobTask, savedSetDict, container, self.getProfile(), now, username)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.getConfigDict().get('savedSetsDeleteSuccessMsg', '')
			responseDict['reloadForm'] = True

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

class UberPDFHandler(AbstractUberFormHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form submissions.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
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
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassUberForm)
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

			candidateName = ''
			person = personSvc.PersonService(connection).getPerson(jobAction.get('person_id',None))
			if person:
				candidateName = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			uberDispSvc = uberDisplaySvc.UberDisplayService(connection)
			context['uberContent'] = uberDispSvc.getContent(container,self.profile.get('siteProfile',{}).get('sitePreferences',{}))
			context['header'] = container.containerDict.get('header','')
			context['candidateName'] = candidateName
			context.update(container.getEditContext(self.getSitePreferences()))
			loader = self.getEnvironment().getTemplateLoader()
			template = loader.load('uberPrint.html')
			html = template.generate(context=context)
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.getEnvironment(), setFooter=True, prefix = 'uberOut_')
			self.redirect(pdf)
		finally:
			self.closeConnection()



#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/uberform/apply/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<setid>[^/]*)", ApplySavedSetHandler),
	(r"/appt/jobaction/uberform/delete/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)/(?P<setid>[^/]*)", DeleteSavedSetHandler),
	(r"/appt/jobaction/uberform/add/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", AddSavedSetHandler),
	(r"/appt/jobaction/uberform/submit/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", UberHandler),
	(r"/appt/jobaction/uberform/draft/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", DraftHandler),
	(r"/appt/jobaction/uberform/pdf/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", UberPDFHandler),
	(r"/appt/jobaction/uberform/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", UberHandler),
]
