# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import re
import json
import tornado.escape

import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.encryptionUtils as encyptionlib
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.uberService as uberSvc

#   Helper class to process UberForm data from various sources.

class UberFormHelper():

	def __init__(self, _reqHandler):
		self.reqHandler = _reqHandler

	def processUberFormData(self, _uberContainer, **kwargs):
		connection = self.reqHandler.getDbConnection()

		isDraft = kwargs.get('draft', False)
		isAddSavedSet = kwargs.get('addSavedSet', False)
		formData = tornado.escape.json_decode(self.reqHandler.request.body)
		overrideUberValidation = isDraft
		if self.reqHandler.getSitePreferenceAsBoolean('ignoreubervalidation', 'false'):
			overrideUberValidation = True
		repeatingGroupData = self.validateFormData(_uberContainer, formData, overrideUberValidation, isAddSavedSet)
		return formData, repeatingGroupData


	#   Workers.

	def validateFormData(self, _container, _formData, _isDraft, _isAddSavedSet):

		#   Validate entered form data against the _container's Questions.
		#   Throws an objection if errors are detected.
		#   Returns a repeatingGroupData structure on success.

		_container.loadInstance()
		uberInstance = _container.getUberInstance()
		questions = uberInstance.get('questions', {})

		flatQuestionList = _container.flattenUberQuestions(questions)
		self._fixRepeatingTextDataType(_formData, flatQuestionList)
		self._fixMultiDropdownDataType(_formData, flatQuestionList)

		repeatingGroupData, requiredGroups = self._organizeRepeatingGroupData(_container, _formData)
		self._removeEmptyGroups(repeatingGroupData, requiredGroups)

		#   Load the given set of responses into the Uber instance, and determine which fields are hidden.
		#   This allows us to perform the appropriate 'required' checks. I.e. we want to avoid flagging a
		#   question as 'required' when it's hidden from the user.

		mockResponses = self._buildMockResponses(_container, _formData, repeatingGroupData)
		uberInstance['responses'] = mockResponses
		_container.applyResponses()
		_container.getResponsesByCode()
		_container.identifyHiddenContainersAndQuestions()
		_container.cascadeHidden()

		#   Identify errors, put validated data back in _formData or repeatingGroupData.

		errorList = []
		self._validateResponsesNotInRepeatingGroups(_container, _formData, _isDraft, flatQuestionList, errorList)
		self._validateResponsesInRepeatingGroups(_container, repeatingGroupData, _isDraft, questions, errorList)
		self._validateNonRepeatingRequiredGroupsContainAResponse(_container, _isDraft, questions, errorList)
		self._validateDateRelationships(_container, _formData, _isDraft, flatQuestionList, errorList)

		#   Outlier check: if they're doing this as a Saved Set, a Saved Set name must be provided.

		if _isAddSavedSet:
			if not _formData.get('saved_set_name', ''):
				errorList.append({ 'code': 'saved_set_name', 'message': 'Required' })

		if errorList:
			raise excUtils.MPSValidationException(errorList)

		return repeatingGroupData

	def _buildMockResponses(self, _container, _formData, _repeatingGroupData):
		questions = _container.getUberInstance().get('questions', {})
		transformDict = {}

		for uberQuestionDict in _container.flattenUberQuestions(questions):
			if not uberQuestionDict.get('repeating', False):
				code = uberQuestionDict.get('code', '')
				value = _formData.get(code, '')
				if value:
					phake = [{ 'question_code': code, 'response': value }]
					transformDict[code] = phake

		for groupCode in _repeatingGroupData.keys():
			occurrencesForGroup = _repeatingGroupData[groupCode]
			for occurrenceNbr in occurrencesForGroup.keys():
				occurrenceDict = occurrencesForGroup[occurrenceNbr]
				for code in occurrenceDict.keys():
					value = occurrenceDict[code]

					if code not in transformDict:
						transformDict[code] = []
					phake = { 'question_code': code, 'response': value }
					transformDict[code].append(phake)

		return transformDict

	def _validateResponsesNotInRepeatingGroups(self, _container, _formData, _isDraft, _flatQuestionList, _errorList):
		#   First pass: responses to questions that are NOT in repeating groups.
		for uberQuestionDict in _flatQuestionList:
			if not uberQuestionDict.get('repeating', False):
				code = uberQuestionDict.get('code', '')
				try:
					value = self._validateOneResponse(_container, uberQuestionDict, _formData, 0, _isDraft)
					_formData[code] = value
				except Exception, e:
					if isinstance(e, excUtils.MPSValidationException):
						_errorList.append({ 'code': code, 'message': e.message })
					else:
						raise e

	def _validateResponsesInRepeatingGroups(self, _container, _repeatingGroupData, _isDraft, _questions, _errorList):
		#   Second pass: responses to questions that ARE IN repeating groups.
		for uberGroupDict in _container.flattenUberRepeatingGroups(_questions):
			groupCode = uberGroupDict.get('code', '')
			if groupCode:
				occurrencesForGroup = _repeatingGroupData[groupCode]
				for occurrenceNbr in occurrencesForGroup.keys():
					occurrenceDict = occurrencesForGroup[occurrenceNbr]
					for uberContainer in uberGroupDict.get('elements', []):
						if uberContainer.get('type', '') == uberSvc.kElementTypeQuestion:
							questionCode = uberContainer.get('code', '')
							if questionCode:
								phakePhormData = { questionCode: occurrenceDict.get(questionCode, '') }
								try:
									value = self._validateOneResponse(_container, uberContainer, phakePhormData, occurrenceNbr, _isDraft)
									if value:
										occurrenceDict[questionCode] = value
								except Exception, e:
									if isinstance(e, excUtils.MPSValidationException):
										_errorList.append({ 'code': "%s_%s" % (questionCode, str(occurrenceNbr)), 'message': e.message })
									else:
										raise e

	def _validateNonRepeatingRequiredGroupsContainAResponse(self, _container, _isDraft, _questions, _errorList):
		#   Third pass: ensure that non-repeating groups that are marked as 'required' contain at least one response.
		if not _isDraft:
			for uberGroupDict in _container.flattenUberNonRepeatingGroups(_questions):
				required = uberGroupDict.get('required', False)
				if required:
					hasResult, firstQuestionCode = self._uberGroupHasResponse(_container, uberGroupDict)
					if not hasResult:
						_errorList.append({ 'code': firstQuestionCode, 'message': 'At least one response is required' })

	def _validateDateRelationships(self, _container, _formData, _isDraft, _flatQuestionList, _errorList):
		#   Fourth pass: check date fields with restrictions relative to other date fields.
		if not _isDraft:
			for uberQuestionDict in _flatQuestionList:
				dataType = uberQuestionDict.get('data_type', '').upper()
				if dataType == uberSvc.kQuestionTypeDate:
					dtAttributes = uberQuestionDict.get('data_type_attributes', '')
					startDateQuestionCode = stringUtils.getDataTypeAttributeValueForKey(dtAttributes, 'after')
					if startDateQuestionCode is not None:
						endDateQuestionCode = uberQuestionDict.get('code', '')
						self._validateOneDateRelationship(_formData, startDateQuestionCode, endDateQuestionCode, _errorList)

	def _validateOneDateRelationship(self, _formData, _startDateQuestionCode, _endDateQuestionCode, _errorList):
		#   Check that _endDateQuestionCode is on or after _startDateQuestionCode.
		#   Don't validate if either date has an existing error.
		#   Don't validate if either date has not been entered.

		errorsByQuestionCodeCache = self._buildErrorsByQuestionCodeCache(_errorList)
		if _startDateQuestionCode in errorsByQuestionCodeCache: return
		if _endDateQuestionCode in errorsByQuestionCodeCache: return

		startDate = _formData.get(_startDateQuestionCode, '')
		endDate = _formData.get(_endDateQuestionCode, '')
		if not startDate: return
		if not endDate: return

		if endDate < startDate:
			_errorList.append({ 'code': _endDateQuestionCode, 'message': 'End date must be on or after start date' })

	def _buildErrorsByQuestionCodeCache(self, _errorList):
		errorsByQuestionCodeCache = {}
		for errorDict in _errorList:
			code = errorDict.get('code', '')
			if code:
				errorsByQuestionCodeCache[code] = True
		return errorsByQuestionCodeCache

	def _validateOneResponse(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		dataType = _uberQuestionDict.get('data_type', '').upper()

		if dataType == uberSvc.kQuestionTypeText: return self._parseText(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeTextArea: return self._parseText(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeRepeatingText: return self._parseRepeatingText(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeRadio: return self._parseRadio(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeCheckbox: return self._parseCheckbox(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeDropdown: return self._parseDropdown(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeMultiDropdown: return self._parseMultiDropdown(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)
		if dataType == uberSvc.kQuestionTypeDate: return self._parseDate(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)

		code = _uberQuestionDict.get('code', '')
		raise excUtils.MPSValidationException("Invalid data type for %s" % code)

	def _parseText(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		code = _uberQuestionDict.get('code', '')
		formValue = _formData.get(code, '').strip()
		if (self._fieldIsRequiredCheck(_uberQuestionDict, _occurrenceNbr, _isDraft)) and (not formValue):
			raise excUtils.MPSValidationException("Required")
		return formValue

	def _parseRepeatingText(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		code = _uberQuestionDict.get('code', '')
		formValueList = _formData.get(code, [])
		validList = []
		for each in formValueList:
			eachStripped = each.strip()
			if eachStripped:
				validList.append(eachStripped)
		if (self._fieldIsRequiredCheck(_uberQuestionDict, _occurrenceNbr, _isDraft)) and (not validList):
			raise excUtils.MPSValidationException("Required")
		return json.dumps(validList)

	def _parseRadio(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		code = _uberQuestionDict.get('code', '')
		formValue = _formData.get(code, '').strip()
		if formValue:
			for optionDict in _uberQuestionDict.get('options', []):
				if formValue == optionDict.get('code',''):
					return formValue
			raise excUtils.MPSValidationException("Invalid value")
		if self._fieldIsRequiredCheck(_uberQuestionDict, _occurrenceNbr, _isDraft):
			raise excUtils.MPSValidationException("Required")
		return ''

	def _parseDropdown(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		return self._parseRadio(_container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft)

	def _parseMultiDropdown(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		code = _uberQuestionDict.get('code', '')
		formValueList = _formData.get(code, [])
		validList = []
		for each in formValueList:
			value = self._parseRadio(_container, _uberQuestionDict, { code: each }, _occurrenceNbr, _isDraft)
			if value:
				validList.append(value)
		if (self._fieldIsRequiredCheck(_uberQuestionDict, _occurrenceNbr, _isDraft)) and (not validList):
			raise excUtils.MPSValidationException("Required")
		return json.dumps(validList)

	def _parseCheckbox(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		code = _uberQuestionDict.get('code', '')
		formValue = _formData.get(code, '').strip()
		if formValue.upper() == 'TRUE':
			return 'true'
		if self._fieldIsRequiredCheck(_uberQuestionDict, _occurrenceNbr, _isDraft):
			raise excUtils.MPSValidationException("Required")
		return 'false'

	def _parseDate(self, _container, _uberQuestionDict, _formData, _occurrenceNbr, _isDraft):
		code = _uberQuestionDict.get('code', '')
		formValue = _formData.get(code, '').strip()
		if formValue:
			try:
				dateFormatString = _container.getDateFormatPreference(_uberQuestionDict, self.reqHandler.getSitePreferences())
				parsed = dateUtils.flexibleDateMatch(formValue, dateFormatString)
				formatted = dateUtils.formatUTCDateOnly(parsed)
			except Exception, e:
				raise excUtils.MPSValidationException("Invalid date")

			if not _isDraft:
				dtAttributes = _uberQuestionDict.get('data_type_attributes', '')
				futureDatesAllowed = stringUtils.getDataTypeAttributeValueForKey(dtAttributes, 'future', _defaultValue=True, _isBoolean=True)
				if not futureDatesAllowed:
					today = dateUtils.formatUTCDateOnly()
					if formatted > today:
						raise excUtils.MPSValidationException("Future dates not allowed")

			return formatted

		if self._fieldIsRequiredCheck(_uberQuestionDict, _occurrenceNbr, _isDraft):
			raise excUtils.MPSValidationException("Required")
		return ''

	def _fieldIsRequiredCheck(self, _uberQuestionDict, _occurrenceNbr, _isDraft):
		#   Returns True if the field should be required.
		#   Returns False if the field should NOT be required.
		if _isDraft: return False
		if not _uberQuestionDict.get('required', False): return False

		if _occurrenceNbr:
			hiddenList = _uberQuestionDict.get('is_hidden', [])
			if len(hiddenList) >= _occurrenceNbr:
				if hiddenList[_occurrenceNbr-1]:
					return False
		else:
			if _uberQuestionDict.get('is_hidden', False): return False

		if _uberQuestionDict.get('parent_hidden', False): return False
		return True

	def _fixRepeatingTextDataType(self, _formData, _flatQuestionList):
		#   Fix any for Repeating_Text form data fields to ensure they are Lists, not strings.
		self._fixRepeating(_formData, _flatQuestionList, uberSvc.kQuestionTypeRepeatingText)

	def _fixMultiDropdownDataType(self, _formData, _flatQuestionList):
		#   Fix any for Multi_Dropdown form data fields to ensure they are Lists, not strings.
		self._fixRepeating(_formData, _flatQuestionList, uberSvc.kQuestionTypeMultiDropdown)

	def _fixRepeating(self, _formData, _flatQuestionList, _questionType):
		for uberQuestionDict in _flatQuestionList:
			if uberQuestionDict.get('data_type', '').upper() == _questionType:
				code = uberQuestionDict.get('code', '')

				#   Special handling for questions in Repeating Groups.

				if uberQuestionDict.get('repeating', False):
					pattern = '%s_(?P<occurrencenbr>[0-9]*$)' % code
					reObj = re.compile(pattern)

					#   Traverse keys in the form data.
					for keyName in _formData.keys():
						match = reObj.match(keyName)
						if match:
							formValue = _formData.get(keyName, '')
							if type(formValue) != type([]):
								if formValue:
									_formData[keyName] = [formValue]
								else:
									_formData[keyName] = []
				else:
					formValue = _formData.get(code, '')
					if type(formValue) != type([]):
						if formValue:
							_formData[code] = [formValue]
						else:
							_formData[code] = []

	def _organizeRepeatingGroupData(self, _container, _formData):

		#   Returns a multi-level dictionary structure of data elements from submitted form data
		#   that are members of Repeating Groups. At the top-level, the dictionary is keyed by
		#   group_code. For each group_code, the 'value' is another dictionary, structured as follows:
		#
		#       key = occurence nbr (int)
		#       value = data field codes and values (another dictionary)
		#
		#   This structure will be used to drive validation and data persistence for questions
		#   that are in Repeating Groups.

		repeatingGroupData = {}
		requiredGroups = []
		_container.loadInstance()
		uberInstance = _container.getUberInstance()

		#   Traverse Repeating Groups only.
		for uberGroupDict in _container.flattenUberRepeatingGroups(uberInstance.get('questions', {})):
			groupCode = uberGroupDict.get('code', '')
			if groupCode:
				if uberGroupDict.get('required', False):
					requiredGroups.append(groupCode)
				if groupCode not in repeatingGroupData:
					repeatingGroupData[groupCode] = {}
				occurrencesForGroup = repeatingGroupData[groupCode]

				#   Traverse question elements in the Repeating Group.
				for uberContainer in uberGroupDict.get('elements', []):
					if uberContainer.get('type', '') == uberSvc.kElementTypeQuestion:
						questionCode = uberContainer.get('code', '')
						if questionCode:
							pattern = '%s_(?P<occurrencenbr>[0-9]*$)' % questionCode
							reObj = re.compile(pattern)

							#   Traverse keys in the form data.
							for keyName in _formData.keys():
								match = reObj.match(keyName)
								if match:
									occurrenceNbr = int(match.groupdict().get('occurrencenbr','0'))
									if occurrenceNbr:
										if occurrenceNbr not in occurrencesForGroup:
											occurrencesForGroup[occurrenceNbr] = {}
										occurrenceDict = occurrencesForGroup[occurrenceNbr]
										occurrenceDict[questionCode] = _formData[keyName]

		return repeatingGroupData, requiredGroups

	def _removeEmptyGroups(self, _repeatingGroupData, _requiredGroups):

		#   Whack empty Repeating Group occurrences, as if they don't even exist.

		for groupCode in _repeatingGroupData.keys():
			occurrencesForGroup = _repeatingGroupData[groupCode]
			occurrenceNbrsToDelete = []
			for occurrenceNbr in occurrencesForGroup.keys():
				occurrenceDict = occurrencesForGroup[occurrenceNbr]
				allBlank = True
				for val in occurrenceDict.values():
					if val:
						allBlank = False
				if allBlank:
					occurrenceNbrsToDelete.append(occurrenceNbr)

			if (groupCode in _requiredGroups) and (len(occurrencesForGroup) == len(occurrenceNbrsToDelete)):
				occurrenceNbrsToDelete = occurrenceNbrsToDelete[1:]

			for occurrenceNbr in occurrenceNbrsToDelete:
				del occurrencesForGroup[occurrenceNbr]

	def _uberGroupHasResponse(self, _container, _uberGroupDict):
		firstQuestionCode = ''
		responsesByCode = _container.getUberInstance().get('responsesByCode', {})

		for uberContainer in _uberGroupDict.get('elements', []):
			if uberContainer.get('type', '') == uberSvc.kElementTypeQuestion:
				questionCode = uberContainer.get('code', '')
				if questionCode:
					if not firstQuestionCode:
						firstQuestionCode = questionCode
					if responsesByCode.get(questionCode, False):
						return True, firstQuestionCode
			else:
				result, q1Code = self._uberGroupHasResponse(_container, uberContainer)
				if not firstQuestionCode:
					firstQuestionCode = q1Code
				if result:
					return True, firstQuestionCode

		if firstQuestionCode:
			return False, firstQuestionCode
		return True, firstQuestionCode

	def identifyDataChanges(self, _container, _formData, _repeatingGroupData):

		#   Compare existing responses in the _container with new answers in _formData.
		#   Construct lists of work that need to be accomplished:
		#   - a list of wf_uber_response table rows to be Inserted
		#   - a list of wf_uber_response table rows to be Updated
		#   - a list of wf_uber_response table rows to be Deleted
		#
		#   Data elements in Repeating Groups are handled separately.

		insertList = []
		updateList = []
		deleteList = []

		#   Invalidate the existing Uber instance and reload it to ensure we're comparing what was entered
		#   against any existing values in the database.

		_container.setIsLoaded(False)
		_container.setUberInstance({})

		_container.loadInstance()
		uberInstance = _container.getUberInstance()
		uberDict = uberInstance.get('uber', {})
		jobTaskId = uberDict.get('job_task_id', 0)
		questions = uberInstance.get('questions', {})

		oldResponses = uberInstance.get('responses', {})
		now = self.reqHandler.getEnvironment().formatUTCDate()
		username = self.reqHandler.getProfile().get('userProfile', {}).get('username', '')

		#   First pass: responses to questions that are NOT in repeating groups.
		#   We create/update/delete responses very selectively so as to try and maintain the correct
		#   updated and lastuser column values as data are changed.

		flatQuestionList = _container.flattenUberQuestions(questions)
		for uberQuestionDict in flatQuestionList:
			if not uberQuestionDict.get('repeating', False):
				code = uberQuestionDict.get('code', '')

				oldResponseDict = {}
				oldResponseList = oldResponses.get(code, [])
				if oldResponseList:
					oldResponseDict = oldResponseList[0]
				oldResponseText = oldResponseDict.get('response', None)
				newResponseText = _formData.get(code, None)

				#   Special handling for encrypted values.
				#   Muck with the form response.
				if uberQuestionDict.get('encrypt', False):
					if newResponseText.find('*') >= 0:
						newResponseText = oldResponseText
					else:
						newResponseText = encyptionlib.encrypt(newResponseText)

				#   No new response --> delete any existing response.
				if not newResponseText:
					if oldResponseDict:
						deleteList.append(oldResponseDict)

				#   No old response --> create a response.
				elif not oldResponseDict:
					responseDict = {}
					responseDict['job_task_id'] = jobTaskId
					responseDict['question_code'] = uberQuestionDict.get('code', '')
					responseDict['repeat_seq'] = 0
					responseDict['response'] = newResponseText
					responseDict['created'] = now
					responseDict['updated'] = now
					responseDict['lastuser'] = username
					insertList.append(responseDict)

				#   Update if new response different than old response.
				elif newResponseText != oldResponseText:
					responseDict = oldResponseDict.copy()
					responseDict['response'] = newResponseText
					responseDict['updated'] = now
					responseDict['lastuser'] = username
					updateList.append(responseDict)

		#   Second pass: responses to questions that ARE IN repeating groups.
		#   It's very difficult to correctly manage updated and lastuser column values for
		#   repeating groups, since entire groups can be added/deleted/modified at any time.
		#   So we cheese out and simply delete all old repeating group data, so that all the
		#   entered data from the form look like additions.

		for uberGroupDict in _container.flattenUberRepeatingGroups(questions):
			groupCode = uberGroupDict.get('code', '')
			if groupCode:
				occurrencesForGroup = _repeatingGroupData[groupCode]
				for uberContainer in uberGroupDict.get('elements', []):
					if uberContainer.get('type', '') == uberSvc.kElementTypeQuestion:
						questionCode = uberContainer.get('code', '')
						if questionCode:
							oldResponseList = oldResponses.get(questionCode, [])
							for oldResponseDict in oldResponseList:
								deleteList.append(oldResponseDict)

							for occurrenceNbr in sorted(occurrencesForGroup.keys()):
								occurrenceDict = occurrencesForGroup[occurrenceNbr]
								responseDict = {}
								responseDict['job_task_id'] = jobTaskId
								responseDict['question_code'] = questionCode
								responseDict['repeat_seq'] = int(occurrenceNbr)
								responseDict['response'] = occurrenceDict.get(questionCode, '')
								responseDict['created'] = now
								responseDict['updated'] = now
								responseDict['lastuser'] = username
								insertList.append(responseDict)

		return insertList, updateList, deleteList
