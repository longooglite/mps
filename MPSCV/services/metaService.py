# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCV.core.metaSQL as metaSQL
import MPSCore.utilities.dictUtilities as dictUtils


######################## CV Menus ########################

def getAllCategories(_dbConnection):
	return metaSQL.getAllCategories(_dbConnection)

######################## CV UI ########################

def getOneCategory(_dbConnection, _category):
	return metaSQL.getOneCategory(_dbConnection, _category)

def getSubCategoriesForCategory(_dbConnection, _categoryCode):
	return metaSQL.getSubCategoriesForCategory(_dbConnection, _categoryCode)

def getSubCategoriesByGroupForCategory(_dbConnection, _categoryCode):
	result = {}
	first = True
	lastGroupCode = None
	curGroupDict = None

	flatList = metaSQL.getSubCategoriesByGroupForCategory(_dbConnection, _categoryCode)
	for flatDict in flatList:
		if first:
			dictUtils.copyKeysWithPrefix(flatDict, result, 'category_')
			dictUtils.copyKeysWithPrefix(flatDict, result, 'mode_')
			result['groupList'] = []
			first = False

		thisGroupCode = flatDict.get('group_code', '')
		if thisGroupCode != lastGroupCode:
			lastGroupCode = thisGroupCode
			curGroupDict = {}
			dictUtils.copyKeysWithPrefix(flatDict, curGroupDict, 'group_')
			curGroupDict['subcatList'] = []
			curGroupDict['subcatCodeList'] = []
			result['groupList'].append(curGroupDict)

		subcatDict = {}
		dictUtils.copyKeysWithPrefix(flatDict, subcatDict, 'subcat_')
		curGroupDict['subcatList'].append(subcatDict)
		curGroupDict['subcatCodeList'].append(subcatDict['subcat_code'])

	return result

def getParentCategories(_dbConnection):
	return metaSQL.getParentCategories(_dbConnection)

def getFieldsForCategory(_dbConnection, _categoryCode, _orderFor='LIST'):
	return metaSQL.getFieldsForCategory(_dbConnection, _categoryCode, _orderFor)

def getAllFields(_dbConnection):
	return metaSQL.getAllFields(_dbConnection)

def getFieldsByGroupForCategory(_dbConnection, _categoryCode, _orderFor='DETAIL'):
	result = []
	first = True
	lastGroupCode = None
	curGroupDict = None
	selectorCache = metaSQL.getSelectorCache(_dbConnection)

	flatList = metaSQL.getFieldsForCategory(_dbConnection, _categoryCode, _orderFor)
	for flatDict in flatList:
		thisGroupCode = flatDict.get('group_code', '')
		if thisGroupCode != lastGroupCode:
			lastGroupCode = thisGroupCode
			curGroupDict = {}
			dictUtils.copyKeysWithPrefix(flatDict, curGroupDict, 'group_')
			curGroupDict['fieldList'] = []
			result.append(curGroupDict)

		fieldDict = {}
		dictUtils.copyKeysWithPrefix(flatDict, fieldDict, 'field_')
		dictUtils.copyKeysWithPrefix(flatDict, fieldDict, 'affordance_')
		if fieldDict.get('affordance_code','') == 'Repeating_Text_Selector' and fieldDict.get('field_static_lookup_code',''):
			fieldDict['data-widget-enums'] = selectorCache.get(fieldDict.get('field_static_lookup_code',[]))
		curGroupDict['fieldList'].append(fieldDict)

	return result

def getStaticLookupData(_dbConnection,static_lookup_code):
	return metaSQL.getStaticLookupData(_dbConnection,static_lookup_code)
