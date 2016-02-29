# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractResolverService import AbstractResolverService
import MPSAppt.services.uberService as uberSvc
import MPSCore.utilities.stringUtilities as stringUtils

#   Given the following:
#       question dictionary
#       database connection
#       site preferences
#
#   this class returns a dictionary containing:
#       'label': the screen prompt for the given question
#       'value': a beautified value, suitable for display on a read-only UI or report
#
#   The given question dictionary is assumed to be taken from an UberForm instance where responses
#   have been applied to the questions in the uberInstance. The safest way to accomplish this is
#   to call the getEditContext() method on the UberForm instance before passing individual question
#   dictionaries to this service.

class UberResolverService(AbstractResolverService):
	def __init__(self, _connection, _sitePreferences, _doNotMaskUberCodes = None):
		AbstractResolverService.__init__(self, _connection, _sitePreferences)
		self.lineSeparator = '<br>'
		self.doNotMaskCodes = _doNotMaskUberCodes

	def resolve(self, _questionDict, _optionalResponseIdx=None):
		responseList = _questionDict.get('responseList', [])
		if not responseList:
			return ''

		if _optionalResponseIdx is not None:
			if len(responseList) < _optionalResponseIdx + 1:
				return ''
			responseList = [responseList[_optionalResponseIdx]]

		#   Resolve response by data_type and special identifier code.

		resolvedValuesList = []
		dataType = _questionDict.get('data_type', '').upper()
		identifierCode = _questionDict.get('identifier_code', '').upper()

		for rawResponseDict in responseList:
			rawResponse = rawResponseDict.get('response', '')
			if type(rawResponse) == type([]):
				for each in rawResponse:
					resolvedValuesList.append(self._resolveOneValue(_questionDict, dataType, identifierCode, each.strip()))
			else:
				resolvedValuesList.append(self._resolveOneValue(_questionDict, dataType, identifierCode, rawResponse.strip()))

		joinText = ', '
		if identifierCode == 'ADDRESS_LINES':
			joinText = self.lineSeparator
		return joinText.join(resolvedValuesList)

	def _resolveOneValue(self, _questionDict, _dataType, _identifierCode, _rawResponse):
		if not _rawResponse:
			return ''

		if _questionDict.get('encrypt', False):
			if not self.doNotMaskCodes or (self.doNotMaskCodes and not _questionDict.get('code','') in self.doNotMaskCodes):
				return stringUtils.maskString(_rawResponse)

		if (_dataType == uberSvc.kQuestionTypeCheckbox):
			if stringUtils.interpretAsTrueFalse(_rawResponse):
				return 'Checked'
			return 'Not Checked'

		if (_dataType == uberSvc.kQuestionTypeRadio) or \
			(_dataType == uberSvc.kQuestionTypeDropdown) or \
			(_dataType == uberSvc.kQuestionTypeMultiDropdown):
			for each in _questionDict.get('options', []):
				if each.get('code', '') == _rawResponse:
					return each.get('display_text', '')
			return _rawResponse

		if (_dataType == uberSvc.kQuestionTypeDate):
			dtAttributes = _questionDict.get('data_type_attributes', '')
			format = stringUtils.getDataTypeAttributeValueForKey(dtAttributes, 'format', _defaultValue='M/D/Y').upper()
			if format == 'M/Y':
				return self.convertMYToDisplayFormat(_rawResponse)
			if format == 'Y':
				return self.convertYToDisplayFormat(_rawResponse)
			return self.convertMDYToDisplayFormat(_rawResponse)

		return _rawResponse

	def resolveQuestionsInGroup(self, _groupDict):
		itemList = []
		if _groupDict.get('type', '') == uberSvc.kElementTypeQuestion:
			itemDict = self._resolveQuestion(_groupDict)
			if itemDict:
				itemList.append(itemDict)
		else:
			for element in _groupDict.get('elements', []):
				if element.get('type', '') == uberSvc.kElementTypeQuestion:
					itemDict = self._resolveQuestion(element)
					if itemDict:
						itemList.append(itemDict)

				elif element.get('type', '') == uberSvc.kElementTypeGroup:
					subItemList = self.resolveQuestionsInGroup(element)
					for subItemDict in subItemList:
						itemList.append(subItemDict)

		return itemList

	def resolveQuestionsInRepeatingGroup(self, _groupDict, _responseIdx):
		itemList = []
		for element in _groupDict.get('elements', []):
			if element.get('type', '') == uberSvc.kElementTypeQuestion:
				itemDict = self._resolveQuestion(element, _responseIdx)
				if itemDict:
					itemList.append(itemDict)
		return itemList

	def _resolveQuestion(self, _questionDict, _optionalResponseIdx=None):
		if _questionDict.get('is_hidden', False):
			return None

		itemDict = {}
		itemDict['label'] = _questionDict.get('display_text', '')
		itemDict['value'] = self.resolve(_questionDict, _optionalResponseIdx)
		itemDict['code'] = _questionDict.get('code','')
		return itemDict

	def resolveFlatQuestionListAsDictionary(self, _flatQuestionList, _optionalResponseIdx=None):
		resultCache = {}
		for questionDict in _flatQuestionList:
			code = questionDict.get('code', '')
			resultCache[code] = self.resolve(questionDict, _optionalResponseIdx)
		return resultCache
