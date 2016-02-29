# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.core.sql.lookupTableSQL as lookupTableSQL

class AbstractUberAdminHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def getQuestionDataTypes(self):
		dataTypes = [
			{ "code": "Text", "descr": "Text" },
			{ "code": "TextArea", "descr": "Text Area" },
			{ "code": "Repeating_Text", "descr": "Repeating Text" },
			{ "code": "Radio", "descr": "Radio" },
			{ "code": "Checkbox", "descr": "Checkbox" },
			{ "code": "Dropdown", "descr": "Dropdown" },
			{ "code": "Multi_Dropdown", "descr": "Multi-Select Dropdown" },
			{ "code": "Date", "descr": "Date" },
		]
		return dataTypes

	def getQuestionDataTypesCache(self):
		cache = {}
		for each in self.getQuestionDataTypes():
			cache[each['code']] = each
		return cache

	def getJobActionTypes(self, _connection):
		return lookupTableSQL.getLookupTable(_connection, 'wf_job_action_type', _orderBy='descr')

	def getJobActionTypesCache(self, _connection):
		cache = {}
		for each in self.getJobActionTypes(_connection):
			cache[each['code']] = each
		return cache

	def getMaxJobActionTypes(self):
		return self.getSitePreferenceAsInt('apptadminubermaxjobactiontypes', 5)

	def getMaxOptions(self):
		return self.getSitePreferenceAsInt('apptadminubermaxoptions', 10)

	def getMaxGroupChildren(self):
		return self.getSitePreferenceAsInt('apptadminubermaxgroupchildren', 40)

	def _validateInteger(self, _formData, _key, _defaultValue, _jErrors):
		if _formData.has_key(_key):
			value = _formData.get(_key, '0')
			if not value:
				_formData[_key] = _defaultValue
			try:
				_formData[_key] = int(_formData[_key])
			except Exception, e:
				_jErrors.append({'code':_key, 'field_value': value, 'message': "Must be a number"})
		else:
			_formData[_key] = _defaultValue

	def _duplicateCodeCheck(self, _connection, _value, _fieldName, _jErrors):
		self._checkOneCode(_connection, _value, _fieldName, 'wf_uber_question', _jErrors, 'Question')
		self._checkOneCode(_connection, _value, _fieldName, 'wf_uber_option', _jErrors, 'Option')
		self._checkOneCode(_connection, _value, _fieldName, 'wf_uber_group', _jErrors, 'Group')

	def _checkOneCode(self, _connection, _code, _fieldName, _tableName, _jErrors, _blurb):
		if lookupTableSvc.getEntityByKey(_connection, _tableName, _code, _key='code'):
			_jErrors.append({ 'code': _fieldName, 'field_value': _code, 'message': 'Already exists as %s' % _blurb })
