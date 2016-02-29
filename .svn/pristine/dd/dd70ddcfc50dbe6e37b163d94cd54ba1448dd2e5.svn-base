# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSCore.utilities.dictUtilities as dictUtils
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCV.handlers.abstractHandler as absHandler
import MPSCV.services.cvService as cvSvc
import MPSCV.services.metaService as metaSvc
import MPSCV.utilities.environmentUtils as envUtils
import MPSCV.utilities.viewMaster as viewMstr

class AbstractDetailHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def applyDataValuesToFields(self, _groupList, _rowData, _category, _viewMaster, sitePreferences):
		for groupDict in _groupList:
			for fieldDict in groupDict.get('fieldList', []):
				fieldDict['formatted_value'] = ''
				fieldDict['placeholder'] = ''
				fieldDict['tooltip'] = ''
				typeString = fieldDict.get('affordance_code', '')

				attributeDict = self.findAttributeDataForField(fieldDict, _rowData)
				if attributeDict:
					dictUtils.copyKeysWithPrefix(attributeDict, fieldDict, 'attribute_')
					attributeValue = attributeDict.get('attribute_value', '')
					formattedValue = _viewMaster.formatAttributeValueForDisplay(attributeValue, fieldDict, typeString, _category, sitePreferences)
					fieldDict['formatted_value'] = formattedValue

				if typeString.upper() == 'DATE':
					attributeDateFormat = fieldDict.get('field_date_format', '')
					if attributeDateFormat:
						allowedFormats = attributeDateFormat.split(',')
						optionList = []
						for allowedFormat in allowedFormats:
							formatKey = _viewMaster.getDateFormatKey(allowedFormat.upper())
							if formatKey:
								pattern = sitePreferences.get(formatKey, '')
								pattern = self.mungeDatePatternForDisplay(pattern)
							else:
								pattern = allowedFormat

							if not fieldDict['placeholder']:
								fieldDict['placeholder'] = pattern
							optionList.append(pattern)

						lenOptionList = len(optionList)
						if lenOptionList < 3:
							fieldDict['tooltip'] = " or ".join(optionList)
						else:
							limit = lenOptionList - 1
							commaChunk = ", ".join(optionList[0:limit])
							fieldDict['tooltip'] = commaChunk + ', or ' + optionList[limit]

	def findAttributeDataForField(self, _fieldDict, _rowData):
		fieldId = _fieldDict.get('field_id', 0)
		if fieldId:
			for attributeDict in _rowData:
				if attributeDict.get('attribute_field_id', 0) == fieldId:
					return attributeDict
		return None

	def findCategoryFieldDict(self, _groupList):
		if _groupList:
			for groupDict in _groupList:
				for fieldDict in groupDict.get('fieldList', []):
					if fieldDict.get('affordance_code', '') == 'Category':
						return fieldDict
		return None

	def mungeDatePatternForDisplay(self, _pattern):
		pattern = _pattern.replace('%m', 'MM')
		pattern = pattern.replace('%d', 'DD')
		pattern = pattern.replace('%Y', 'YYYY')
		return pattern


