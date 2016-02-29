# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.core.containers.task import Task
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.utilities.encryptionUtils as encyptionlib
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.uberResolverService as uberResolverSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.core.constants as constants

class UberForm(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setUberInstance({})
		self.setResponsesApplied(False)

	#   Define an 'uber instance' as a dictionary containing the following keys and values:
	#
	#       'uber'              the wf_uber table record, which contains a jsonified version of the applicable
	#                           questions. The stored JSON is updated every time the control is loaded (if it
	#                           has changed), up until the time the Job Action is 'complete'. After that, the
	#                           stored copy is always used, as it correctly reflects the questions in effect
	#                           at the time the Job Action was finished.
	#                           also has a 'primary' job task id, which is only populated when this uber instance
	#                           shares an uber form with another job action.
	#       'questions'         the unjsonified wf_uber.uber_question_json, which is a stored copy of the uber
	#                           question structure (a dictionary) for this specific instance. Any 'response'
	#                           to a question has been applied if the 'applyResponses' method has
	#                           been executed.
	#       'responses'         a dictionary of wf_uber_response records, keyed by question_code
	#                           each 'value' for a given question_code is a List of wf_uber_response dictionaries.
	#                           normally, there is one response dictionary in the list
	#                           multiple responses appear for Repeating Groups
	#       'responsesByCode'   a dictionary keyed by question code and/or radio/dropdown response.
	#                           useful for determining which questions have responses.
	#                           built by the getResponsesByCode() method, which must be called explicitly.

	def getUberInstance(self): return self.uberInstanceDict
	def setUberInstance(self, _uberInstanceDict): self.uberInstanceDict = _uberInstanceDict

	def getResponsesApplied(self): return self.responsesApplied
	def setResponsesApplied(self, _responsesApplied): self.responsesApplied = _responsesApplied

	def setIsLoaded(self, _isLoaded):
		self.isLoaded = _isLoaded
		if not _isLoaded:
			self.setUberInstance({})
			self.setResponsesApplied(False)

	def getRevisionsRequiredDescriptors(self,fieldName):
		if fieldName == constants.kFLRRGLobalCommentCode:
			return {'question':"General Comment","form":self.getDescr()}
		elif fieldName == constants.kFLRRRepeaterAddRemove:
			return {'question':"Ability to add & remove groups is enabled","form":self.getDescr()}
		lookupCode = fieldName
		# in the case of table-driven repeating groups, identify base question by munging field identifier based on uber naming convention
		parts = fieldName.split('_')
		if parts:
			fieldNum = parts[len(parts)-1]
			if self.identifierEndsWithInteger(fieldNum):
				lookupCode = lookupCode[0:len(lookupCode) - len('_' + fieldNum)]
		descriptors = {}
		for questionDict in self.flattenUberQuestions(self.getUberInstance().get('questions', {})):
			if questionDict.get('code','') == lookupCode:
				questionText = questionDict.get('display_text','')
				questionText = questionText[0:len(questionText)-1] if questionText.endswith(':') else questionText
				descriptors['question'] = questionText
				descriptors['form'] = self.getDescr()
		return descriptors

	def identifierEndsWithInteger(self,strValue):
		try:
			int(strValue)
		except:
			pass
			return False
		return True

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			uberInstance = {}
			jobTaskId = jobTask.get('id',0)
			ubrService = uberSvc.UberService(self.getWorkflow().getConnection())

			#   Get or create the Uber table row.

			uber = ubrService.getUber(jobTaskId)
			if uber:
				uberInstance['uber'] = uber
				if not self.getWorkflow().getJobActionDict().get('complete', False):
					questionJson = self.loadUberQuestionsFromDatabase(ubrService)
					if questionJson != uber['uber_question_json']:
						now = envUtils.getEnvironment().formatUTCDate()
						uber['uber_question_json'] = questionJson
						uber['updated'] = now
						uber['lastuser'] = self.getWorkflow().getUserProfile().get('userProfile', {}).get('username', '')
						ubrService.updateUberJson(uber)
			else:
				now = envUtils.getEnvironment().formatUTCDate()
				uberDict = {}
				uberDict['job_task_id'] = jobTaskId
				uberDict['uber_question_json'] = self.loadUberQuestionsFromDatabase(ubrService)
				uberDict['complete'] = False
				uberDict['created'] = now
				uberDict['updated'] = now
				uberDict['lastuser'] = self.getWorkflow().getUserProfile().get('userProfile', {}).get('username', '')
				ubrService.createUber(uberDict)
				uberInstance['uber'] = ubrService.getUber(jobTaskId)

			#   Unpack the questions.
			#   Find existing responses.

			uber = uberInstance.get('uber', {})
			uberInstance['questions'] = json.loads(uber.get('uber_question_json', {}))
			self.loadUberResponses(uberInstance)
			self.setUberInstance(uberInstance)
			self.synchronizePersonalInfo()

	def loadInstanceByForce(self):
		self.setIsLoaded(False)
		self.setIsLoaded(True)
		ubrService = uberSvc.UberService(self.getWorkflow().getConnection())

		uberInstance = {}
		uberInstance['questions'] = ubrService.assembleUberQuestionSet(self.getConfigDict().get('questionGroupCode', ''))
		self.setUberInstance(uberInstance)

	def loadUberQuestionsFromDatabase(self, _ubrService):

		#   The list of questions for an instantiation of the Uber Form is stored in the wf_uber table as a jsonified string.
		#   When the Uber Form is first created, we load the question list from the database, massage it as necessary, and
		#   store it in the wf_uber table row.
		#
		#   This method loads Uber Question info from the database and returns a jsonified string for storage.

		_ubrService.setJobActionTypeCodes(self.getJobActionTypeCodes())
		_ubrService.setOmittedQuestionAndGroupCodes(self.getConfigDict().get('omitCodes', []))
		questions = _ubrService.assembleUberQuestionSet(self.getConfigDict().get('questionGroupCode', ''))
		return json.dumps(questions)

	def getJobActionTypeCodes(self):
		typeIdList = []

		#   The current Job Action.
		thisJobActionDict = self.getWorkflow().getJobActionDict()
		thisTypeId = thisJobActionDict.get('job_action_type_id', 0)
		if thisTypeId:
			typeIdList.append(thisTypeId)

		#   Related Job Actions.
		connection = self.getWorkflow().getConnection()
		jaService = jobActionSvc.JobActionService(connection)
		relatedJobActionIds = jaService.getRelatedJobActions(thisJobActionDict.get('id', 0))
		for relatedJobActionId in relatedJobActionIds:
			relatedJobActionDict = lookupTableSvc.getEntityByKey(connection, 'wf_job_action', relatedJobActionId, _key='id')
			if relatedJobActionDict:
				relatedTypeId = relatedJobActionDict.get('job_action_type_id', 0)
				if (relatedTypeId) and (relatedTypeId not in typeIdList):
					typeIdList.append(relatedTypeId)

		#   Convert typeIdList to typeCodeList.
		typeCodeList = []
		if typeIdList:
			typeCodeCache = lookupTableSvc.getLookupTable(connection, 'wf_job_action_type', _key='id', _orderBy='id')
			for typeId in typeIdList:
				typeDict = typeCodeCache.get(typeId, None)
				if typeDict:
					typeCode = typeDict.get('code', '')
					if (typeCode) and (typeCode not in typeCodeList):
						typeCodeList.append(typeCode)

		return typeCodeList

	def loadUberResponses(self, _uberInstance):
		#   Loads responses into the given _uberInstance.
		uber = _uberInstance.get('uber', {})
		responses = uberSvc.UberService(self.getWorkflow().getConnection()).getUberResponses(uber.get('job_task_id', 0))

		encryptedQuestionCache = self.identifyEncryptedQuestions(_uberInstance)
		if encryptedQuestionCache:
			for questionCode in responses.keys():
				if questionCode in encryptedQuestionCache:
					responseList = responses[questionCode]
					for responseDict in responseList:
						try:
							decryptedValue = encyptionlib.decrypt(responseDict.get('response', ''))
							responseDict['response'] = decryptedValue
						except Exception, e:
							pass

		_uberInstance['responses'] = responses

	def identifyEncryptedQuestions(self, _uberInstance):
		#   Returns a dictionary of question codes that are stored as encrypted values.
		encryptedCache = {}
		for questionDict in self.flattenUberQuestions(_uberInstance.get('questions', {})):
			if questionDict.get('encrypt', False):
				questionCode = questionDict.get('code', '')
				if questionCode:
					encryptedCache[questionCode] = True
		return encryptedCache

	def synchronizePersonalInfo(self):
		if self.isComplete(): return
		if not self.getConfigDict().get('isPersonalInfo', False): return

		identifierCodes = self.getConfigDict().get('personalInfoCodes', [])
		if not identifierCodes: return

		#   Do not fill any fields from personDict if any of the corresponding uberform fields already have responses.
		self.applyResponses()
		questionsByIdentifierCodeCache = self.organizeQuestionsByIdentifierCode()

		for identifierCode in identifierCodes:
			questionDict = questionsByIdentifierCodeCache.get(identifierCode, {})
			if questionDict:
				responseList = questionDict.get('responseList', [])
				if responseList:
					return

		#   Get person.
		personDict = self.getPersonDict()
		if not personDict: return

		#   Fill'em.
		for identifierCode in identifierCodes:
			questionDict = questionsByIdentifierCodeCache.get(identifierCode, {})
			if questionDict:
				responseList = questionDict.get('responseList', [])
				if not responseList:
					response = self.createResponse(identifierCode, questionDict, personDict)
					if response:
						responseList.append(response)

	def organizeQuestionsByIdentifierCode(self):
		self.loadInstance()
		questionsByIdentifierCodeCache = {}
		for questionDict in self.flattenUberQuestions(self.getUberInstance().get('questions', {})):
			identifierCode = questionDict.get('identifier_code', '')
			if identifierCode:
				questionsByIdentifierCodeCache[identifierCode] = questionDict
		return questionsByIdentifierCodeCache

	def getPersonDict(self):
		jobAction = self.getWorkflow().getJobActionDict()
		if jobAction:
			personId = jobAction.get('person_id', 0)
			if personId:
				personDict = personSvc.PersonService(self.getWorkflow().getConnection()).getPerson(personId)
				if personDict:
					return personDict
		return None

	def createResponse(self, _identifierCode, _questionDict, _personDict):
		personValue = _personDict.get(_identifierCode, '')
		if not personValue:
			return None

		response = {}
		response['isFake'] = True
		response['question_code'] = _questionDict.get('code', '')
		response['repeat_seq'] = 0
		response['complete'] = 'f'

		#   Assuming straight text fields.
		#   When we do radios/dropdowns, setting the response['response'] gets more complicated.
		response['response'] = personValue
		return response

	def breakManagedTableBonds(self):
		repeatingGroupsActuallyManagedByTables = {}
		questions = self.getUberInstance().get('questions', {})
		tableGroupList = self.flattenUberTableGroups(questions)
		repeatingGroupList = self.flattenUberRepeatingGroups(questions)

		if tableGroupList:
			repeatingGroupCache = self._createCacheByCode(repeatingGroupList)

			for tableGroupDict in tableGroupList:
				managesGroupCode = tableGroupDict.get('managesGroupCode', '')
				if managesGroupCode:
					repeatingGroupDict = repeatingGroupCache.get(managesGroupCode, {})
					if repeatingGroupDict:
						managedGroupCode = repeatingGroupDict.get('code', '')
						if managedGroupCode:
							repeatingGroupsActuallyManagedByTables[managedGroupCode] = True

		for repeatingGroup in repeatingGroupList:
			groupCode = repeatingGroup.get('code', '')
			if groupCode not in repeatingGroupsActuallyManagedByTables:
				if 'managedByCode' in repeatingGroup:
					del repeatingGroup['managedByCode']


	#   Match responses with questions.

	def applyResponses(self):

		#   Apply responses to the questions in the current Uber Instance.
		#   Operates on the questions and responses in the current Uber Instance.

		if self.getResponsesApplied():
			return
		self.setResponsesApplied(True)

		questions = self.getUberInstance().get('questions', {})
		responses = self.getUberInstance().get('responses', {})
		for uberQuestionDict in self.flattenUberQuestions(questions):
			questionCode = uberQuestionDict.get('code', '')
			responseList = responses.get(questionCode, [])
			uberQuestionDict['responseList'] = responseList

			#   Futz with the responseList in two cases:
			#
			#   For Repeating Text and Multi-Dropdown fields, the multiple values are stored as a
			#   jsonified List in the response field. We un-jsonify them into a python array.
			#
			#   For Repeating Groups, we store the count of responses in the uberQuestionDict.
			#   If there are no responses, we create a placeholder response so that an empty
			#   question set appears on the form.

			dataType = uberQuestionDict.get('data_type', '').upper()
			for responseDict in responseList:
				if (responseDict) and \
					((dataType == uberSvc.kQuestionTypeRepeatingText) or (dataType == uberSvc.kQuestionTypeMultiDropdown)):
					textResponse = responseDict.get('response', '[]')
					if type(textResponse) == type([]):
						responseDict['response'] = textResponse
					else:
						responseDict['response'] = json.loads(textResponse)

			if uberQuestionDict.get('repeating', False):
				responseCount = len(uberQuestionDict.get('responseList',[]))
				if responseCount:
					uberQuestionDict['response_count'] = responseCount
				else:
					placeholderDict = {}
					placeholderDict['isPlaceholder'] = True
					placeholderDict['job_task_id'] = self.getUberInstance().get('uber', {}).get('job_task_id', 0)
					placeholderDict['question_code'] = questionCode
					placeholderDict['response'] = [] if dataType == uberSvc.kQuestionTypeRepeatingText or dataType == uberSvc.kQuestionTypeMultiDropdown else ''
					placeholderDict['complete'] = False
					placeholderDict['created'] = ''
					placeholderDict['updated'] = ''
					placeholderDict['lastuser'] = ''
					uberQuestionDict['responseList'] = [placeholderDict]
					uberQuestionDict['response_count'] = len(uberQuestionDict['responseList'])

		#   Get response counts for repeating groups.

		for uberGroupDict in self.flattenUberGroups(questions):
			uberGroupDict['response_count'] = 0
			if uberGroupDict.get('repeating', False):
				for element in uberGroupDict.get('elements', []):
					thisResponseCount = element.get('response_count', 0)
					if thisResponseCount > uberGroupDict['response_count']:
						uberGroupDict['response_count'] = thisResponseCount


	#   Build a dictionary indicating which questions have been answered.
	#   Uses the questions and responses in the current Uber Instance.

	def getResponsesByCode(self):
		byCodeDict = {}
		questions = self.getUberInstance().get('questions', {})
		for uberQuestionDict in self.flattenUberQuestions(questions):
			questionCode = uberQuestionDict.get('code', '')
			dataType = uberQuestionDict.get('data_type', '').upper()
			responseList = uberQuestionDict.get('responseList', [])

			if uberQuestionDict.get('repeating', False):
				i = 1
				for responseDict in responseList:
					repeatQuestionCode = "%s_%i" % (questionCode, i)
					repeatResponse = responseDict.get('response', '')
					self._getOneQuestionResponse(byCodeDict, repeatQuestionCode, dataType, repeatResponse, _repeatingIdx=i)
					i += 1
			else:
				if responseList:
					self._getOneQuestionResponse(byCodeDict, questionCode, dataType, responseList[0].get('response', ''), _repeatingIdx=0)

		for uberGroupDict in self.flattenUberGroups(questions):
			parentList = uberGroupDict.get('parentList', [])
			for parent in parentList:
				if byCodeDict.get(parent, False):
					byCodeDict[uberGroupDict.get('code', '')] = True

		self.getUberInstance()['responsesByCode'] = byCodeDict

	def _getOneQuestionResponse(self, _byCodeDict, _questionCode, _dataType, _response, _repeatingIdx=0):
		if _dataType == uberSvc.kQuestionTypeCheckbox:
			if _response.upper() == 'TRUE':
				_byCodeDict[_questionCode] = True

		elif (_dataType == uberSvc.kQuestionTypeRadio) or \
			(_dataType == uberSvc.kQuestionTypeDropdown):
			if _response:
				_byCodeDict[_questionCode] = True
				if not _repeatingIdx:
					_byCodeDict[_response] = True
				else:
					mungedResponse = self._mungeRepeatingResponse(_questionCode, _response, _repeatingIdx)
					_byCodeDict[mungedResponse] = True

		else:
			if _response:
				_byCodeDict[_questionCode] = True

	def _mungeRepeatingResponse(self, _questionCode, _response, _repeatingIdx):
		if '|' in _response:
			splits = _response.split('|')
			return "%s|%s" % (_questionCode, splits[1])
		return "%s_%s" % (_response, _repeatingIdx)


	#   Pass thru the questions and responses in the current Uber Instance,
	#   setting an 'is_hidden' = True attribute on those that should be 'hidden'.
	#   Is dependant on getResponsesByCode() having been executed.

	def identifyHiddenContainersAndQuestions(self):
		mainContainer = self.getUberInstance().get('questions',{})
		self._identifyHiddenOnContainer(mainContainer)

	def _identifyHiddenOnContainer(self, _container):
		containerType = _container.get('type','')
		parentList = _container.get('parentList', [])
		if parentList:
			isParentCheckbox = False
			isHideWhenChecked = False
			singleParentCode = ''
			singleParentContainer = None
			if len(parentList) == 1:
				singleParentCode = parentList[0]
				singleParentContainer = self.getQuestionByCode(singleParentCode, self.getUberInstance())
				if singleParentContainer:
					if singleParentContainer.get('data_type', '').upper() == uberSvc.kQuestionTypeCheckbox:
						isParentCheckbox = True
						if stringUtils.getDataTypeAttributeValueForKey(singleParentContainer.get('data_type_attributes', ''), 'hidewhenchecked', _defaultValue=False, _isBoolean=True):
							isHideWhenChecked = True

			responseCache = self.getUberInstance().get('responsesByCode', {})
			if isParentCheckbox:
				if (containerType == uberSvc.kElementTypeQuestion) and \
					(_container.get('repeating', False)):
					hiddenList = []
					for responseDict in singleParentContainer.get('responseList', []):
						shouldHide = False
						response = responseDict.get('response', '')
						if response:
							isChecked = stringUtils.interpretAsTrueFalse(response)
							if isChecked:
								if isHideWhenChecked:
									shouldHide = True
							else:
								if not isHideWhenChecked:
									shouldHide = True
						hiddenList.append(shouldHide)
					_container['is_hidden'] = hiddenList
				else:
					for responseDict in singleParentContainer.get('responseList', []):
						response = responseDict.get('response', '')
						if response:
							isChecked = stringUtils.interpretAsTrueFalse(response)
							if isChecked:
								if isHideWhenChecked:
									_container['is_hidden'] = True
							else:
								if not isHideWhenChecked:
									_container['is_hidden'] = True

			else:
				if (containerType == uberSvc.kElementTypeQuestion) and \
					(_container.get('repeating', False)):
					hiddenList = []
					i = 1
					for responseDict in _container.get('responseList', []):
						mungedParentList = []
						for each in parentList:
							mungedParentList.append("%s_%i" % (each, i))
						hiddenList.append(not self._anyCodeAppearsInResponseList(mungedParentList, responseCache))
						i += 1
					_container['is_hidden'] = hiddenList
				else:
					if not self._anyCodeAppearsInResponseList(parentList, responseCache):
						_container['is_hidden'] = True

		if containerType == uberSvc.kElementTypeGroup:
			for element in _container.get('elements',''):
				self._identifyHiddenOnContainer(element)

	def _anyCodeAppearsInResponseList(self, _codeList, _responseList):
		for code in _codeList:
			if code in _responseList:
				return True
		return False


	#   Cascade parental 'is_hidden's down thru their children,
	#   setting a 'parent_hidden' = True attribute on those that should be 'hidden'.
	#   Is dependant on identifyHiddenContainersAndQuestions() having been executed.
	#
	#   'parent_hidden' = True basically means that either the element itself is hidden,
	#   or some parent of the element up the chain is hidden.

	def cascadeHidden(self):
		mainContainer = self.getUberInstance().get('questions',{})
		self._cascadeHiddenOnContainer(mainContainer, False)

	def _cascadeHiddenOnContainer(self, _container, _isHidden):
		myHidden = _isHidden
		if not myHidden:
			isHiddenObject = _container.get('is_hidden', False)
			if type(isHiddenObject) != type([]):
				myHidden = isHiddenObject
		if myHidden:
			_container['parent_hidden'] = True

		if _container.get('type','') == uberSvc.kElementTypeGroup:
			for element in _container.get('elements',''):
				self._cascadeHiddenOnContainer(element, myHidden)


	#   Mark group containers that contain no questions as 'no_display'.
	#   This occurs when entire sets of questions are omitted via Title Overrides.

	def markEmptyGroups(self):
		mainContainer = self.getUberInstance().get('questions',{})
		self._markEmptyGroupsOnContainer(mainContainer)

	def _markEmptyGroupsOnContainer(self, _container):
		if _container.get('type','') == uberSvc.kElementTypeGroup:
			for element in _container.get('elements',''):
				self._markEmptyGroupsOnContainer(element)
			if (not self._getQuestionCountForContainer(_container)) and (not _container.get('filler', False)):
				_container['no_display'] = True

	def _getQuestionCountForContainer(self, _container):
		if _container.get('type','') == uberSvc.kElementTypeQuestion:
			return 1
		questionCount = 0
		for element in _container.get('elements',''):
			questionCount += self._getQuestionCountForContainer(element)
		return questionCount


	#   Convert responses for Date controls to human-readable format.
	#   Operates on the questions and responses in the current Uber Instance.

	def prepDatesForDisplay(self, _sitePreferences):
		questions = self.getUberInstance().get('questions', {})
		responses = self.getUberInstance().get('responses', {})
		for uberQuestionDict in self.flattenUberQuestions(questions):
			if uberQuestionDict.get('data_type', '').upper() == uberSvc.kQuestionTypeDate:
				dateFormatString = self.getDateFormatPreference(uberQuestionDict, _sitePreferences)
				uberQuestionDict['date_format'] = dateUtils.mungeDatePatternForDisplay(dateFormatString)

				questionCode = uberQuestionDict.get('code', '')
				responseList = responses.get(questionCode, [])
				for response in responseList:
					textResponse = response.get('response', '')
					if textResponse:
						response['response'] = dateUtils.parseDate(textResponse, dateFormatString)

	def getDateFormatPreference(self, _uberQuestionDict, _sitePreferences):

		#   Get the site's preferred date display format.

		dtAttributes = _uberQuestionDict.get('data_type_attributes', '')
		configDateFormat = stringUtils.getDataTypeAttributeValueForKey(dtAttributes, 'format', _defaultValue='M/D/Y').upper()
		if configDateFormat == 'Y':
			return  _sitePreferences.get('yformat', '%Y')
		elif configDateFormat == 'M/Y':
			return  _sitePreferences.get('ymformat', '%m/%Y')
		return  _sitePreferences.get('ymdformat', '%m/%d/%Y')


	#   Interpret data type attributes for display.

	def interpretDataTypeAttributes(self):
		questions = self.getUberInstance().get('questions', {})
		for uberQuestionDict in self.flattenUberQuestions(questions):
			dataTypeAttributes = uberQuestionDict.get('data_type_attributes', '')
			if dataTypeAttributes:
				if stringUtils.getDataTypeAttributeValueForKey(dataTypeAttributes, 'reverse', _defaultValue=False, _isBoolean=True):
					uberQuestionDict['isReverse'] = True
				if stringUtils.getDataTypeAttributeValueForKey(dataTypeAttributes, 'stack', _defaultValue=False, _isBoolean=True):
					uberQuestionDict['isStack'] = True
				if stringUtils.getDataTypeAttributeValueForKey(dataTypeAttributes, 'hidewhenchecked', _defaultValue=False, _isBoolean=True):
					uberQuestionDict['isHideWhenChecked'] = True


	#   Mask encrypted responses.
	#   Operates on the questions and responses in the current Uber Instance.

	def maskEncryptedResponses(self, _sitePreferences,_doNotMaskCodes):
		questions = self.getUberInstance().get('questions', {})
		responses = self.getUberInstance().get('responses', {})
		for uberQuestionDict in self.flattenUberQuestions(questions):
			if uberQuestionDict.get('encrypt', False):
				questionCode = uberQuestionDict.get('code', '')
				responseList = responses.get(questionCode, [])
				for response in responseList:
					if not _doNotMaskCodes or (_doNotMaskCodes and not questionCode in _doNotMaskCodes):
						response['response'] = stringUtils.maskString(response.get('response', ''))

	def _createCacheByCode(self, _srcList):
		cache = {}
		for each in _srcList:
			code = each.get('code', '')
			if code:
				cache[code] = each
		return cache


	#   Flattening the Question structure.

	def flattenUberQuestions(self, _uberDict):

		#   Find all the questions in the given _questions structure, returning them as a List
		#   in the order in which they are encountered during tree traversal.

		elementType = _uberDict.get('type', '')
		if elementType == uberSvc.kElementTypeQuestion:
			return [_uberDict]

		flatList = []
		if elementType == uberSvc.kElementTypeGroup:
			for element in _uberDict.get('elements', []):
				flatList.extend(self.flattenUberQuestions(element))
		return flatList

	def flattenUberGroups(self, _uberDict):

		#   Find all the groups in the given _questions structure, returning them as a List
		#   in the order in which they are encountered during tree traversal.

		elementType = _uberDict.get('type', '')
		if elementType == uberSvc.kElementTypeQuestion:
			return []

		flatList = []
		if elementType == uberSvc.kElementTypeGroup:
			flatList.append(_uberDict)
			for element in _uberDict.get('elements', []):
				flatList.extend(self.flattenUberGroups(element))
		return flatList

	def flattenUberRepeatingGroups(self, _uberDict):

		#   Find all the Repeating groups (only) in the given _questions structure, returning them as a List
		#   in the order in which they are encountered during tree traversal.

		repeatingList = []
		for uberGroupDict in self.flattenUberGroups(_uberDict):
			if uberGroupDict.get('repeating', False):
				repeatingList.append(uberGroupDict)
		return repeatingList

	def flattenUberNonRepeatingGroups(self, _uberDict):

		#   Find all the Non-Repeating groups (only) in the given _questions structure, returning them as a List
		#   in the order in which they are encountered during tree traversal.

		nonRepeatingList = []
		for uberGroupDict in self.flattenUberGroups(_uberDict):
			if not uberGroupDict.get('repeating', False):
				nonRepeatingList.append(uberGroupDict)
		return nonRepeatingList

	def flattenUberTableGroups(self, _uberDict):

		#   Find all the Table groups (only) in the given _questions structure, returning them as a List
		#   in the order in which they are encountered during tree traversal.

		repeatingList = []
		for uberGroupDict in self.flattenUberGroups(_uberDict):
			if uberGroupDict.get('repeating_table', False):
				repeatingList.append(uberGroupDict)
		return repeatingList


	#   Manufacturing a dictionary of all question/responses that have identifier_codes.
	#       key: identifier code
	#       value: simple list of responses

	def getResponseCacheByIdentifierCode(self, _raw=False, _doNotMaskUberCodes = None):
		self.loadInstance()
		self.applyResponses()

		cache = {}
		questions = self.getUberInstance().get('questions', {})
		resolver = uberResolverSvc.UberResolverService(self.getWorkflow().getConnection(), {}, _doNotMaskUberCodes = _doNotMaskUberCodes)
		for uberQuestionDict in self.flattenUberQuestions(questions):
			identifierCode = uberQuestionDict.get('identifier_code', '')
			if identifierCode:
				if _raw:
					cache[identifierCode] = self._assembleRawResponses(uberQuestionDict)
				else:
					cache[identifierCode] = resolver.resolve(uberQuestionDict)
		return cache

	def _assembleRawResponses(self, _uberQuestionDict):
		responseList = _uberQuestionDict.get('responseList', [])
		if not responseList:
			return []

		resolvedValuesList = []
		for rawResponseDict in responseList:
			rawResponse = rawResponseDict.get('response', '')
			if type(rawResponse) == type([]):
				resolvedValuesList.extend(rawResponse)
			else:
				resolvedValuesList.append(rawResponse)
		return resolvedValuesList


	#   Find a specific Uber Question.

	def getQuestionByCode(self, _questionCode, _uberInstance):
		if _questionCode:
			for questionDict in self.flattenUberQuestions(_uberInstance.get('questions', {})):
				if questionDict.get('code', '') == _questionCode:
					return questionDict
		return None


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			dataDict = {}
			dataDict['url'] = self._getURL()
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences, _doNotMaskCodes=None, _prepDatesForDisplay=True):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['submit_enabled'] = self.getConfigDict().get('submitEnabled', True)
			context['submit_text'] = self.getConfigDict().get('submitText', 'Submit')
			context['submit_url'] = self._getURL(_action='/submit')
			context['draft_enabled'] = self.getConfigDict().get('draftEnabled', True)
			context['draft_text'] = self.getConfigDict().get('draftText', 'Save as Draft')
			context['draft_url'] = self._getURL(_action='/draft')
			context['print_enabled'] = self.getConfigDict().get('printEnabled', True)
			context['print_url'] = self._getURL(_action='/pdf')
			context['printLabelColumnWidth'] = self.getConfigDict().get('printLabelColumnWidth', '400px')
			context['displayOptionCodeRight'] = self.getConfigDict().get('displayOptionCodeRight', [])
			context['displayOptionCodeLeft'] = self.getConfigDict().get('displayOptionCodeLeft', [])

			self.applyResponses()
			self.getResponsesByCode()
			self.identifyHiddenContainersAndQuestions()
			self.markEmptyGroups()
			if _prepDatesForDisplay:
				self.prepDatesForDisplay(_sitePreferences)
			self.interpretDataTypeAttributes()
			self.maskEncryptedResponses(_sitePreferences,_doNotMaskCodes)
			self.breakManagedTableBonds()
			context['uber_instance'] = self.getUberInstance()

			context['saved_sets_enabled'] = self.getConfigDict().get('savedSetsEnabled', False)
			if context['saved_sets_enabled']:
				context['add_url'] = self._getURL(_action='/add')
				ubrService = uberSvc.UberService(self.getWorkflow().getConnection())
				context['saved_sets'] = ubrService.getUberSavedSetNames(self.getCommunity(), self.getUsername(), self.getConfigDict().get('questionGroupCode', ''))
				for each in context['saved_sets']:
					suffix = '/' + str(each.get('id', 0))
					each['apply_url'] = self._getURL(_action='/apply', _suffix=suffix)
					each['delete_url'] = self._getURL(_action='/delete', _suffix=suffix)

			return context

		return {}

	def _getURL(self, _prefix='/appt/jobaction/uberform', _action='', _suffix=''):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s%s/%s/%s%s' % (_prefix, _action, jobActionIdStr, self.getCode(), _suffix)

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			#   The task is 'complete' when the 'Submit' button has been pressed, which ensures that
			#   all required fields have been entered. We simply check the wf_uber record.
			return self.getUberInstance().get('uber', {}).get('complete', False)

		return True

	def deleteYourself(self):
		self.loadInstance()
		uberInstance = self.getUberInstance()
		if uberInstance:
			uberDuberJobTaskId = uberInstance.get('uber',{}).get('job_task_id',-1)
			uberSvc.UberService(self.getWorkflow().getConnection()).deleteUberResponsesForTask({"id":uberDuberJobTaskId})
			import MPSAppt.services.jobActionService as jobActionSvc
			jobActionSvc.JobActionService(self.getWorkflow().getConnection()).unfreezeJobTaskById(uberDuberJobTaskId)
