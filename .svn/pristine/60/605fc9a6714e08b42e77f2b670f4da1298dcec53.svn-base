# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.internalEvalService as internalEvalSvc
import MPSAppt.core.sql.evaluationsSQL as evaluationsSQL
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.stringUtilities as stringUtils


class EvaluationsService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)


	#   Basic operations.

	def getEvaluator(self, _evaluatorId):
		evaluatorDict = lookupTableSvc.getEntityByKey(self.connection, 'wf_evaluator', _evaluatorId, _key='id')
		self.unjsonifyEvaluator(evaluatorDict)
		return evaluatorDict

	def getEvaluatorByEmailKey(self, _emailKey):
		evaluatorDict = lookupTableSvc.getEntityByKey(self.connection, 'wf_evaluator', _emailKey, _key='emailed_key')
		self.unjsonifyEvaluator(evaluatorDict)
		return evaluatorDict

	def getEvaluatorsList(self, _jobTaskId,_orderBy="id ASC"):
		evaluatorsList = lookupTableSvc.getEntityListByKey(self.connection, 'wf_evaluator', _jobTaskId, _key='job_task_id', _orderBy="id ASC")
		for evaluatorDict in evaluatorsList:
			self.unjsonifyEvaluator(evaluatorDict)
		return evaluatorsList

	def getReviewersForReviewersList(self,_jobTaskId):
		evalSourceDict = lookupTableSvc.getLookupTable(self.connection,"wf_evaluator_source")
		evaluatorTypes = lookupTableSvc.getLookupTable(self.connection,"wf_evaluator_type")
		evaluatorsReceived = []
		evaluatorsDeclined = []
		evaluators = self.getEvaluatorsList(_jobTaskId,_orderBy="UPPER(lastname),UPPER(firstname)")
		for evaluator in evaluators:
			if evaluator.get('declined',False):
				evaluatorsDeclined.append(evaluator)
			else:
				if evaluator.get('uploaded',False):
					evaluatorsReceived.append(evaluator)
		return {"evaluatorsReceived":evaluatorsReceived,"evaluatorsDeclined":evaluatorsDeclined,"evalSourceDict":evalSourceDict,"evaluatorTypes":evaluatorTypes}

	def createEvaluator(self, _evaluatorDict, doCommit=True):
		self.jsonifyEvaluator(_evaluatorDict)
		evaluationsSQL.createEvaluator(self.connection, _evaluatorDict, doCommit)

	def updateEvaluatorDemographics(self, _evaluatorDict, doCommit=True):
		self.jsonifyEvaluator(_evaluatorDict)
		evaluationsSQL.updateEvaluatorDemographics(self.connection, _evaluatorDict, doCommit)

	def updateEvaluatorEmail(self, _evalEmailDict, doCommit=True):
		evaluationsSQL.updateEvaluatorEmail(self.connection, _evalEmailDict, doCommit)

	def updateEvaluatorApproval(self, _evalApprovalDict, doCommit=True):
		evaluationsSQL.updateEvaluatorApproval(self.connection, _evalApprovalDict, doCommit)

	def updateEvaluatorUpload(self, _evalUploadDict, doCommit=True):
		evaluationsSQL.updateEvaluatorUpload(self.connection, _evalUploadDict, doCommit)

	def updateEvaluatorDeclined(self, _evalDeclinedDict, doCommit=True):
		evaluationsSQL.updateEvaluatorDeclined(self.connection, _evalDeclinedDict, doCommit)


	#   Not-so-Basic operations.

	def updateEvaluator(self, _jobTaskDict, _evaluatorDict, _existingEvaluator, doCommit=True):
		try:
			if _existingEvaluator:
				self.updateEvaluatorDemographics(_evaluatorDict, doCommit=False)
			else:
				self.createEvaluator(_evaluatorDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleAddEditEvaluator(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _profile, _formData, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Evaluator (demographics) table row.
			existingEvaluator = self.getEvaluator(_evaluatorDict.get('id',0))
			self.updateEvaluator(_jobTaskDict, _evaluatorDict, existingEvaluator, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				_container.resolveNames(_evaluatorDict)
				logDict['verb'] = constants.kJobActionLogVerbAddEvaluator
				if existingEvaluator:
					logDict['verb'] = constants.kJobActionLogVerbUpdateEvaluator
				logDict['item'] = _evaluatorDict.get('full_name', _container.getDescr())
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			activityLogConfigKeyName = 'addActivityLog'
			if existingEvaluator:
				activityLogConfigKeyName = 'editActivityLog'
			self._constructActivityLogText(_container, _evaluatorDict, activityLogConfigKeyName)
			dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName=activityLogConfigKeyName,_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleDeleteEvaluator(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _profile, _formData, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Find the Evaluator table row, then delete it.
			existingEvaluator = self.getEvaluator(_evaluatorDict.get('id',0))
			if existingEvaluator:
				evaluationsSQL.deleteEvaluator(self.connection, existingEvaluator, doCommit=False)

				#   Write the Job Action Log entry.
				if _container.getIsLogEnabled():
					_container.resolveNames(existingEvaluator)
					logDict['verb'] = constants.kJobActionLogVerbDelete
					logDict['item'] = existingEvaluator.get('full_name', _container.getDescr())
					logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
					jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

				#   Common handler pre-commit activities.
				self._constructActivityLogText(_container, existingEvaluator, 'deleteActivityLog')
				dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
				self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName='deleteActivityLog',_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleDeclineEvaluator(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _profile, _formData, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Find the Evaluator table row, then delete it.
			existingEvaluator = self.getEvaluator(_evaluatorDict.get('id',0))
			if existingEvaluator:
				evaluationsSQL.updateEvaluatorDeclined(self.connection, _evaluatorDict, doCommit=False)

				#   Write the Job Action Log entry.
				if _container.getIsLogEnabled():
					_container.resolveNames(existingEvaluator)
					logDict['verb'] = constants.kJobActionLogVerbDeclineEvaluator
					logDict['item'] = existingEvaluator.get('full_name', _container.getDescr())
					logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
					jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

				#   Common handler pre-commit activities.
				self._constructActivityLogText(_container, existingEvaluator, 'declineActivityLog')
				dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
				self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName='declineActivityLog',_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleApproveDenyEvaluator(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _profile, _formData, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Find the Evaluator table row, then delete it.
			existingEvaluator = self.getEvaluator(_evaluatorDict.get('id',0))
			if existingEvaluator:
				evaluationsSQL.updateEvaluatorApproval(self.connection, _evaluatorDict, doCommit=False)

				#   Write the Job Action Log entry.
				if _container.getIsLogEnabled():
					_container.resolveNames(existingEvaluator)
					logDict['verb'] = constants.kJobActionLogVerbApproveEvaluator
					if not _evaluatorDict.get('approved', False):
						logDict['verb'] = constants.kJobActionLogVerbDenyEvaluator
					logDict['item'] = existingEvaluator.get('full_name', _container.getDescr())
					logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
					jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

				#   Common handler pre-commit activities.
				activityLogConfigKeyName = 'approveActivityLog'
				if not _evaluatorDict.get('approved', False):
					activityLogConfigKeyName = 'denyActivityLog'
				self._constructActivityLogText(_container, existingEvaluator, activityLogConfigKeyName)
				dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
				self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName=activityLogConfigKeyName,_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSendEmail(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _profile, _formData, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Find the Evaluator table row.
			#   Send the email, and update the Evaluator.
			#   Touch the Job Task to update user and timestamp.
			_evaluatorDict['emailed_email_id'] = None
			existingEvaluator = self.getEvaluator(_evaluatorDict.get('id',0))
			if existingEvaluator:
				if self.getEmailOn(_profile):
					evaluatorId = existingEvaluator.get('id',0)
					sitePreferences = _profile.get('siteProfile', {}).get('sitePreferences', {})
					letterContext = _container.getEditContextSend(evaluatorId, sitePreferences)
					letterContext['skin'] = sitePreferences.get('skin', 'default')

					loader = envUtils.getEnvironment().getTemplateLoader()
					template = loader.load(letterContext.get('emailTemplateName', ''))
					phatBody = template.generate(context=letterContext)
					body = stringUtils.squeeze(phatBody)

					solicitationEmailContext = {}
					solicitationEmailContext['addresses'] = [existingEvaluator.get('email','')]
					solicitationEmailContext['ccAddresses'] = []
					solicitationEmailContext['bccAddresses'] = []
					solicitationEmailContext['body'] = body

					formCC = _formData.get('cc_addresses')
					if formCC:
						solicitationEmailContext['ccAddresses'] = formCC.split(',')

					solicitationEmailContext['subjectLine'] = _formData.get('subject_line', None)
					if not solicitationEmailContext['subjectLine']:
						solicitationEmailContext['subjectLine'] = _container.getConfigDict().get('emailSubjectLine', 'Letter of Recommendation Request')

					import MPSAppt.services.emailService as emailSvc
					emailer = emailSvc.EmailService(self.connection, _jobActionDict, _jobTaskDict, _container, _profile, _username, _now)
					emailId = emailer.prepareAndSendSolicitationEmail(solicitationEmailContext, False)
					_evaluatorDict['emailed_email_id'] = emailId

				evaluationsSQL.updateEvaluatorEmail(self.connection, _evaluatorDict, doCommit=False)

				#   Write the Job Action Log entry.
				if _container.getIsLogEnabled():
					_container.resolveNames(existingEvaluator)
					logDict['verb'] = constants.kJobActionLogVerbSendEvaluatorEmail
					logDict['item'] = existingEvaluator.get('full_name', _container.getDescr())
					logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
					jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

				#   Common handler pre-commit activities.
				self._constructActivityLogText(_container, existingEvaluator, 'sendActivityLog')
				dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
				self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName='sendActivityLog',_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleFileUpload(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _profile, _formData, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Find the Evaluator table row, and update.
			existingEvaluator = self.getEvaluator(_evaluatorDict.get('id',0))
			if existingEvaluator:
				evaluationsSQL.updateEvaluatorUpload(self.connection, _evaluatorDict, doCommit=False)

				#   Write the Job Action Log entry.
				if _container.getIsLogEnabled():
					_container.resolveNames(existingEvaluator)
					logDict['verb'] = constants.kJobActionLogVerbUpload
					logDict['item'] = existingEvaluator.get('full_name', _container.getDescr())
					logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
					jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

				#   Common handler pre-commit activities.
				dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
				self._constructActivityLogText(_container, existingEvaluator, 'uploadActivityLog')
				self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName='uploadActivityLog',_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleFormSubmission(self, _jobActionDict, _jobTaskDict, _evaluatorDict, _container, _isDraft, _profile, _formData, _now, _username, doCommit=True):
		_container.resolveNames(_evaluatorDict)
		fullName = _evaluatorDict.get('full_name', _username)
		_evaluatorDict['lastuser'] = fullName

		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = fullName

			#   Find the Evaluator table row, and update.
			evaluationsSQL.updateEvaluatorUpload(self.connection, _evaluatorDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbUberFormDraft if _isDraft else constants.kJobActionLogVerbUberForm
				logDict['item'] = _evaluatorDict.get('full_name', _container.getDescr())
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			dashboardConfigKeyName = self.getDashboardEventKey(_jobTaskDict,_container)
			activityLogConfigKeyName = self.getActivityLogKey(_jobTaskDict,_container, _isDraft)
			self._constructActivityLogText(_container, _evaluatorDict, 'activityLogConfigKeyName')
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, fullName, _activityLogConfigKeyName=activityLogConfigKeyName,_dashboardConfigKeyName=dashboardConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def getDashboardEventKey(self,_jobTaskDict,_container):
		key = "removeEvalDashboardEvents"
		dashboardConfig = {}
		events = _container.containerDict.get('config',{}).get('addEvalDashboardEvents', [])
		for each in events:
			if each.get('code','') == 'eval_review':
				dashboardConfig = each
				break
		if dashboardConfig:
			evaluatorTypes = lookupTableSvc.getLookupTable(self.connection,"wf_evaluator_type")
			allowedEvaluatorTypes = dashboardConfig.get('evaluatorTypes',[])
			evaluators = self.getEvaluatorsList(_jobTaskDict.get('id',-1))
			if evaluators:
				for evaluator in evaluators:
					thisEvalType = evaluatorTypes.get(evaluator.get('evaluator_type_id',-1))
					if thisEvalType:
						if thisEvalType.get('code','') in allowedEvaluatorTypes:
							if evaluator.get('uploaded',False):
								if not evaluator.get('approved',False):
									key = "addEvalDashboardEvents"
									break
		return key

	def getActivityLogKey(self,_jobTaskDict,_container, _isDraft):
		if _isDraft:
			return 'draftActivityLog'
		return 'submitActivityLog'


	#   Miscellaneous.

	def _constructActivityLogText(self, _container, _evaluatorDict, _activityLogConfigKeyName):
		_container.resolveNames(_evaluatorDict)
		name = _evaluatorDict.get('full_name', '')
		activityLogDict = _container.getConfigDict().get(_activityLogConfigKeyName, {})
		activityLogDict['activityLogText'] = "%s %s" % (activityLogDict.get('activityLogText', ''), name)

		baseActivityLogDict = _container.getConfigDict().get('activityLog', {})
		activityLogDict['comments'] = baseActivityLogDict.get('comments', [])


	#   JSON futzing.

	def jsonifyEvaluator(self, _evaluatorDict):
		if _evaluatorDict:
			keys = ['titles','address_lines']
			for key in keys:
				try:
					self.jsonify(_evaluatorDict, key)
				except:
					_evaluatorDict[key + '_json'] = '[]'

	def jsonify(self, _evaluatorDict, _key):
		aList = _evaluatorDict.get(_key, [])
		if type(aList) is str or type(aList) is unicode:
			aList = [aList]
		_evaluatorDict[_key + '_json'] = json.dumps(aList)

	def unjsonifyEvaluator(self, _evaluatorDict):
		if _evaluatorDict:
			keys = ['titles','address_lines']
			for key in keys:
				try:
					self.unjsonify(_evaluatorDict, key)
				except:
					_evaluatorDict[key] = []

	def unjsonify(self, _evaluatorDict, _key):
		jsonified = _evaluatorDict.get(_key, '')
		_evaluatorDict[_key] = json.loads(jsonified)


	#   Importing an Internal Evaluator.

	def importInternalEvaluator(self, _jobActionDict, _jobTaskDict, _container, sourceId, _profile, _now, _username, doCommit=True):

		evaluator = internalEvalSvc.InternalEvalService(self.connection).getEvaluator(sourceId)
		if evaluator:
			evaluatorDict = {}
			evaluatorDict['job_task_id'] = _jobTaskDict.get('id',None)
			evaluatorDict['emailed_key'] = envUtils.getEnvironment().generateUniqueId()
			evaluatorDict['created'] = _now
			evaluatorDict['updated'] = _now
			evaluatorDict['lastuser'] = _username
			evaluatorDict['first_name'] = evaluator.get('first_name','')
			evaluatorDict['last_name'] = evaluator.get('last_name','')
			evaluatorDict['email'] = evaluator.get('email_address','')
			evaluatorDict['suffix'] = ''
			evaluatorDict['phone'] = ''
			evaluatorDict['middle_name'] = ''
			evaluatorDict['salutation'] = ''
			evaluatorDict['phone'] = ''
			evaluatorDict['degree'] = ''
			evaluatorDict['titles'] = ''
			evaluatorDict['institution'] = ''
			evaluatorDict['address_lines'] = ''
			evaluatorDict['city'] = ''
			evaluatorDict['state'] = ''
			evaluatorDict['postal'] = ''
			evaluatorDict['country'] = ''
			evaluatorDict['admission_date'] = ''
			evaluatorDict['program'] = ''
			evaluatorDict['reason'] = ''
			self.handleAddEditEvaluator(_jobActionDict, _jobTaskDict, evaluatorDict, _container, _profile, {}, _now, _username, doCommit=doCommit)


	#   Importing an Evaluator.

	def importEvaluator(self, _jobActionDict, _jobTaskDict, _container, _srcTaskCode, _srcIdx, _profile, _now, _username, doCommit=True):

		#   Get configuration data and the source Task container.

		srcConfigDict, srcTaskContainer = self._getConfigForImportSource(_container, _srcTaskCode)
		if not srcConfigDict:
			raise excUtils.MPSValidationException("Unknown source task code")
		if not srcTaskContainer:
			raise excUtils.MPSValidationException("Unable to find source task container")

		#   Load up the source Uberform.

		sitePreferences = _profile.get('siteProfile',{}).get('sitePreferences',{})
		srcTaskContainer.loadInstance()
		sourceEditContext = srcTaskContainer.getEditContext(sitePreferences, _prepDatesForDisplay=False)
		sourceUberInstance = sourceEditContext.get('uber_instance', {})
		sourceQuestionList = srcTaskContainer.flattenUberQuestions(sourceUberInstance.get('questions', {}))

		#   Get question and response caches, and build Evaluator.

		questionCache = self._getQuestionCache(sourceQuestionList)
		responseCache = self._getResponseRowAsDictionary(sourceQuestionList, _srcIdx)

		srcImportColumns = srcConfigDict.get('importColumns', {})
		evaluatorDict = {}
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'evaluator_source_id', _defaultValue=None)
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'evaluator_type_id', _defaultValue=None)
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'first_name')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'middle_name')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'last_name')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'suffix')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'email')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'phone')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'salutation', _defaultValue='Dear Dr.')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'degree', _stripLeading=True, _resolveOption=True)
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'titles')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'institution')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'address_lines', _defaultValue=[])
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'city')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'state', _stripLeading=True)
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'postal')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'country', _stripLeading=True)
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'admission_date')
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'program', _stripLeading=True)
		self._mapOneEvaluatorColumn(srcImportColumns, questionCache, responseCache, evaluatorDict, 'reason')
		evaluatorDict['job_task_id'] = _jobTaskDict.get('id',None)
		evaluatorDict['emailed_key'] = envUtils.getEnvironment().generateUniqueId()
		evaluatorDict['created'] = _now
		evaluatorDict['updated'] = _now
		evaluatorDict['lastuser'] = _username
		self.handleAddEditEvaluator(_jobActionDict, _jobTaskDict, evaluatorDict, _container, _profile, {}, _now, _username, doCommit=doCommit)

	def _getConfigForImportSource(self, _container, _srcTaskCode):
		#   Given the Evaluations container and desired task code,
		#   return the configuration data and task container.

		if (_container) and (_srcTaskCode):
			sourceList = _container.getConfigDict().get('importSources', [])
			for sourceConfigDict in sourceList:
				sourceTaskCode = sourceConfigDict.get('taskCode', '')
				if sourceTaskCode == _srcTaskCode:
					sourceTaskContainer = _container.getWorkflow().getContainer(sourceTaskCode)
					if (sourceTaskContainer) and \
						(sourceTaskContainer.getClassName() in (constants.kContainerClassUberForm,)):
						return sourceConfigDict, sourceTaskContainer
					return sourceConfigDict, None
		return None, None

	def _getQuestionCache(self, _flatQuestionList):
		resultCache = {}
		for questionDict in _flatQuestionList:
			code = questionDict.get('code', '')
			resultCache[code] = questionDict
		return resultCache

	def _getResponseRowAsDictionary(self, _flatQuestionList, _responseIdx):
		resultCache = {}
		for questionDict in _flatQuestionList:
			code = questionDict.get('code', '')
			resultCache[code] = self._getOneResponse(questionDict, _responseIdx)
		return resultCache

	def _getOneResponse(self, _questionDict, _responseIdx):
		responseList = _questionDict.get('responseList', [])
		if not responseList:
			return ''
		if len(responseList) < _responseIdx + 1:
			return ''
		return responseList[_responseIdx].get('response', '')

	def _mapOneEvaluatorColumn(self, _srcImportColumns, _questionCache, _responseCache, _evaluatorDict, _key, _defaultValue='', _stripLeading=False, _resolveOption=False):
		srcKeyName = _srcImportColumns.get(_key, '')
		if srcKeyName:
			value = _responseCache.get(srcKeyName, _defaultValue)

			if _resolveOption:
				srcQuestionDict = _questionCache.get(srcKeyName, {})
				if srcQuestionDict:
					for optionDict in srcQuestionDict.get('options', []):
						if optionDict.get('code', '') == value:
							descr = optionDict.get('display_text', '')
							if descr:
								value = descr
								_stripLeading = False

			if _stripLeading:
				prefix = "%s|" % srcKeyName
				if value.startswith(prefix):
					value = value[len(prefix):]

			_evaluatorDict[_key] = value
		else:
			_evaluatorDict[_key] = _defaultValue