class DetailHandler(AbstractDetailHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['cvView','cvEdit'])

		community = kwargs.get('community', 'default')
		username = kwargs.get('username', '')
		categoryCode = kwargs.get('categoryCode', '')
		rowId = kwargs.get('rowId', '')
		formData = tornado.escape.json_decode(self.request.body)

		if not community or not username or not categoryCode:
			self.redirect("/cv")
			return

		try:
			#   Verify that access is allowed in proxy situations.
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)

			#   Get the profile of the CV Subject (i.e. the person who's CV is being edited).
			subjectProfile = self.getCVSubject(community, username)

			#   Find the Category and Subcategories.
			categoryList = metaSvc.getOneCategory(connection, categoryCode)
			if not categoryList:
				raise excUtils.MPSValidationException("Category not found")
			categoryDict = categoryList[0]
			subcategoryList = metaSvc.getSubCategoriesForCategory(connection, categoryCode)

			#   Get Field list by detail display group.
			#   Apply any existing data values for the Row.
			groupList = metaSvc.getFieldsByGroupForCategory(connection, categoryCode, _orderFor='DETAIL')
			rowDict = {}
			rowData = []
			if rowId:
				rowData = cvSvc.getRowData(connection, rowId)
				if rowData:
					dictUtils.copyKeysWithPrefix(rowData[0], rowDict, 'row_')
				else:
					result = cvSvc.getRow(connection, rowId)
					if result:
						dictUtils.copyKeysWithPrefix(result[0], rowDict, 'row_')

			viewMaster = viewMstr.ViewMaster(connection)
			sitePreferences = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})
			self.applyDataValuesToFields(groupList, rowData, categoryCode, viewMaster, sitePreferences)

			#   Apply initial Category value for Add.
			tab_title = formData.get('tabTitle', '')
			if not rowId or rowId == '0':
				subCategoryCode = self.getFirstSubCategoryCodeForTabTitle(tab_title, subcategoryList)
				if subCategoryCode:
					self.applySubCategoryValue(subCategoryCode, groupList)

			#   Determine editability.
			disabled = True
			if self.hasPermission('cvEdit'):
				if not proxyDict:
					disabled = False
				else:
					disabled = not proxyDict.get('can_write', False)

			#   Get static lookup table data.
			staticCodes = self.getStaticLookupCodes(groupList)
			staticLookupTables = viewMaster.getStaticListCache()
			for code in staticCodes:
				if not code in staticLookupTables:
					staticLookupTables[code] = metaSvc.getStaticLookupData(connection, code)

			#   Render the page.
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['cvCommunity'] = community
			context['cvOwner'] = username
			context['categoryCode'] = categoryCode
			context['rowId'] = rowId
			context['path'] = '/'.join(['','cv','view',community,username,categoryCode])

			context['mode'] = "edit" if rowDict else "add"
			context['subjectProfile'] = subjectProfile
			context['categoryDict'] = categoryDict
			context['subcategoryList'] = subcategoryList
			context['rowDict'] = rowDict
			context['groupList'] = groupList
			context['staticLookupTables'] = staticLookupTables
			context['disabled'] = "disabled" if disabled else ""
			context['pageLoadType'] = 'form'

			# Do Not Ship ;!)
			context['testJsonEnumWidget'] = False

			self.render("detail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def getFirstSubCategoryCodeForTabTitle(self, _tabTitle, _subCategoryList):
		if _tabTitle and _subCategoryList:
			for subCategoryDict in _subCategoryList:
				if _tabTitle == subCategoryDict.get('group_descr', ''):
					return subCategoryDict.get('code', '')
		return ''

	def applySubCategoryValue(self, _subCategoryCode, _groupList):
		if _subCategoryCode and _groupList:
			fieldDict = self.findCategoryFieldDict(_groupList)
			if fieldDict:
				if not fieldDict.get('attribute_value', ''):
					fieldDict['attribute_value'] = _subCategoryCode

	def getStaticLookupCodes(self, _groupList):
		staticCodes = []
		for groupDict in _groupList:
			for fieldDict in groupDict.get('fieldList', []):
				affordanceCode = fieldDict.get('affordance_code','')
				if affordanceCode == 'Static_Dropdown' or affordanceCode == 'Radio':
					staticCodes.append(fieldDict.get('field_static_lookup_code', ''))
		return staticCodes


class RowSaveHandler(AbstractDetailHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('cvEdit')

		formData = tornado.escape.json_decode(self.request.body)
		community = formData.get('community', 'default')
		username = formData.get('username', '')
		categoryCode = formData.get('categoryCode', '')
		rowId = formData.get('rowId', '')
		path = formData.get('path', '')

		if not community or not username or not categoryCode:
			self.redirect("/cv")
			return

		try:
			#   Verify that access is allowed in proxy situations.
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)

			#   Find the Category.
			categoryList = metaSvc.getOneCategory(connection, categoryCode)
			if not categoryList:
				raise excUtils.MPSValidationException("Category not found")
			categoryDict = categoryList[0]

			#   Get Field list by detail display group.
			#   The grouping by detail display group is not actually important here, just using common routines.
			#   Apply any existing data values for the Row.
			groupList = metaSvc.getFieldsByGroupForCategory(connection, categoryCode, _orderFor='DETAIL')
			rowDict = {}
			rowData = []
			if rowId:
				rowData = cvSvc.getRowData(connection, rowId)
				if rowData:
					dictUtils.copyKeysWithPrefix(rowData[0], rowDict, 'row_')
				else:
					result = cvSvc.getRow(connection, rowId)
					if result:
						dictUtils.copyKeysWithPrefix(result[0], rowDict, 'row_')

			viewMaster = viewMstr.ViewMaster(connection)
			sitePreferences = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})
			self.applyDataValuesToFields(groupList, rowData, categoryCode, viewMaster, sitePreferences)

			#   Go through the Fields defined for this Category.
			#   Apply values received from the GUI.
			#   Construct lists of work that need to be accomplished:
			#   - a list of Attribute table rows to be Inserted
			#   - a list of Attribute table rows to be Updated

			insertList, updateList, errorList = self.identifyDataChanges(connection, groupList, formData, categoryCode)

			#   Errors nix the operation.
			if errorList:
				raise excUtils.MPSValidationException(errorList)

			#   Exclude From CV, if applicable, applies to the entire row.
			excludeFromCV = False
			if categoryDict.get('exclude_from_cv_display', False):
				excludeFromCV = formData.get('exclude_from_cv_val', False)
			rowDict['exclude_from_cv_val'] = excludeFromCV

			# Save data changes.
			loggedInCommunity = self.getUserProfileCommunity()
			loggedInUser = self.getUserProfileUsername()
			cvSvc.saveRowData(connection, community, username, rowDict, insertList, updateList, loggedInUser)

			#   Determine which tab to return to.
			tabTitle = ''
			fieldDict = self.findCategoryFieldDict(groupList)
			if fieldDict:
				fieldCode = fieldDict.get('field_code', '')
				if fieldCode:
					attribute_value = formData.get(fieldCode, '')
					if attribute_value:
						subcategoryList = metaSvc.getSubCategoriesForCategory(connection, categoryCode)
						subCategoryGroupDescr = self.findGroupDescrForSubCategoryCode(subcategoryList, attribute_value)
						if subCategoryGroupDescr:
							tabTitle = '#tab_' + subCategoryGroupDescr.replace(' ', '')

			responseDict = self.getPostResponseDict("Entry saved")
			responseDict['redirect'] = path + tabTitle
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def findGroupDescrForSubCategoryCode(self, _subCategoryList, _subCategoryCode):
		if _subCategoryList and _subCategoryCode:
			for subCategoryDict in _subCategoryList:
				if _subCategoryCode == subCategoryDict.get('code', ''):
					return subCategoryDict.get('group_descr', '')
		return ''

	def identifyDataChanges(self, _dbConnection, _groupList, _formData, _category):

		#   Given a list of Fields with current values, and a dictionary of data from
		#   the GUI form, construct and return three Lists:
		#
		#   - a list of Attribute table rows to be Inserted
		#   - a list of Attribute table rows to be Updated
		#   - a list of Error messages

		insertList = []
		updateList = []
		errorList = []

		viewMaster = viewMstr.ViewMaster(_dbConnection)
		sitePreferences = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})

		for groupDict in _groupList:
			for fieldDict in groupDict.get('fieldList', []):
				fieldCode = fieldDict.get('field_code', '')
				formValue = _formData.get(fieldCode, '')

				required = fieldDict.get('field_required', False)
				if required and not formValue:
					sMsg = "%s required" % fieldDict.get('field_descr', '')
					jErr = {'code':fieldCode, 'field_value': fieldDict.get('formValue', ''), 'message': sMsg}
					errorList.append(jErr)

				else:
					typeString = fieldDict.get('affordance_code', '')
					try:
						persistValue = viewMaster.parseDisplayValueForPersistence(formValue, fieldDict, typeString, _category, sitePreferences)
						if 'attribute_id' in fieldDict:
							if persistValue != fieldDict.get('attribute_value', ''):
								updateList.append((fieldDict['attribute_id'],persistValue))
						else:
							insertList.append((fieldCode, persistValue))

					except Exception, e:
						if isinstance(e, excUtils.MPSValidationException):
							jErr = {'code':fieldCode, 'field_value': fieldDict.get('formValue', ''), 'message': e.message}
							errorList.append(jErr)
						else:
							raise e

		return insertList, updateList, errorList


#   All URL mappings for this module.
urlMappings = [
	(r'/cv/add/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<categoryCode>[^/]*)/(?P<tabCode>[^/]*)', DetailHandler),
	(r'/cv/add/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<categoryCode>[^/]*)', DetailHandler),
	(r'/cv/edit/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<categoryCode>[^/]*)/(?P<rowId>[^/]*)', DetailHandler),
	(r'/cv/save', RowSaveHandler),
]
