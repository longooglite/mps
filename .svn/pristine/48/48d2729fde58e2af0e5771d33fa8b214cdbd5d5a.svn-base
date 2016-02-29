# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime

from MPSAppt.core.containers.task import Task
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.uberContainerService as uberContainerSvc
import MPSAppt.services.uberResolverService as uberResolverSvc
import MPSAppt.services.evaluationsService as evaluationsSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.jobActionResolverService as resolverSvc
import MPSAppt.services.internalEvalService as internalEvalSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.core.constants as constants

class Evaluations(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setEvaluatorsList([])

		self.setSourcesByCodeCache({})      #   all evaluator_source database records, keyed by code
		self.setSourcesByIdCache({})        #   all evaluator_source database records, keyed by id
		self.setTypesByCodeCache({})        #   all evaluator_type database records, keyed by code
		self.setTypesByIdCache({})          #   all evaluator_type database records, keyed by id

		self.setSourceList([])              #   evaluator_sources we care about
		self.setTypeList([])                #   evaluator_types we care about
		self.setTypeCollectionsList([])     #   collections of evaluator_types we care about

		self.setFileRepoSequenceList([])    #   file uploads

		self.setTitleCode('')               #   when evaluators must fill out forms instead of file uploads


	#   Getters/Setters.

	def getEvaluatorsList(self): return self.evaluatorsList
	def setEvaluatorsList(self, _evaluatorsList): self.evaluatorsList = _evaluatorsList


	def getSourcesByCodeCache(self): return self.sourcesByCodeCache
	def setSourcesByCodeCache(self, _sourcesByCodeCache): self.sourcesByCodeCache = _sourcesByCodeCache
	def getSourcesByIdCache(self): return self.sourcesByIdCache
	def setSourcesByIdCache(self, _sourcesByIdCache): self.sourcesByIdCache = _sourcesByIdCache


	def getTypesByCodeCache(self): return self.typesByCodeCache
	def setTypesByCodeCache(self, _typesByCodeCache): self.typesByCodeCache = _typesByCodeCache
	def getTypesByIdCache(self): return self.typesByIdCache
	def setTypesByIdCache(self, _typesByIdCache): self.typesByIdCache = _typesByIdCache


	def getSourceList(self): return self.sourceList
	def setSourceList(self, _sourceList): self.sourceList = _sourceList

	def getTypeList(self): return self.typeList
	def setTypeList(self, _typeList): self.typeList = _typeList

	def getTypeCollectionsList(self): return self.typeCollectionsList
	def setTypeCollectionsList(self, _typeCollectionsList): self.typeCollectionsList = _typeCollectionsList


	def getFileRepoSequenceList(self): return self.fileRepoSequenceList
	def setFileRepoSequenceList(self, _fileRepoSequenceList): self.fileRepoSequenceList = _fileRepoSequenceList


	def getTitleCode(self): return self.titleCode
	def setTitleCode(self, _titleCode): self.titleCode = _titleCode


	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		self._loadSourceCaches()
		self._loadTypeCaches()

		self._loadSourceList()
		self._loadTypeList()
		self._loadTypeCollectionsList()

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultList = evaluationsSvc.EvaluationsService(self.getWorkflow().getConnection()).getEvaluatorsList(jobTask.get('id',0))
			for evaluatorDict in resultList:
				self._resolveEvaluatorSource(evaluatorDict)
				self._resolveEvaluatorType(evaluatorDict)
				self.resolveNames(evaluatorDict)
			self.setEvaluatorsList(resultList)

			fileRepoCache = self.getWorkflow().getFileRepoCache()
			self.setFileRepoSequenceList(fileRepoCache.get(self.getCode(),[]))

			if (resultList) and (self.usesFormResponse()):
				jaResolver = resolverSvc.JobActionResolverService(self.getWorkflow().getConnection(), {})
				jaContext = jaResolver.resolve(self.getWorkflow().getJobActionDict())
				self.setTitleCode(jaContext.get('title', {}).get('code', ''))

				groupCode = self.getConfigDict().get('questionGroupCode', '')
				containerService = uberContainerSvc.UberContainerService(self.getWorkflow().getConnection())
				jaService = jobActionSvc.JobActionService(self.getWorkflow().getConnection())

				for evaluatorDict in resultList:
					containerCode = evaluatorDict.get('emailed_key','')
					if containerCode:
						uberContainer = containerService.createUberContainer(self.getWorkflow(), containerCode, groupCode, self.getTitleCode())
						evaluatorDict['uberContainer'] = uberContainer

						uberJobTask = jaService.getJobTask(self.getWorkflow().getJobActionDict(), uberContainer)
						evaluatorDict['uberJobTask'] = uberJobTask
						if uberJobTask:
							jobTaskCache = self.getWorkflow().getJobTaskCache()
							jobTaskCache[containerCode] = uberJobTask


	def _loadSourceCaches(self):
		rawDict = lookupTableSvc.getLookupTable(self.getWorkflow().getConnection(), 'wf_evaluator_source', _key='code')
		self.setSourcesByCodeCache(rawDict)
		self.setSourcesByIdCache(self._organizeCodeCacheById(rawDict))

	def _loadTypeCaches(self):
		rawDict = lookupTableSvc.getLookupTable(self.getWorkflow().getConnection(), 'wf_evaluator_type', _key='code')
		self.setTypesByCodeCache(rawDict)
		self.setTypesByIdCache(self._organizeCodeCacheById(rawDict))

	def _organizeCodeCacheById(self, _cacheByCode):
		cacheById = {}
		for each in _cacheByCode.values():
			cacheById[each.get('id',0)] = each
		return cacheById

	def _loadSourceList(self):
		for sourceConfigDict in self.getConfigDict().get('evaluatorSources',[]):
			thisCode = sourceConfigDict.get('code','')
			if thisCode:
				thisRawDict = self.getSourcesByCodeCache().get(thisCode)
				if thisRawDict:
					thisRawDict['min'] = int(sourceConfigDict.get('min','0'))
					thisRawDict['max'] = int(sourceConfigDict.get('max','0'))
					self.getSourceList().append(thisRawDict)

	def _loadTypeList(self):
		for sourceConfigDict in self.getConfigDict().get('evaluatorTypes',[]):
			thisCode = sourceConfigDict.get('code','')
			if thisCode:
				thisRawDict = self.getTypesByCodeCache().get(thisCode)
				if thisRawDict:
					thisRawDict['min'] = int(sourceConfigDict.get('min','0'))
					thisRawDict['max'] = int(sourceConfigDict.get('max','0'))
					self.getTypeList().append(thisRawDict)

	def _loadTypeCollectionsList(self):
		for sourceConfigDict in self.getConfigDict().get('evaluatorTypeCollections',[]):
			thisCodeList = sourceConfigDict.get('codes',[])
			idList = []
			for thisCode in thisCodeList:
				thisRawDict = self.getTypesByCodeCache().get(thisCode)
				if thisRawDict:
					idList.append(thisRawDict.get('id',0))
			if idList:
				collectionDict = {}
				collectionDict['ids'] = idList
				collectionDict['descr'] = sourceConfigDict.get('descr','')
				collectionDict['min'] = int(sourceConfigDict.get('min','0'))
				collectionDict['max'] = int(sourceConfigDict.get('max','0'))
				self.getTypeCollectionsList().append(collectionDict)

	def _resolveEvaluatorSource(self, _evaluatorDict):
		fk = _evaluatorDict.get('evaluator_source_id', 0)
		if fk:
			sourceDict = self.getSourcesByIdCache().get(fk, None)
			if sourceDict:
				_evaluatorDict['evaluator_source_code'] = sourceDict.get('code', '')
				_evaluatorDict['evaluator_source_descr'] = sourceDict.get('descr', '')

	def _resolveEvaluatorType(self, _evaluatorDict):
		fk = _evaluatorDict.get('evaluator_type_id', 0)
		if fk:
			typeDict = self.getTypesByIdCache().get(fk, None)
			if typeDict:
				_evaluatorDict['evaluator_type_code'] = typeDict.get('code', '')
				_evaluatorDict['evaluator_type_descr'] = typeDict.get('descr', '')
				_evaluatorDict['evaluator_type_is_external'] = typeDict.get('is_external', '')
				_evaluatorDict['evaluator_type_is_arms_length'] = typeDict.get('is_arms_length', '')
				_evaluatorDict['evaluator_type_requires_approval'] = typeDict.get('requires_approval', '')

	def resolveNames(self, _evaluatorDict):
		firstName = _evaluatorDict.get('first_name','')
		middleName = _evaluatorDict.get('middle_name','')
		lastName = _evaluatorDict.get('last_name','')
		suffix = _evaluatorDict.get('suffix','')
		_evaluatorDict['full_name'] = stringUtils.constructFullName(firstName, lastName, middleName, suffix)
		_evaluatorDict['last_comma_first'] = stringUtils.constructLastCommaFirstName(firstName, lastName)


	#   Rendering the Workflow Overview page.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			dataDict = {}
			dataDict['url'] = self._getURL()
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			counts = self._getCounts()
			dataDict['nbr_complete'] = counts.get('completed', 0)
			dataDict['nbr_required'] = counts.get('min', 0)
			dataDict['usesFileResponse'] = self.usesFileResponse()
			dataDict['usesFormResponse'] = self.usesFormResponse()
			dataDict['usesEvaluatorSources'] = self.usesEvaluatorSources()
			dataDict['usesEvaluatorTypes'] = self.usesEvaluatorTypes()
			return dataDict
		return {}


	#   Standard extensions to the default Edit Context.

	def getCommonEvaluationsEditContext(self, _sitePreferences):
		context = self.getCommonEditContext(_sitePreferences)
		jaResolver = resolverSvc.JobActionResolverService(self.getWorkflow().getConnection(), _sitePreferences)
		personContext = jaResolver._resolvePerson(self.getWorkflow().getJobActionDict(), None)
		context['evaluatee'] = personContext
		context['usesFileResponse'] = self.usesFileResponse()
		context['usesFormResponse'] = self.usesFormResponse()
		context['usesEvaluatorSources'] = self.usesEvaluatorSources()
		context['usesEvaluatorTypes'] = self.usesEvaluatorTypes()
		context['packetEnabled'] = self.getConfigDict().get('packetEnabled',True)
		context['requiresResponses'] = self.getConfigDict().get('requiresResponses',True)
		context['assessment_header'] = self.getConfigDict().get('assessment_header','Clinical Assessment')

		return context

	def usesFormResponse(self):
		return self.getConfigDict().get('responseClassName', constants.kContainerClassFileUpload) == constants.kContainerClassUberForm

	def usesFileResponse(self):
		return not self.usesFormResponse()

	def usesEvaluatorSources(self):
		return len(self.getConfigDict().get('evaluatorSources', [])) > 0

	def usesEvaluatorTypes(self):
		return len(self.getConfigDict().get('evaluatorTypes', [])) > 0


	#   Rendering the Evaluations Overview page.

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['counts'] = self._getCounts()
			context['evaluators'] = self._getEvaluatorList(_sitePreferences, context['disabled'])
			context['evaluatorTextMC'] = self.getConfigDict().get('evaluatorTextMC','Evaluator')
			context['evaluatorTextLC'] = self.getConfigDict().get('evaluatorTextLC','evaluator')
			context['evaluationTextMC'] = self.getConfigDict().get('evaluationTextMC','Evaluation')
			context['evaluationTextLC'] = self.getConfigDict().get('evaluationTextLC','evaluation')

			self._setupAdd(context, context['disabled'])
			self._setupImport(context, context['add_allowed'])
			self._setupDownloadSolicitationPacket(context, context['disabled'])
			self._setupDownloadReviewersList(context, context['disabled'])
			self._setupDownloadSolicitationLetter(context, context['disabled'])
			return context
		return {}

	def _setupAdd(self, _context, _isDisabled):
		#   Evaluators can be added unless
		#       controls are disabled, or
		#       we've already reached the maximum number of allowed Evaluators.

		_context['add_allowed'] = False
		_context['add_url'] = ''
		if (not _isDisabled):
			max = int(self.getConfigDict().get('max','0'))
			entered = self._getEnteredCount()
			if entered < max:
				_context['add_allowed'] = True
				_context['add_url'] = self._getURL(_action='/add')

	def _setupImport(self, _context, _isAddAllowed):
		#   Evaluators can be imported from uberform(s) unless
		#       controls are disabled, or
		#       evaluators cannot be added, or
		#       configuration does not support uberform importing.

		_context['import_allowed'] = False
		_context['import_url'] = ''
		if (_isAddAllowed and (self.getConfigDict().get('internalEvaluatorImport', False))):
			_context['import_allowed'] = True
			_context['import_url'] = self._getURL(_action='/import')
		elif (_isAddAllowed) and (self.getConfigDict().get('importEnabled', False)):
			sourceList = self.getConfigDict().get('importSources', [])
			if sourceList:
				atLeastOneTaskCodeIsLegit = False
				for sourceDict in sourceList:
					taskCode = sourceDict.get('taskCode', '')
					if taskCode:
						taskContainer = self.getWorkflow().getContainer(taskCode)
						if (taskContainer) and \
							(taskContainer.getClassName() in (constants.kContainerClassUberForm,)):
							atLeastOneTaskCodeIsLegit = True
							break

				if atLeastOneTaskCodeIsLegit:
					_context['import_allowed'] = True
					_context['import_url'] = self._getURL(_action='/import')

	def _setupDownloadSolicitationPacket(self, _context, _isDisabled):
		#   If enabled, Solicitation Packet can always be downloaded.

		_context['packet_enabled'] = False
		_context['packet_allowed'] = False
		_context['packet_url'] = ''
		_context['packet_text'] = ''
		if self.getConfigDict().get('packetEnabled', True):
			prefix='/appt/jobaction/packet/download'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			_context['packet_enabled'] = True
			_context['packet_allowed'] = True
			_context['packet_url'] = '%s/%s/%s' % (prefix, jobActionIdStr, self.getCode())
			_context['packet_text'] = self.getConfigDict().get('packetText', "View/Download Packet")

	def _setupDownloadReviewersList(self, _context, _isDisabled):
		#   If enabled, Reviewers List can be downloaded unless
		#       no Evaluators have been entered.

		_context['reviewers_enabled'] = False
		_context['reviewers_allowed'] = False
		_context['reviewers_url'] = ''
		_context['reviewers_text'] = ''

		if self.getConfigDict().get('reviewersEnabled', True):
			_context['reviewers_enabled'] = True
			_context['reviewers_text'] = self.getConfigDict().get('reviewersText', "View/Download Reviewers List")
			if self._getEnteredCount():
				prefix='/appt/jobaction/evaluations/reviewers'
				jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
				_context['reviewers_allowed'] = True
				_context['reviewers_url'] = '%s/%s/%s' % (prefix, jobActionIdStr, self.getCode())

	def _setupDownloadSolicitationLetter(self, _context, _isDisabled):
		#   If enabled, Solicitation Letter can be downloaded unless
		#       no Evaluators have been entered.

		_context['letter_enabled'] = False
		_context['letter_allowed'] = False
		_context['letter_url'] = ''
		_context['letter_text'] = ''

		if self.getConfigDict().get('letterEnabled', True):
			_context['letter_enabled'] = True
			_context['letter_text'] = self.getConfigDict().get('letterText', "View/Download Letter")
			if self._getEnteredCount():
				prefix='/appt/jobaction/evaluations/letter'
				jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
				_context['letter_allowed'] = True
				_context['letter_url'] = '%s/%s/%s' % (prefix, jobActionIdStr, self.getCode())


	#   Rendering the Evaluations Add and Edit pages.

	def getEditContextAdd(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/add')
			context['initial_form_values'] = { 'salutation': 'Dear Dr.' }
			context['evaluator_sources'] = self._screenEvaluatorSources(context['initial_form_values'])
			context['evaluator_types'] = self._screenEvaluatorTypes(context['initial_form_values'])
			context['prompts'] = self.dictifyPromptsList(self.getConfigDict().get('prompts',{}))
			return context
		return {}

	def getEditContextEdit(self, _evaluatorId, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/edit', _suffix='/' + str(_evaluatorId))
			context['initial_form_values'] = { 'salutation': 'Dear Dr.' }
			currentEvaluatorDict = self.findEvaluatorById(_evaluatorId)
			if currentEvaluatorDict:
				context['initial_form_values'] = currentEvaluatorDict

			context['evaluator_sources'] = self._screenEvaluatorSources(context['initial_form_values'])
			context['evaluator_types'] = self._screenEvaluatorTypes(context['initial_form_values'])
			context['prompts'] = self.dictifyPromptsList(self.getConfigDict().get('prompts',{}))
			context['subject_line'] = self.getConfigDict().get('emailSubjectLine', 'Letter of Recommendation Request')
			return context
		return {}

	def _screenEvaluatorSources(self, _existingFormValuesDict):
		currentId = _existingFormValuesDict.get('evaluator_source_id', 0)

		#   Screen Evaluator Sources based on raw counts of existing records versus
		#   max configured values.

		for thisDict in self.getSourceList():
			thisDict['disabled'] = False
			thisId = thisDict.get('id',0)
			if (not currentId) or (currentId != thisId):
				thisCode = thisDict.get('code','')
				for minMaxDict in self.getConfigDict().get('evaluatorSources', []):
					if thisCode == minMaxDict.get('code',''):
						max = int(minMaxDict.get('max', '99999'))
						actual = self._getSourceCount(thisId)
						if actual >= max:
							thisDict['disabled'] = True

		return self.getSourceList()

	def _screenEvaluatorTypes(self, _existingFormValuesDict):
		currentId = _existingFormValuesDict.get('evaluator_type_id', 0)

		#   Screen Evaluator Types based on raw counts of existing records versus
		#   max configured values.

		for thisDict in self.getTypeList():
			thisDict['disabled'] = False
			thisId = thisDict.get('id',0)
			if (not currentId) or (currentId != thisId):
				thisCode = thisDict.get('code','')
				for minMaxDict in self.getConfigDict().get('evaluatorTypes', []):
					if thisCode == minMaxDict.get('code',''):
						max = int(minMaxDict.get('max', '99999'))
						actual = self._getTypeCount(thisId)
						if actual >= max:
							thisDict['disabled'] = True

		#   Make a list of Evaluator Type Codes that need to get shut down based on
		#   Evaluator Type Collection maximum counts.

		codesToZonk = {}
		for minMaxDict in self.getConfigDict().get('evaluatorTypeCollections', []):
			actual = 0
			for code in minMaxDict.get('codes', []):
				actual += self._getTypeCountByCode(code)
			max = int(minMaxDict.get('max', '99999'))
			if actual >= max:
				for code in minMaxDict.get('codes', []):
					codesToZonk[code] = True

		#   Zonk the specified Evaluator Type Codes.

		for thisDict in self.getTypeList():
			if not thisDict['disabled']:
				thisId = thisDict.get('id',0)
				if (not currentId) or (currentId != thisId):
					thisCode = thisDict.get('code','')
					if thisCode in codesToZonk:
						thisDict['disabled'] = True

		return self.getTypeList()


	#   Rendering the Evaluations Import page.

	def getEditContextImport(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/import')

			#   summaryData is a list of dictionaries.
			#   Each dictionary describes importable entries from a given import source.
			#   Import sources are described in the task's configuration.
			summaryData = []

			if self.getConfigDict().get('internalEvaluatorImport',False):
				summaryData = self.getInternalEvaluatorSummaryData()
			else:
				sourceList = self.getConfigDict().get('importSources', [])
				for sourceConfigDict in sourceList:
					sourceTaskCode = sourceConfigDict.get('taskCode', '')
					if sourceTaskCode:
						sourceTaskContainer = self.getWorkflow().getContainer(sourceTaskCode)
						if (sourceTaskContainer) and \
							(sourceTaskContainer.getClassName() in (constants.kContainerClassUberForm,)):
							summaryData.append(self._buildImportSummaryDict(sourceConfigDict, sourceTaskContainer, _sitePreferences))
			context['summaryData'] = summaryData
			return context

		return {}

	def getInternalEvaluatorSummaryData(self):
		summaryList = []
		summaryDict = {"header":"","summaryColumns":[]}
		summaryDict['taskCode'] = 'internalevaluatorimport'
		summaryDict['summaryColumns'].append({"code":"first_name","descr":"First Name"})
		summaryDict['summaryColumns'].append({"code":"last_name","descr":"Last Name"})
		summaryDict['summaryColumns'].append({"code":"email_address","descr":"Email Address"})
		summaryDict['data'] = internalEvalSvc.InternalEvalService(self.workflow.connection).getAllEvaluators()
		summaryList.append(summaryDict)
		return summaryList

	def _buildImportSummaryDict(self, _sourceConfigDict, _sourceTaskContainer, _sitePreferences):
		#   Build and return a dictionary describing one input source and
		#   its importable entities.
		taskCode = _sourceConfigDict.get('taskCode', '')

		summaryDict = {}
		summaryDict['taskCode'] = taskCode
		summaryDict['header'] = _sourceConfigDict.get('header', '')
		if not summaryDict['header']:
			summaryDict['header'] = _sourceTaskContainer.getHeader()
		summaryDict['summaryColumns'] = _sourceConfigDict.get('summaryColumns', [])
		summaryDict['data'] = []

		#   Load up the source Uberform.
		_sourceTaskContainer.loadInstance()
		sourceEditContext = _sourceTaskContainer.getEditContext(_sitePreferences)
		sourceUberInstance = sourceEditContext.get('uber_instance', {})
		sourceQuestionList = _sourceTaskContainer.flattenUberQuestions(sourceUberInstance.get('questions', {}))

		#   Determine the number of importable entries.
		#   This is a count of the number of 'full' response rows, ignoring placeholders.
		count = None
		for questionDict in sourceQuestionList:
			responseCount = 0
			for responseDict in questionDict.get('responseList', []):
				if not responseDict.get('isPlaceholder', False):
					responseCount += 1
			if count is None:
				count = responseCount
			elif responseCount < count:
				count = responseCount

		#   Build a dictionary of summary column values for each importable row.
		if count:
			idx = 0
			resolver = uberResolverSvc.UberResolverService(self.getWorkflow().getConnection(), _sitePreferences)
			while idx < count:
				dataRow = {}
				dataRow['id'] = "import|%s|%i" % (taskCode, idx)
				for summaryColumnDict in summaryDict['summaryColumns']:
					summaryColumnCode = summaryColumnDict.get('code', '')
					summaryQuestionDict = _sourceTaskContainer.getQuestionByCode(summaryColumnCode, sourceUberInstance)
					if summaryQuestionDict:
						value = resolver.resolve(summaryQuestionDict, _optionalResponseIdx=idx)
						dataRow[summaryColumnCode] = value
				summaryDict['data'].append(dataRow)
				idx += 1

		return summaryDict


	#   Rendering the Evaluations Delete page.

	def getEditContextDelete(self, _evaluatorId, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/delete', _suffix='/' + str(_evaluatorId))
			context['comment_prompt_list'] = self._setupCommentPromptList('deleteCommentCode')
			return context
		return {}


	#   Rendering the Evaluations Decline page.

	def getEditContextDecline(self, _evaluatorId, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/decline', _suffix='/' + str(_evaluatorId))
			context['comment_prompt_list'] = self._setupCommentPromptList('declineCommentCode')
			return context
		return {}


	#   Rendering the Evaluations Review page.

	def getEditContextReview(self, _evaluatorId, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/review', _suffix='/' + str(_evaluatorId))
			context['approve_url'] = self._getURL(_action='/approve', _suffix='/' + str(_evaluatorId))
			context['deny_url'] = self._getURL(_action='/deny', _suffix='/' + str(_evaluatorId))
			context['comment_prompt_list'] = self._setupCommentPromptList('reviewCommentCode')
			return context
		return {}


	#   Rendering the Evaluations Send page.

	def getEditContextSend(self, _evaluatorId, _sitePreferences, _isPDF=False):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEvaluationsEditContext(_sitePreferences)
			context['url'] = self._getURL(_action='/send', _suffix='/' + str(_evaluatorId))
			context['contact_info'] = self.getWorkflow().getUserProfile().get('userProfile',{}).get('userPreferences',{})

			evaluatorDict = self.findEvaluatorById(_evaluatorId)
			context['evaluator'] = evaluatorDict
			self._resolveEvaluatorDueDate(_sitePreferences, context)

			jaResolver = resolverSvc.JobActionResolverService(self.getWorkflow().getConnection(), _sitePreferences)
			jaContext = jaResolver.resolve(self.getWorkflow().getJobActionDict())
			context.update(jaContext)
			self._resolveDepartmentImages(_sitePreferences, context, _isPDF)

			site = _sitePreferences.get('code','')
			emailTemplateName = self.getConfigDict().get('emailTemplateName','undefined')
			context['emailTemplateName'] = self.buildFullPathToSiteTemplate(site, emailTemplateName)
			context['subject_line'] = self.getConfigDict().get('emailSubjectLine', 'Letter of Recommendation Request')

			appCode = envUtils.getEnvironment().getAppCode()
			appURLPrefix = self._getApplicationURLPrefix(appCode)
			key = evaluatorDict.get('emailed_key','')
			context['packet_url'] = "%s/appt/visitor/candidate/packet/%s" % (appURLPrefix, key)
			context['upload_url'] = "%s/appt/visitor/evaluator/upload/%s" % (appURLPrefix, key)
			context['form_url'] = "%s/appt/visitor/evaluator/form/%s" % (appURLPrefix, key)

			return context

		return {}

	def _resolveEvaluatorDueDate(self, _sitePreferences, _context):
		evaluatorDict = _context.get('evaluator', {})
		dueDateString = evaluatorDict.get('emailed_due_date', '')
		if not dueDateString:
			daze = int(_sitePreferences.get('solicitationduedays', '7'))
			dueDate = datetime.datetime.today() + datetime.timedelta(days=daze)
			dueDateString = envUtils.getEnvironment().formatUTCDate(dueDate)
		evaluatorDict['emailed_due_date'] = self.convertMDYToDisplayFormat(_sitePreferences, dueDateString)

	def _resolveDepartmentImages(self, _sitePreferences, _context, _isPDF=False):
		#   Header image.
		appCode = envUtils.getEnvironment().getAppCode()
		skin = _sitePreferences.get('skin', 'default')
		departmentDict = _context.get('department', {})
		headerImageFilename = departmentDict.get('header_image','')
		if self.getConfigDict().get('headerImageOverride',''):
			headerImageFilename = self.getConfigDict().get('headerImageOverride','')
		if headerImageFilename:
			departmentDict['header_image_url'] = self._resolveImageURL(appCode, skin, headerImageFilename, _isPDF)

		#   Chair signatures.
		for chairDict in departmentDict.get('department_chair',[]):
			sigImageFilename = chairDict.get('chair_signature','')
			if sigImageFilename:
				chairDict['chair_signature_url'] = self._resolveImageURL(appCode, skin, sigImageFilename, _isPDF)

	def _resolveImageURL(self, _appCode, _skin, _imageFilename, _isPDF=False):
		if _isPDF:
			skinFolderPath = envUtils.getEnvironment().getSkinFolderPath()
			args = ("file://%s" % skinFolderPath, _skin, _imageFilename)
		else:
			args = (self._getApplicationURLPrefix(_appCode), _skin, _imageFilename)
		return '''%s/%s/images/%s''' % args

	def _getApplicationURLPrefix(self, _appCode):
		appURL = self._getApplicationURL(_appCode)
		return appURL[:appURL.rfind('/')]

	def _getApplicationURL(self, _appCode):
		appList = self.getWorkflow().getUserProfile().get('siteProfile',{}).get('siteApplications',[])
		for appDict in appList:
			if appDict.get('code','') == _appCode:
				return appDict.get('url','')
		return ''


	#   Rendering the Evaluations File Upload page.

	def getEditContextFile(self, _evaluatorId, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			currentEvaluatorDict = self.findEvaluatorById(_evaluatorId)
			if currentEvaluatorDict:
				context = self.getCommonEvaluationsEditContext(_sitePreferences)
				context['url'] = self._getURL(_action='/upload', _suffix='/' + str(_evaluatorId))
				context['upload_url'] = context['url']
				context['delete_url'] = 'gobble gobble gobble'
				context['replace_url'] = 'gobble gobble gobble'
				context['salutation'] = currentEvaluatorDict.get('salutation','')
				context['last_name'] = currentEvaluatorDict.get('last_name','')

				appCode = envUtils.getEnvironment().getAppCode()
				appURLPrefix = self._getApplicationURLPrefix(appCode)
				key = currentEvaluatorDict.get('emailed_key','')
				context['packet_url'] = "%s/appt/visitor/candidate/packet/%s" % (appURLPrefix, key)

				desiredSeqNbr = int(currentEvaluatorDict.get('uploaded_file_repo_seq_nbr','0'))
				for seqNbrDict in self.getFileRepoSequenceList():
					seqNbr = int(seqNbrDict.get('seq_nbr','99999'))
					if seqNbr == desiredSeqNbr:
						timezone = _sitePreferences.get('timezone', 'US/Eastern')
						format = _sitePreferences.get('ymdhmformat', '%m/%d/%Y %H:%M')
						jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))

						currentDict = seqNbrDict.get('current',{})
						if currentDict:
							self.localizeDates(currentDict, timezone, format)
							argTuple = (jobActionIdStr, self.getCode(), seqNbr, str(currentDict.get('version_nbr','0')))
							currentDict['download_url'] = '/appt/jobaction/file/download/%s/%s/%i/%s' % argTuple
							argTuple = (jobActionIdStr, self.getCode(), seqNbr)
							currentDict['delete_url'] = '/appt/jobaction/file/delete/%s/%s/%i' % argTuple

						for version in seqNbrDict.get('versions',[]):
							self.localizeDates(version, timezone, format)
							version['download_url'] = '/appt/jobaction/file/download/%s/%s/%i/%s' % (jobActionIdStr, self.getCode(), seqNbr, str(version.get('version_nbr','0')))
						context['versions'] = seqNbrDict.get('versions',[])
						if currentDict:
							context['versions'] = [currentDict] + context['versions']

				context['eval_upload_item'] = self.renderAsFileItem(_evaluatorId, currentEvaluatorDict, _sitePreferences)
				return context

		return {}

	def localizeDates(self, _fileRepoDict, timezone, format):
		if _fileRepoDict:
			_fileRepoDict['created_display'] = self.localizeDate(_fileRepoDict.get('created',''), timezone, format)
			_fileRepoDict['updated_display'] = self.localizeDate(_fileRepoDict.get('updated',''), timezone, format)

	def renderAsFileItem(self, _evaluatorId, _currentEvaluatorDict, _sitePreferences):
		desiredSeqNbr = int(_currentEvaluatorDict.get('uploaded_file_repo_seq_nbr','0'))

		common = {}
		common['class_name'] = constants.kContainerClassFileUpload
		common['code'] = self.getCode()
		common['descr'] = 'Upload Evaluation'
		common['header'] = self.getHeader()
		common['is_blocked'] = self.getIsBlocked()
		common['is_complete'] = self.isComplete()
		common['optional'] = self.isComplete()
		common['revisions_required'] = self.getRevisionsRequired()
		common['title'] = ''
		common['view_details'] = True

		config = {}
		config['min'] = '1'
		config['max'] = '1'

		sequenceDict = {}
		sequenceDict['seq_nbr'] = str(desiredSeqNbr)
		sequenceDict['upload_url'] = self._getURL(_action='/upload', _suffix='/' + str(_evaluatorId))
		sequenceDict['current'] = {}
		sequenceDict['versions'] = []

		for seqNbrDict in self.getFileRepoSequenceList():
			seqNbr = int(seqNbrDict.get('seq_nbr','99999'))
			if seqNbr == desiredSeqNbr:
				timezone = _sitePreferences.get('timezone', 'US/Eastern')
				format = _sitePreferences.get('ymdhmformat', '%m/%d/%Y %H:%M')
				jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))

				currentDict = seqNbrDict.get('current',{})
				self.localizeDates(currentDict, timezone, format)
				argTuple = (jobActionIdStr, self.getCode(), seqNbr, str(currentDict.get('version_nbr','0')))
				currentDict['download_url'] = '/appt/jobaction/file/download/%s/%s/%i/%s' % argTuple
				argTuple = (jobActionIdStr, self.getCode(), seqNbr)
				currentDict['delete_url'] = '/appt/jobaction/file/delete/%s/%s/%i' % argTuple
				sequenceDict['current'] = currentDict

				for version in seqNbrDict.get('versions',[]):
					self.localizeDates(version, timezone, format)
					version['download_url'] = '/appt/jobaction/file/download/%s/%s/%i/%s' % (jobActionIdStr, self.getCode(), seqNbr, str(version.get('version_nbr','0')))
				sequenceDict['versions'] = seqNbrDict.get('versions',[])

		data = {}
		data['activity_log'] = []
		data['disabled'] = self.standardTaskDisabledCheck()
		data['sequence_list'] = [sequenceDict]

		rider = {}
		rider['common'] = common
		rider['config'] = config
		rider['data'] = data
		return rider


	#   Rendering the Evaluations Form Upload page.

	def getEditContextForm(self, _evaluatorId, _sitePreferences, _isVisitor=True):
		self.loadInstance()
		if self.getIsEnabled():
			currentEvaluatorDict = self.findEvaluatorById(_evaluatorId)
			if currentEvaluatorDict:
				context = self.getCommonEvaluationsEditContext(_sitePreferences)
				context['url'] = self._getURL(_action='/form', _suffix='/' + str(_evaluatorId))
				context['salutation'] = currentEvaluatorDict.get('salutation','')
				context['last_name'] = currentEvaluatorDict.get('last_name','')

				appCode = envUtils.getEnvironment().getAppCode()
				appURLPrefix = self._getApplicationURLPrefix(appCode)
				key = currentEvaluatorDict.get('emailed_key','')
				context['evaluatorId'] = key
				context['packet_url'] = "%s/appt/visitor/candidate/packet/%s" % (appURLPrefix, key)

				container = currentEvaluatorDict.get('uberContainer', None)
				evaluatorJobTask = currentEvaluatorDict.get('uberJobTask', None)
				if not evaluatorJobTask:
					now = envUtils.getEnvironment().formatUTCDate()
					containerCode = currentEvaluatorDict.get('emailed_key','unknown')

					jaService = jobActionSvc.JobActionService(self.getWorkflow().getConnection())
					evaluatorJobTask = jaService.getOrCreateJobTask(self.getWorkflow().getJobActionDict(), container, now, self.getCode())
					jobTaskCache = self.getWorkflow().getJobTaskCache()
					jobTaskCache[containerCode] = evaluatorJobTask

				container.setIsLoaded(False)
				container.loadInstance()
				uberContext = container.getEditContext(_sitePreferences)

				disabled = context.get('disabled', True)
				context.update(uberContext)
				if _isVisitor:
					context['submit_url'] = '/appt/visitor/evaluator/form/submit/' + key
					context['draft_url'] = '/appt/visitor/evaluator/form/draft/' + key
					context['print_url'] = '/appt/visitor/evaluator/form/print/' + key
					context['form_url'] = '/appt/visitor/evaluator/form/' + key
				else:
					context['disabled'] = disabled
					jobActionId = str(self.getWorkflow().getJobActionDict().get('id', 0))
					urlTuple = (jobActionId, self.getCode(), _evaluatorId)
					context['url'] = '/appt/jobaction/evaluations/form/%s/%s/%s' % urlTuple
					context['submit_url'] = '/appt/jobaction/evaluations/submit/%s/%s/%s' % urlTuple
					context['draft_url'] = '/appt/jobaction/evaluations/draft/%s/%s/%s' % urlTuple
					context['print_url'] = '/appt/jobaction/evaluations/print/%s/%s/%s' % urlTuple

				return context

		return {}


	#   Completitude and conditionals.

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			counts = self._getCounts()
			if counts['min'] > counts['received']:
				return False
			if counts['min'] > counts['completed']:
				return False
			for breakout in counts.get('breakouts',[]):
				if not breakout['met']:
					return False
		return True

	def isEvaluatorComplete(self, _evaluatorDict):

		#   An Evaluator is 'Complete' iff:
		#       it's not Declined, and
		#       it has an evaluator response, and
		#       EITHER this evaluationType does not need review,
		#           OR this evaluationType NEEDS review AND the review was approved.

		if self.isDeclined(_evaluatorDict):
			return False

		if self.hasEvaluatorResponse(_evaluatorDict):
			if not self.requiresReview(_evaluatorDict):
				return True
			return self.isApproved(_evaluatorDict)

		return False

	def isDeclined(self, _evaluatorDict):
		return (_evaluatorDict.get('declined_date','')) and (_evaluatorDict.get('declined',False))

	def isEmailed(self, _evaluatorDict):
		return (_evaluatorDict.get('emailed_date','')) and (_evaluatorDict.get('emailed',False))

	def hasEvaluatorResponse(self, _evaluatorDict):
		if self.usesFormResponse():
			return self.hasFormResponse(_evaluatorDict)
		return self.isUploaded(_evaluatorDict)

	def hasFormResponse(self, _evaluatorDict):
		uberContainer = _evaluatorDict.get('uberContainer', None)
		if uberContainer:
			return uberContainer.isComplete()
		return False

	def isUploaded(self, _evaluatorDict):
		desiredSeqNbr = int(_evaluatorDict.get('uploaded_file_repo_seq_nbr','0'))
		for seqNbrDict in self.getFileRepoSequenceList():
			seqNbr = int(seqNbrDict.get('seq_nbr','99999'))
			if seqNbr == desiredSeqNbr:
				if seqNbrDict.get('current',{}):
					return True
		return False

	def isApproved(self, _evaluatorDict):
		return (_evaluatorDict.get('approved_date','')) and (_evaluatorDict.get('approved',False))

	def approvalHasBeenRecorded(self, _evaluatorDict):
		return True if (_evaluatorDict.get('approved_date','')) else False

	def requiresReview(self, _evaluatorDict):
		return _evaluatorDict.get('evaluator_type_requires_approval', False)


	#   Evaluator List.

	def _getEvaluatorList(self, _sitePreferences, _isDisabled):
		evalList = []
		for evaluatorDict in self.getEvaluatorsList():
			thisDict = evaluatorDict.copy()
			thisDict['is_complete'] = self.isEvaluatorComplete(thisDict)
			self._determineStatus(thisDict, _sitePreferences)
			self._setupDecline(thisDict, _isDisabled)
			self._setupSend(thisDict, _isDisabled)
			self._setupView(thisDict, _isDisabled)
			self._setupUpload(thisDict, _isDisabled)
			self._setupForm(thisDict, _isDisabled)
			self._setupReview(thisDict, _isDisabled)
			self._setupEdit(thisDict, _isDisabled)
			self._setupDelete(thisDict, _isDisabled)
			self._setupPrint(thisDict, _isDisabled)
			evalList.append(thisDict)
		return evalList

	def _determineStatus(self, _evaluatorDict, _sitePreferences):

		#   Screen out Declined immediately.

		status = ''
		if self.isDeclined(_evaluatorDict):
			status = 'Declined'

		if not status:
			if self.hasEvaluatorResponse(_evaluatorDict):
				if self.isEvaluatorComplete(_evaluatorDict):
					if self.requiresReview(_evaluatorDict):
						status = 'Approved'
					else:
						blurb = 'Uploaded'
						if self.usesFormResponse():
							blurb = 'Uploaded'
						status = '%s on %s' % (blurb, self.convertTimestampToDisplayFormat(_sitePreferences, _evaluatorDict.get('uploaded_date','')))
						if not self.isEmailed(_evaluatorDict):
							status += ' - Email not sent'
				else:
					if self.requiresReview(_evaluatorDict):
						if (self.approvalHasBeenRecorded(_evaluatorDict)) and (not self.isApproved(_evaluatorDict)):
							status = 'Denied'
						else:
							status = 'Pending Review'
							if not self.isEmailed(_evaluatorDict):
								status += ' - Email not sent'

		if not status:
			if self.isEmailed(_evaluatorDict):
				status = 'Sent'

		if not status:
			status = 'Not Sent'

		_evaluatorDict['status'] = status


	def _setupDecline(self, _evaluatorDict, _isDisabled):
		#   Evaluators can be marked as Declined unless
		#       controls are disabled, or
		#       an evaluation response has been provided, or
		#       the evaluator is already marked as Declined.

		_evaluatorDict['decline_allowed'] = False
		_evaluatorDict['decline_url'] = ''
		if (not _isDisabled) and \
			(not self.hasEvaluatorResponse(_evaluatorDict)) and \
			(not self.isDeclined(_evaluatorDict)):
			_evaluatorDict['decline_allowed'] = True
			_evaluatorDict['decline_url'] = self._getURL(_action='/decline', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupSend(self, _evaluatorDict, _isDisabled):
		#   Email can be sent unless
		#       controls are disabled, or
		#       evaluator has declined, or
		#       an evaluation response has been provided, or
		#       pre-requisites are not complete.

		_evaluatorDict['send_allowed'] = False
		_evaluatorDict['send_url'] = ''
		if (not _isDisabled) and \
			(not self.isDeclined(_evaluatorDict)) and \
			(not self.hasEvaluatorResponse(_evaluatorDict)):
			preReqTaskCodes = self.getConfigDict().get('emailSendBlockers', [])
			if self._checkTasksComplete(preReqTaskCodes):
				_evaluatorDict['send_allowed'] = True
				_evaluatorDict['send_url'] = self._getURL(_action='/send', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupView(self, _evaluatorDict, _isDisabled):
		#   Evaluation can be viewed unless
		#       controls are disabled, or
		#       response type is not File, or
		#       no evaluation response has been provided.

		_evaluatorDict['view_allowed'] = False
		_evaluatorDict['view_url'] = ''
		if (not _isDisabled) and \
			(self.usesFileResponse()) and \
			(self.hasEvaluatorResponse(_evaluatorDict)):
			_evaluatorDict['view_allowed'] = True
			_evaluatorDict['view_url'] = self._getURL(_prefix='/appt/jobaction/file', _action='/download', _suffix='/' + str(_evaluatorDict.get('uploaded_file_repo_seq_nbr',0)))

	def _setupPrint(self, _evaluatorDict, _isDisabled):
		#   Evaluation can be viewed unless
		#       controls are disabled, or
		#       response type is not File, or
		#       no evaluation response has been provided.

		_evaluatorDict['print_allowed'] = False
		_evaluatorDict['print_url'] = ''
		if (not _isDisabled) and \
			(self.usesFormResponse()) and \
			(self.hasEvaluatorResponse(_evaluatorDict)):
			_evaluatorDict['print_allowed'] = True
			_evaluatorDict['print_url'] = self._getURL(_action='/print', _suffix='/' + str(_evaluatorDict.get('id',0)))


	def _setupUpload(self, _evaluatorDict, _isDisabled):
		#   Evaluation can be uploaded unless
		#       controls are disabled, or
		#       response type is not File, or
		#       evaluator has declined.

		_evaluatorDict['upload_allowed'] = False
		_evaluatorDict['upload_url'] = ''
		if (not _isDisabled) and \
			(self.usesFileResponse()) and \
			(not self.isDeclined(_evaluatorDict)):
			_evaluatorDict['upload_allowed'] = True
			_evaluatorDict['upload_url'] = self._getURL(_action='/upload', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupForm(self, _evaluatorDict, _isDisabled):
		#   Forms can be entered unless
		#       controls are disabled, or
		#       response type is not Form, or
		#       evaluator has declined.

		_evaluatorDict['form_allowed'] = False
		_evaluatorDict['form_url'] = ''
		if (not _isDisabled) and \
			(self.usesFormResponse()) and \
			(not self.isDeclined(_evaluatorDict)):
			_evaluatorDict['form_allowed'] = True
			_evaluatorDict['form_url'] = self._getURL(_action='/form', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupReview(self, _evaluatorDict, _isDisabled):
		#   Evaluation can be reviewed unless
		#       controls are disabled, or
		#       evaluator has declined, or
		#       no evaluation response has been provided, or
		#       evaluation does not require review, or
		#       user does not have review privilege.

		_evaluatorDict['review_allowed'] = False
		_evaluatorDict['review_url'] = ''
		if (not _isDisabled) and \
			(not self.isDeclined(_evaluatorDict)) and \
			(self.hasEvaluatorResponse(_evaluatorDict)) and \
			(self.requiresReview(_evaluatorDict)) and \
			(self.hasAnyPermission(self.getConfigDict().get('reviewPermissions',[]))):
			_evaluatorDict['review_allowed'] = True
			_evaluatorDict['review_url'] = self._getURL(_action='/review', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupEdit(self, _evaluatorDict, _isDisabled):
		#   Evaluators can be edited at any time, unless
		#       controls are disabled.

		_evaluatorDict['edit_allowed'] = False
		_evaluatorDict['edit_url'] = ''
		if not _isDisabled:
			_evaluatorDict['edit_allowed'] = True
			_evaluatorDict['edit_url'] = self._getURL(_action='/edit', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupDelete(self, _evaluatorDict, _isDisabled):
		#   Evaluators can be deleted unless
		#       controls are disabled, or
		#       email has been sent.

		_evaluatorDict['delete_allowed'] = False
		_evaluatorDict['delete_url'] = ''
		if (not _isDisabled) and \
			(not self.isEmailed(_evaluatorDict)):
			_evaluatorDict['delete_allowed'] = True
			_evaluatorDict['delete_url'] = self._getURL(_action='/delete', _suffix='/' + str(_evaluatorDict.get('id',0)))

	def _setupCommentPromptList(self, _commentCodeKey):
		commentCode = self.getConfigDict().get(_commentCodeKey, '')
		if commentCode:
			commentConfigDict = self.getCommentConfigForCommentCode(commentCode)
			if commentConfigDict:
				if self.hasAnyPermission(commentConfigDict.get('accessPermissions',[])):
					promptDict = {}
					promptDict['comment_code'] = commentConfigDict.get('commentCode','')
					promptDict['comment_label'] = commentConfigDict.get('commentLabel','')
					return [promptDict]
		return []



	#   Counting.

	def _getCounts(self):
		counts = {}
		counts['min'] = int(self.getConfigDict().get('min','0'))
		counts['max'] = int(self.getConfigDict().get('max','0'))
		counts['entered'] = self._getEnteredCount()
		counts['received'] = self._getReceivedCount()
		counts['completed'] = self._getCompletedCount()
		counts['by_source'] = self._getSourceCounts()
		counts['breakouts'] = self._getBreakoutCounts()
		counts['showMaxAllowed'] = self.getConfigDict().get('showMaxAllowed',True)
		return counts

	def _getEnteredCount(self):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				count += 1
		return count

	def _getReceivedCount(self):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if self.hasEvaluatorResponse(evaluatorDict):
					count += 1
		return count

	def _getCompletedCount(self):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if self.isEvaluatorComplete(evaluatorDict):
					count += 1
		return count

	def _getSourceCounts(self):
		counts = []
		for sourceDict in self.getSourceList():
			countDict = sourceDict.copy()
			countDict['actual'] = self._getSourceCount(countDict.get('id',0))
			counts.append(countDict)
		return counts

	def _getBreakoutCounts(self):
		breakouts = []

		for sourceDict in self.getSourceList():
			min = sourceDict.get('min',0)
			if min:
				completed = self._getSourceCompleteCount(sourceDict.get('id',0))
				sourceDict['completed'] = completed
				sourceDict['met'] = completed >= min
				breakouts.append(sourceDict)

		for typeDict in self.getTypeList():
			min = typeDict.get('min',0)
			if min:
				completed = self._getTypeCompleteCount(typeDict.get('id',0))
				typeDict['completed'] = completed
				typeDict['met'] = completed >= min
				breakouts.append(typeDict)

		for collectionDict in self.getTypeCollectionsList():
			min = collectionDict.get('min',0)
			if min:
				completed = 0
				for id in collectionDict.get('ids',[]):
					completed += self._getTypeCompleteCount(id)
				collectionDict['completed'] = completed
				collectionDict['met'] = completed >= min
				breakouts.append(collectionDict)

		return breakouts

	def _getSourceCount(self, _sourceId):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if evaluatorDict.get('evaluator_source_id', -1) == _sourceId:
					count += 1
		return count

	def _getSourceCompleteCount(self, _sourceId):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if evaluatorDict.get('evaluator_source_id', -1) == _sourceId:
					if self.isEvaluatorComplete(evaluatorDict):
						count += 1
		return count

	def _getTypeCount(self, _typeId):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if evaluatorDict.get('evaluator_type_id', -1) == _typeId:
					count += 1
		return count

	def _getTypeCountByCode(self, _typeCode):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if evaluatorDict.get('evaluator_type_code', '') == _typeCode:
					count += 1
		return count

	def _getTypeCompleteCount(self, _typeId):
		count = 0
		for evaluatorDict in self.getEvaluatorsList():
			if not evaluatorDict.get('declined', False):
				if evaluatorDict.get('evaluator_type_id', -1) == _typeId:
					if self.isEvaluatorComplete(evaluatorDict):
						count += 1
		return count


	#   Miscellaneous.

	def _getURL(self, _prefix='/appt/jobaction/evaluations', _action='', _suffix=''):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s%s/%s/%s%s' % (_prefix, _action, jobActionIdStr, self.getCode(), _suffix)

	def findEvaluatorById(self, _evaluatorId):
		for evaluatorDict in self.getEvaluatorsList():
			if evaluatorDict.get('id',0) == _evaluatorId:
				return evaluatorDict
		return {}

	def _checkTasksComplete(self, _containerCodeList):

		#   Return False if any container in the given list is not Complete.
		#   Return True  otherwise.

		for containerCode in _containerCodeList:
			container = self.getWorkflow().getContainer(containerCode)
			if container:
				if not container.isComplete():
					return False
		return True
