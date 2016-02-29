# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

import MPSCV.services.metaService as metaSvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.exceptionUtils as excUtils

#   ViewMaster(tm).
#
#   ViewMaster formats a cv_attribute for display, using a specified
#   cv_field dictionary and a specified cv_affordance_type.

class ViewMaster(object):

	def __init__(self, _dbConnection, _repeatDelimiter='<br/>'):
		self.dbConnection = _dbConnection
		self.repeatDelimiter = _repeatDelimiter
		self.staticDictCache = {}
		self.staticListCache = {}
		self.categoryCache = {}


	#   Accessors.

	def getStaticDictCache(self): return self.staticDictCache
	def getStaticListCache(self): return self.staticListCache
	def getCategoryCache(self): return self.categoryCache


	#   Mainline formatters

	def formatAttributeValueForDisplay(self, _attributeValue, _fieldDict, _typeString, _categoryCode, _sitePreferencesDict, isPrintedCV = False):

		#   Format the given _attributeValue for human consumption.
		#
		#   The _fieldDict should contain the following keys, the values of
		#   which may, or may not, be applicable to the formatting process,
		#   depending on the value of _typeString:
		#
		#       field_static_lookup_code
		#       field_date_format
		#
		#   _attributeValue should be the raw value to be formatted.
		#   _typeString should be a recognized cv_affordance-type code.
		#   _categoryCode is needed when converting 'Category' affordance types.
		#   _sitePreferencesDict is needed to get the Site's date display format preferences.

		if not _attributeValue: return ''
		if not _fieldDict: return ''
		if not _typeString: return ''

		typeUC = _typeString.upper()
		if typeUC == 'TEXT': return self.formatText(_attributeValue, _fieldDict, isPrintedCV)
		if typeUC == 'TEXTAREA': return self.formatText(_attributeValue, _fieldDict, isPrintedCV)
		if typeUC == 'RADIO': return self.formatStaticDropdown(_attributeValue, _fieldDict, isPrintedCV)
		if typeUC == 'CHECKBOX': return self.formatCheckbox(_attributeValue, _fieldDict)
		if typeUC == 'STATIC_DROPDOWN':
			value = self.formatStaticDropdown(_attributeValue, _fieldDict, isPrintedCV)
			return self.formatText(value,_fieldDict,isPrintedCV)
		if typeUC == 'CATEGORY':
			value = self.formatCategory(_attributeValue, _fieldDict, _categoryCode)
			return self.formatText(value,_fieldDict,isPrintedCV)
		if typeUC == 'DATE': return self.formatDate(_attributeValue, _fieldDict, _sitePreferencesDict)
		if typeUC == 'REPEATING_TEXT': return self.formatRepeat(_attributeValue, _fieldDict,isPrintedCV)
		if typeUC == 'REPEATING_TEXT_SELECTOR': return self.formatRepeatTextSelector(_attributeValue, _fieldDict,isPrintedCV)

	def parseDisplayValueForPersistence(self, _displayValue, _fieldDict, _typeString, _categoryCode, _sitePreferencesDict):

		#   Format the given _displayValue for human consumption.
		#
		#   The _fieldDict should contain the following keys, the values of
		#   which may, or may not, be applicable to the formatting process,
		#   depending on the value of _typeString:
		#
		#       field_static_lookup_code
		#       field_date_format
		#
		#   _displayValue should be the raw value to be formatted.
		#   _typeString should be a recognized cv_affordance-type code.
		#   _categoryCode is needed when converting 'Category' affordance types.
		#   _sitePreferencesDict is needed to get the Site's date display format preferences.

		if not _fieldDict: return ''
		if not _typeString: return ''

		typeUC = _typeString.upper()
		if typeUC == 'TEXT': return self.parseText(_displayValue, _fieldDict)
		if typeUC == 'TEXTAREA': return self.parseText(_displayValue, _fieldDict)
		if typeUC == 'RADIO': return self.parseStaticDropdown(_displayValue, _fieldDict)
		if typeUC == 'CHECKBOX': return self.parseCheckbox(_displayValue, _fieldDict)
		if typeUC == 'STATIC_DROPDOWN': return self.parseStaticDropdown(_displayValue, _fieldDict)
		if typeUC == 'CATEGORY': return self.parseCategory(_displayValue, _fieldDict, _categoryCode)
		if typeUC == 'DATE': return self.parseDate(_displayValue, _fieldDict, _sitePreferencesDict)
		if typeUC == 'REPEATING_TEXT': return self.parseRepeat(_displayValue, _fieldDict)
		if typeUC == 'REPEATING_TEXT_SELECTOR': return self.parseRepeatTextSelector(_displayValue, _fieldDict)

		return self.parseText(_displayValue, _fieldDict)


	#   Formatting Worker bees.

	def formatText(self, _attributeValue, _fieldDict, isPrintedCV):
		if isPrintedCV:
			return self.getStyledText(_attributeValue, _fieldDict)
		return _attributeValue

	def formatRepeat(self, _attributeValue, _fieldDict, isPrintedCV = False):
		if isPrintedCV:
			try:
				textList = json.loads(_attributeValue)
				joinedValue = self.repeatDelimiter.join(textList)
				return self.getStyledText(joinedValue,_fieldDict)
			except Exception, e:
				pass
		return _attributeValue

	def formatRepeatTextSelector(self, _attributeValue, _fieldDict, isPrintedCV = False):
		if isPrintedCV:
			try:
				textList = json.loads(_attributeValue)
				joinedValue = self.repeatDelimiter.join(textList)
				return self.getStyledText(joinedValue,_fieldDict)
			except Exception, e:
				pass
		return _attributeValue

	def formatStaticDropdown(self, _attributeValue, _fieldDict, isPrintedCV):
		lookupKey = _fieldDict.get('field_static_lookup_code', '')
		self._loadStaticCacheForKey(lookupKey)
		myLittleCache = self.staticDictCache.get(lookupKey, {})

		if _attributeValue in myLittleCache:
			myLittleDict = myLittleCache[_attributeValue]
			if isPrintedCV and 'pdfalt' in _fieldDict.get('field_list_display_options', ''):
				return myLittleDict.get('alt_descr', '') or myLittleDict.get('descr', '')
			if 'code' in _fieldDict.get('field_list_display_options', ''):
				return myLittleDict.get('code', '')
			return myLittleDict.get('descr', '')
		return _attributeValue

	def formatCategory(self, _attributeValue, _fieldDict, _categoryCode):
		self._loadCategoryCacheForKey(_categoryCode)
		myLittleCache = self.categoryCache.get(_categoryCode, {})

		if _attributeValue in myLittleCache:
			return myLittleCache[_attributeValue].get('descr', '')
		return _attributeValue

	def formatCheckbox(self, _attributeValue, _fieldDict):
		if _attributeValue == 'true':
			value = _fieldDict.get('field_alt_descr','') or _fieldDict.get('field_descr','')
			if value:
				return "(%s)" % value
		return ''

	def formatDate(self, _attributeValue, _fieldDict, _sitePreferencesDict):
		attributeValueLen = len(_attributeValue)
		if not attributeValueLen:
			return ''

		attributeDateFormat = _fieldDict.get('field_date_format', '')
		magicPhrase = self.identifyMagicPhrase(_attributeValue, attributeDateFormat)
		if magicPhrase:
			return magicPhrase

		attributeDateFormat = attributeDateFormat.upper()
		if ',' in attributeDateFormat:
			allowableDateFormats = attributeDateFormat.split(',')
			if attributeValueLen == 4 and 'Y' in allowableDateFormats:
				formatKey = 'Y'
			elif attributeValueLen == 7 and 'M/Y' in allowableDateFormats:
				formatKey = 'M/Y'
			elif attributeValueLen == 10 and 'M/D/Y' in allowableDateFormats:
				formatKey = 'M/D/Y'
			else:
				formatKey = allowableDateFormats[0]
		else:
			formatKey = attributeDateFormat

		format = ''
		formatKey = self.getDateFormatKey(formatKey)
		if formatKey:
			format = _sitePreferencesDict.get(formatKey, '')
		return dateUtils.parseDate(_attributeValue, format)


	#   Parsing Worker bees.

	def parseText(self, _displayValue, _fieldDict):
		return _displayValue

	def parseStaticDropdown(self, _displayValue, _fieldDict):
		if not _displayValue:
			return ''
		lookupKey = _fieldDict.get('field_static_lookup_code', '')
		self._loadStaticCacheForKey(lookupKey)
		myLittleCache = self.staticDictCache.get(lookupKey, {})

		if not _displayValue in myLittleCache:
			raise excUtils.MPSValidationException("Invalid %s" % _fieldDict.get('field_descr', ''))
		return _displayValue

	def parseCategory(self, _displayValue, _fieldDict, _categoryCode):
		self._loadCategoryCacheForKey(_categoryCode)
		myLittleCache = self.categoryCache.get(_categoryCode, {})

		if _displayValue and not _displayValue in myLittleCache:
			raise excUtils.MPSValidationException("Invalid %s" % _fieldDict.get('field_descr', ''))
		return _displayValue

	def parseCheckbox(self, _displayValue, _fieldDict):
		if _displayValue:
			displayValueUC = _displayValue.upper()
			if displayValueUC == 'TRUE': return 'true'
		return 'false'

	def parseDate(self, _displayValue, _fieldDict, _sitePreferencesDict):
		if not _displayValue:
			return ''

		#   Watch for Magic Phrases.

		attributeDateFormat = _fieldDict.get('field_date_format', '')
		magicPhrase = self.identifyMagicPhrase(_displayValue, attributeDateFormat)
		if magicPhrase:
			return magicPhrase

		#   Match one of the allowable date formats.

		attributeDateFormat = attributeDateFormat.upper()
		allowedFormats = attributeDateFormat.split(',')
		for formatSpecifier in allowedFormats:
			formatKey = self.getDateFormatKey(formatSpecifier)
			if formatKey:
				try:
					pattern = _sitePreferencesDict.get(formatKey, '')
					parsed = dateUtils.flexibleDateMatch(_displayValue, pattern)

					if formatSpecifier == 'Y':
						return str(parsed.year).rjust(4,'0')
					if formatSpecifier == 'M/Y':
						return "%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'))
					if formatSpecifier == 'M/D/Y':
						return "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
				except Exception, e:
					pass

		raise excUtils.MPSValidationException("Invalid %s" % _fieldDict.get('field_descr', ''))

	def parseRepeat(self, _displayValue, _fieldDict):
		#   Result needs to be a JSON list.
		#   Input could already be a JSON list, or could be a single unJSONified string.

		parts = []
		if _displayValue:
			if type(_displayValue) is list:
				parts = _displayValue
			elif type(_displayValue) is str:
				parts.append(_displayValue)
			elif type(_displayValue) is unicode:
				parts.append(_displayValue)

		return json.dumps(parts)

	def parseRepeatTextSelector(self, _displayValue, _fieldDict):
		#   Result needs to be a JSON list.
		#   Input could already be a JSON list, or could be a single unJSONified string.

		parts = []
		if _displayValue:
			if type(_displayValue) is list:
				parts = _displayValue
			elif type(_displayValue) is str:
				parts.append(_displayValue)
			elif type(_displayValue) is unicode:
				parts.append(_displayValue)

		return json.dumps(parts)

	#   Utility.

	def getStyledText(self, _attributeValue, _fieldDict):
		displayOptions = _fieldDict.get('field_list_display_options','')
		attributeValue = _attributeValue
		if 'label' in displayOptions and attributeValue:
			attributeValue = "%s: %s" % (_fieldDict.get('field_descr'),attributeValue)
		if 'bold' in displayOptions:
			attributeValue = "<b>%s</b>" % (attributeValue)
		if 'underline' in displayOptions:
			attributeValue = "<u>%s</u>" % (attributeValue)
		if 'italic' in displayOptions:
			attributeValue = "<i>%s</i>" % (attributeValue)
		if 'center' in displayOptions:
			attributeValue = "<center>%s</center>" % (attributeValue)
		if 'linebreak' in displayOptions:
			attributeValue = '<div class="clearfix">%s</div>' % (attributeValue)
		if 'parens' in displayOptions:
			attributeValue = '(%s)' % (attributeValue)
		if 'quote' in displayOptions:
			if not attributeValue.startswith('"'):
				attributeValue = '"%s"' % (attributeValue)
		if 'prepend' in displayOptions:
			attributeValue = self.getPrePostPendendedAttributeValue('prepend',attributeValue,displayOptions)
		if 'postpend' in displayOptions:
			attributeValue = self.getPrePostPendendedAttributeValue('postpend',attributeValue,displayOptions)

		return attributeValue

	def getPrePostPendendedAttributeValue(self,preOrPost,_attributeValue,_displayOptions):
		returnValue = _attributeValue
		beginIdx = _displayOptions.find(preOrPost + '|')
		if beginIdx > -1:
			tmpStr = _displayOptions[beginIdx:9999]
			splits = tmpStr.split('|')
			if len(splits) == 2:
				appendValue = splits[1]
				if preOrPost == 'prepend':
					returnValue = "%s %s" % (appendValue,_attributeValue)
				else:
					returnValue = "%s %s" % (_attributeValue,appendValue)
		return returnValue

	def identifyMagicPhrase(self, _attributeValue, _attributeDateFormat):
		magicPhrases = []
		knownFormats = ['Y','M/Y','M/D/Y']
		for each in _attributeDateFormat.split(','):
			if each.upper() not in knownFormats:
				magicPhrases.append(each)

		attributeValueUC = _attributeValue.upper()
		for phrase in magicPhrases:
			if phrase.upper() == attributeValueUC:
				return phrase

		return None

	def getDateFormatKey(self, _attributeDateFormat):
		if _attributeDateFormat == "Y": return 'yformat'
		if _attributeDateFormat == "M/Y": return 'ymformat'
		if _attributeDateFormat == "M/D/Y": return 'ymdformat'
		return ''

	def _loadStaticCacheForKey(self, _lookupKey):
		if not _lookupKey: return
		if _lookupKey in self.staticDictCache: return

		staticList = metaSvc.getStaticLookupData(self.dbConnection, _lookupKey)
		self.staticListCache[_lookupKey] = staticList
		self.staticDictCache[_lookupKey] = self._convertListToDict(staticList)

	def _loadCategoryCacheForKey(self, _categoryCode):
		if not _categoryCode: return
		if _categoryCode in self.categoryCache: return

		categoryList = metaSvc.getSubCategoriesForCategory(self.dbConnection, _categoryCode)
		self.categoryCache[_categoryCode] = self._convertListToDict(categoryList)

	def _convertListToDict(self, _list):
		result = {}
		for each in _list:
			code = each.get('code', None)
			if code:
				result[code] = each
		return result
