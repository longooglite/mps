# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import operator
import json
import os
import tornado.template

from MPSCV.services import metaService
from MPSCV.services import cvService
import MPSCore.utilities.dictUtilities as dictUtils
import MPSCV.utilities.viewMaster as viewMstr
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.PDFUtils as pdfUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

class CVPrintService():
	def __init__(self,_dbConnection, _initalContext, _subjectProfile, _sitePreferences,_template,_environment):
		self.connection = _dbConnection
		self.subjectProfile = _subjectProfile
		self.sitePreferences = _sitePreferences
		self.template = _template
		self.initalContext = _initalContext
		self.environment = _environment

	#   printing
	def renderCVToPDF(self,categoryCode = None):
		community = self.subjectProfile.get('community', '')
		username = self.subjectProfile.get('username', '')

		if categoryCode:
			categoryDicts = []
			categoryContext = self.getCategoryViewContext(self.connection, categoryCode, community, username, True)
			catDict = {}
			catDict['categoryDict'] = categoryContext.get('categoryDict',{})
			catDict['rowDataDict'] = categoryContext.get('rowDataDict',{})
			categoryDicts.append(catDict)
		else:
			categories = metaService.getAllCategories(self.connection)
			categoryDicts = []
			for cat in categories:
				categoryContext = self.getCategoryViewContext(self.connection,cat.get('code',''), community, username, True)
				catDict = {}
				catDict['categoryDict'] = categoryContext.get('categoryDict',{})
				catDict['rowDataDict'] = categoryContext.get('rowDataDict',{})
				categoryDicts.append(catDict)
			categoryDicts = self.removeEmptyDicts(categoryDicts)

		printDicts = self.getPrintDicts(self.connection, categoryDicts)
		context = self.getInitialTemplateContext()
		context['categories'] = categoryDicts
		context['printDicts'] = printDicts
		context['printCatDict'] = self.getPrintCatDict(printDicts)
		fullName = self.getFullName(self.connection, self.subjectProfile)

		pdfhtml = self.render_template(self.template, context=context, skin=context['skin'])
		pdffilename,fullPath = self.createPDFFromHTML(pdfhtml,fullName)
		return pdffilename,fullPath

	def render_template(self,template_name, **kwargs):
		html = 'template not found'
		env = self.environment
		rootTemplatePaths = env.buildFullPathToCVSiteTemplatesList(self.initalContext.get('site',''))
		templatePath = None
		rootTemplatePath = ''
		foundTemplate = False
		for rootTemplatePath in rootTemplatePaths:
			templatePath = os.path.join(rootTemplatePath,template_name)
			if os.path.exists(templatePath):
				foundTemplate = True
				break
		if foundTemplate:
			loader = tornado.template.Loader(rootTemplatePath)
			template = loader.load(template_name)

			html = template.generate(**kwargs)
		return html

	@mpsExceptionWrapper("Unable to create PDF")
	def createPDFFromHTML(self, html, name = ""):
		pdf,fullPath = pdfUtils.createPDFFromHTML(html, self.environment, name)
		return pdf,fullPath

	def getPrintCatDict(self,printDicts):
		returnVal = {}
		for each in printDicts:
			returnVal[each.get('category_code','')] = each
		return returnVal

	def getPrintDicts(self,connection,categoryDicts):
		categoryList = []
		for catDict in categoryDicts:
			categoryDict = catDict.get('categoryDict',{})
			category = {}
			category['parent_code'] = categoryDict.get('category_parent_code','')
			category['category_code'] = categoryDict.get('category_code','')
			category['descr'] = categoryDict.get('category_descr')
			subDescr = categoryDict.get('category_descr')
			category['mode_code'] = categoryDict.get('mode_code')
			category['isNumberedList'] = False
			category['isThreeLevelDisplay'] = False
			if "3levelpresentation" in catDict.get('categoryDict',{}).get('category_display_options',''):
				category['isThreeLevelDisplay'] = True
			if "numberedlist" in catDict.get('categoryDict',{}).get('category_display_options',''):
				category['isNumberedList'] = True
			category['subcategories'] = []

			for subcategoryGroup in catDict.get('categoryDict',{}).get('groupList',[]):
				#for subcategorykey in catDict.get('rowDataDict',{}):
				subcategorykey = subcategoryGroup.get('group_code','')
				rowDataDict = catDict.get('rowDataDict',{}).get(subcategorykey,{})
				subCategory = {}
				subCategory['sub_descr'] = subDescr
				subCategory['display'] = True
				if category.get('mode_code','') == 'ListSingleEntry':
					subCategory['display'] = False
				subCategory['descr'] = rowDataDict.get('group_descr','')
				subCategory['subcategory_code'] = rowDataDict.get('group_code','')
				subCategory['rows'] = []
				for rowDict in rowDataDict.get('rowList',[]):
					row = {'fields' : []}
					row['rawfields'] = rowDict.get('undoctoredfieldList',[])
					for fieldDict in rowDict.get('fieldList',{}):
						field = {}
						field['formatted_value'] = fieldDict.get('formatted_value')
						field['field_code'] = fieldDict.get('field_code','')
						row['fields'].append(field)
					subCategory['rows'].append(row)
				if len(subCategory.get('rows',[])) > 0:
					category['subcategories'].append(subCategory)

			if len(category.get('subcategories',[])) > 0:
				categoryList.append(category)
		parentAssignedCategoryList = self.assignToParent(connection,categoryList)
		return parentAssignedCategoryList

	def assignToParent(self,connection,categoryList):
		parentCategories = self.getParentCategories(connection)
		newCategoryList = []
		for cat in categoryList:
			if cat.get('parent_code','') == '':
				newCategoryList.append(cat)
			else:
				parentCode = cat.get('parent_code','')
				descr = parentCategories.get(parentCode,'')
				if descr <> 'DUN':
					parentCategory = {}
					parentCategory['parent_code'] = ''
					parentCategory['category_code'] = parentCode
					parentCategory['descr'] = descr
					parentCategories[parentCode] = 'DUN'
					parentCategory['mode_code'] = cat.get('mode_code','')
					parentCategory['isNumberedList'] = cat.get('isNumberedList',False)
					parentCategory['isThreeLevelDisplay'] = cat.get('isThreeLevelDisplay',False)
					parentCategory['subcategories'] = []
					for childCat in categoryList:
						if childCat.get('parent_code','') == cat.get('parent_code',''):
							for subcats in childCat.get('subcategories',[]):
								parentCategory['subcategories'].append(subcats)
					newCategoryList.append(parentCategory)
		return newCategoryList

	def getParentCategories(self,connection):
		parentCategories = {}
		rawParentCategories = metaService.getParentCategories(connection)
		for each in rawParentCategories:
			parentCategories[each.get('code','')] = each.get('descr','')
		return parentCategories

	#   both print and page rendering

	def getCategoryViewContext(self, connection, category, community, user_id, isPrintedCV = False):
		#   Get Categories, Subcategories, and CV Data to drive the List display.
		#   First marry up the list of SubCategories for the current Category
		#   with the list of fields to be displayed. We need this in order to
		#   display the correct groups and columns, even if there are no data
		#   records for the Category.

		categoryDict = metaService.getSubCategoriesByGroupForCategory(connection, category)
		fieldList = metaService.getFieldsForCategory(connection, category, _orderFor='PDF' if isPrintedCV else 'LIST')
		self.addDisplayFields(categoryDict, fieldList, isPrintedCV)

		#   Go get the data that is associated with this Category.
		#   This is a rather involved process with a little database access and
		#   lots of in-memory munging to organize the data for display.

		rowDataDict = cvService.getCVListDisplayDataForUser(connection, community, user_id, category, isPrintedCV)
		self.formatRowDataForDisplay(rowDataDict, community, user_id, category, connection, isPrintedCV)
		self.sortRowDataForDisplay(rowDataDict, categoryDict)
		self.combineDataColumns(rowDataDict,isPrintedCV)
		self.combineColumnHeaders(categoryDict,isPrintedCV)
		if not isPrintedCV:
			self.applyWhoDunit(user_id, rowDataDict)

		#   Render the page.
		context = self.getInitialTemplateContext()
		context['cvOwnerName'] = self.getCvOwnerFormalName(connection, self.subjectProfile)
		context['subjectProfile'] = self.subjectProfile
		context['categoryDict'] = categoryDict
		context['rowDataDict'] = rowDataDict
		return context

	def getCvOwnerFormalName(self, _connection, _subjectProfile):
		cvNameCode = self.sitePreferences.get('cvnamecode', '')
		if cvNameCode:
			community = _subjectProfile.get('community', 'default')
			username = _subjectProfile.get('username','')
			formalNameList = cvService.getFormalName(_connection, community, username, cvNameCode)
			if formalNameList:
				formalName = formalNameList[0].get('attribute_value','')
				if formalName:
					return formalName

		return _subjectProfile.get('userPreferences',{}).get('full_name','')

	def combineColumnHeaders(self, _categoryDict, isPrintedCV = False):

		#   Multiple data Fields can be displayed in a single column.
		#   This routine collapses column headings as appropriate.

		lastSeqNbr = None
		newFieldList = []
		oldFieldList = _categoryDict.get('displayFieldList',[])
		for thisFieldDict in oldFieldList:
			if isPrintedCV:
				thisSeqNbr = thisFieldDict.get('field_display_on_pdf_seq', 0)
			else:
				thisSeqNbr = thisFieldDict.get('field_display_on_list_seq', 0)

			if thisSeqNbr != lastSeqNbr:
				newFieldList.append(thisFieldDict)
				lastSeqNbr = thisSeqNbr

		_categoryDict['displayFieldList'] = newFieldList

	def combineDataColumns(self, _rowDataDict, isPrintedCV = False):

		#   Multiple data Fields can be displayed in a single column.
		#   This routine collapses row data from multiple columns into one as appropriate.

		for thisKey in _rowDataDict.keys():
			thisSubcategoryDict = _rowDataDict[thisKey]
			if 'rowList' in thisSubcategoryDict:
				thisRowList = thisSubcategoryDict['rowList']
				for thisRowDict in thisRowList:
					if 'fieldList' in thisRowDict:
						thisFieldList = thisRowDict['fieldList']

						lastSeqNbr = None
						lastFieldDict = None
						newFieldList = []
						for thisFieldDict in thisFieldList:
							if isPrintedCV:
								thisSeqNbr = self.normalizeSequenceValue(thisFieldDict.get('field_display_on_pdf_seq', ''))
							else:
								thisSeqNbr = self.normalizeSequenceValue(thisFieldDict.get('field_display_on_list_seq', ''))

							if thisSeqNbr != lastSeqNbr:
								newFieldList.append(thisFieldDict)
								lastSeqNbr = thisSeqNbr
								lastFieldDict = thisFieldDict
							else:
								myValue = thisFieldDict['formatted_value']
								lastValue = lastFieldDict['formatted_value']
								sep = ''
								if len(myValue.strip()) > 0:
									sep = ", "
									display_options = thisFieldDict.get('field_list_display_options','')
									if "dashsep" in display_options:
										sep = " - "
									if "slashsep" in display_options:
										sep = " / "
									if "colonsep" in display_options:
										sep = ": "
									if "spacesep" in display_options:
										sep = "&nbsp;"
									if "periodsep" in display_options:
										sep = ". "
									if "semicolonsep" in display_options:
										sep = "; "
									if "nosep" in display_options:
										sep = ""

								if myValue:
									if lastValue and not lastValue.strip().endswith(sep.strip()) and not lastValue.strip().endswith('<br/>'):
										lastValue += sep
									if lastValue.endswith('.'):
										lastValue += ' '
									lastValue += myValue
									lastValue = lastValue.replace('&nbsp;', ' ')
									lastFieldDict['formatted_value'] = lastValue

						thisRowDict['fieldList'] = newFieldList
						thisRowDict['undoctoredfieldList'] = thisFieldList

	def normalizeSequenceValue(self, _rawSequenceValue):
		if not _rawSequenceValue:
			return ''
		return _rawSequenceValue.split('.')[0]

	def sortRowDataForDisplay(self, _rowDataDict, _categoryDict):

		#   Sort the data for display.
		#   The Field metadata specifies which fields are used to sort.
		#   Alternatively, the Category may specify user-defined row ordering.

		gotSortKeys = False
		sortKeyList = []
		userSortable = _categoryDict.get('category_user_sortable', False)

		for thisKey in _rowDataDict.keys():
			thisSubcategoryDict = _rowDataDict[thisKey]
			if 'rowList' in thisSubcategoryDict:
				thisRowList = thisSubcategoryDict['rowList']
				for thisRowDict in thisRowList:
					sortKey = ''
					thisRowDict['category_user_sortable'] = userSortable
					if 'fieldList' in thisRowDict:
						thisFieldList = thisRowDict['fieldList']
						if not gotSortKeys:
							sortKeyList = self.getSortKeysFromFieldList(thisFieldList)
							gotSortKeys = True
						sortKey = self.buildOneSortKey(thisRowDict, thisFieldList, sortKeyList)
					thisRowDict['sortKey'] = sortKey
				thisSubcategoryDict['rowList'] = sorted(thisRowList, key=operator.itemgetter('sortKey'))

	def getSortKeysFromFieldList(self, _fieldList):
		#   Extract a list of the Fields to be used for the initial sort.
		sortList = []
		for fieldDict in _fieldList:
			sortSeq = fieldDict.get('field_list_sort_key_seq', 0)
			if sortSeq > 0:
				sortList.append(fieldDict)
		sorted(sortList, key=operator.itemgetter('field_list_sort_key_seq'))

		keyList = []
		for fieldDict in sortList:
			fieldCode = fieldDict.get('field_code', '')
			if fieldCode:
				keyList.append(fieldCode)
		return keyList

	def buildOneSortKey(self, _rowDict, _fieldList, _sortKeyList):
		values = []
		if _rowDict.get('category_user_sortable', False):
			values.append('%010d' % _rowDict.get('row_user_sort_seq', 0))
		else:
			for sortKey in _sortKeyList:
				for fieldDict in _fieldList:
					if fieldDict.get('field_code', '') == sortKey:
						values.append(fieldDict.get('attribute_value', '').ljust(200))
						break

		values.append('%010d' % _rowDict.get('row_id', 0))
		return '|'.join(values)

	def formatRowDataForDisplay(self, _rowDataDict, _community, _username, _categoryCode, _dbConnection, isPrintedCV = False):

		#   Given a collection of rows to be displayed, add a 'formatted_value' to each.
		#   This field is computed by trans-mogrifying the stored 'attribute_value'
		#   on each row based on the field's 'affordance_code' (i.e. type of field:
		#   text, date, lookup list, etc).

		viewMaster = viewMstr.ViewMaster(_dbConnection)

		for thisKey in _rowDataDict.keys():
			thisSubcategoryDict = _rowDataDict[thisKey]
			if 'rowList' in thisSubcategoryDict:
				thisRowList = thisSubcategoryDict['rowList']
				for thisRowDict in thisRowList:
					thisRowDict['editURL'] = '/'.join(['','cv','edit',_community,_username,_categoryCode,str(thisRowDict.get('row_id','0'))])
					if 'fieldList' in thisRowDict:
						thisFieldList = thisRowDict['fieldList']
						for thisFieldDict in thisFieldList:
							attributeValue = thisFieldDict.get('attribute_value', '')
							typeString = thisFieldDict.get('affordance_code', '')
							formattedValue = viewMaster.formatAttributeValueForDisplay(attributeValue, thisFieldDict, typeString, _categoryCode, self.sitePreferences, isPrintedCV)
							thisFieldDict['formatted_value'] = formattedValue.strip()


	def addDisplayFields(self, _categoryDict, _fieldList, isPrintedCV = False):

		#   Add list of fields that get displayed onto the Category information.

		if _categoryDict:
			displayFieldList = []
			_categoryDict['displayFieldList'] = displayFieldList

			if _fieldList:
				for fieldDict in _fieldList:
					if isPrintedCV:
						displaySeq = fieldDict.get('field_display_on_pdf_seq', '')
					else:
						displaySeq = fieldDict.get('field_display_on_list_seq', '')

					if displaySeq:
						displayDict = {}
						dictUtils.copyKeysWithPrefix(fieldDict, displayDict, 'field_')
						dictUtils.copyKeysWithPrefix(fieldDict, displayDict, 'affordance_')
						displayFieldList.append(displayDict)

	def getFullName(self, connection, subjectProfile):
		fullName = ''
		cvNameCode = self.sitePreferences.get('cvnamecode', '')
		if cvNameCode:
			community = subjectProfile.get('community', 'default')
			username = subjectProfile.get('username','')
			nameQry = cvService.getFormalName(connection,community, username,cvNameCode)
			if len(nameQry) > 0:
				fullName = nameQry[0].get('attribute_value','')
		if fullName == '':
			fullName = self.subjectProfile.get('userProfile', {}).get('userPreferences', {}).get('full_name', '')

		return fullName

	def applyWhoDunit(self, _cvOwnerUsername, _rowDataDict):

		#   Add a 'row_updated' attribute to each row.

		for thisKey in _rowDataDict.keys():
			thisSubcategoryDict = _rowDataDict[thisKey]
			if 'rowList' in thisSubcategoryDict:
				thisRowList = thisSubcategoryDict['rowList']
				for thisRowDict in thisRowList:
					thisRowDict['row_updated'] = ''
					lastEditor = thisRowDict.get('row_who_dunit', '')
					dataList = [lastEditor, dateUtils.parseDate(thisRowDict.get('row_when_dunit', ''), self.getSiteYearMonthDayFormat())]
					thisRowDict['row_updated'] = json.dumps(dataList)

	def getSiteYearMonthDayFormat(self): return self.sitePreferences.get('ymdformat', '%m/%d/%Y')

	def getInitialTemplateContext(self):
		context = self.initalContext
		context['windowTitle'] = 'Curriculum Vitae'
		context['pageHeaderTitle'] = 'Curriculum Vitae'
		return context

	def removeEmptyDicts(self, demDicts):
		keepers = []
		for each in demDicts:
			categoryDict = each.get('categoryDict')
			if categoryDict.get('displayFieldList',[]) <> []:
				keepers.append(each)
		return keepers

