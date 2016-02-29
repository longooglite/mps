# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import collections

import MPSAppt.core.sql.lookupTableSQL as lookupSQL


def getLookupTable(_connection, _tableName, _key='id', _orderBy='code'):
	result = collections.OrderedDict()
	rowList = lookupSQL.getLookupTable(_connection, _tableName, _orderBy)
	for row in rowList:
		result[row[_key]] = row
	return result

def getStaticLookupTable(_connection, _keyName, _key='id'):
	result = {}
	rowList = lookupSQL.getEntityListByKey(_connection, 'cv_static_lookup', _keyName, 'lookup_key')
	for row in rowList:
		result[row[_key]] = row
	return result

def getStaticLookupDiscreteValue(_connection, _lookupKey, _value, _keyCol='code'):
	result = lookupSQL.getStaticLookupDiscreteValue(_connection, _lookupKey, _value, _keyCol)
	return result

def getEntityByKey(_connection, _tableName, _keyValue, _key='code'):
	return lookupSQL.getEntityByKey(_connection, _tableName, _keyValue, _key)

def getEntityListByKey(_connection, _tableName, _keyValue, _key='code', _orderBy=None):
	return lookupSQL.getEntityListByKey(_connection, _tableName, _keyValue, _key, _orderBy)

def workflowMetatrackExists(_connection, _workflow_id, _metatrack_id):
	return lookupSQL.workflowMetatrackExists(_connection, _workflow_id, _metatrack_id)

def getCodeDescrListByKey(_connection, _tableName, _keyValue, _key, code='code',descr='descr'):
	rawData = lookupSQL.getCodeDescrListByKey(_connection, _tableName, _keyValue, _key, code, descr )
	if _keyValue == 'COUNTRIES':
		index = -1
		for country in rawData:
			index +=1
			if country.get('code','') == 'UnitedStatesofAmerica':
				del rawData[index]
				rawData.insert(0,country)
				break
	return rawData

def getStaticCodeDescrCache(_connection):
	rawData = lookupSQL.getAllStaticLookupData(_connection)
	cache = {}
	for row in rawData:
		lookupKey = row.get('lookup_key', '')
		if lookupKey:
			if lookupKey not in cache:
				cache[lookupKey] = []
			code = row.get('code', '')
			if code:
				cache[lookupKey].append(row)

	countryList = cache.get('COUNTRIES', [])
	if countryList:
		index = -1
		for country in countryList:
			index += 1
			if country.get('code', '') == 'UnitedStatesofAmerica':
				del countryList[index]
				countryList.insert(0, country)
				break

	return cache

def saveStaticItem(_connection, _itemDict, _isAdd, doCommit=True):
	if _isAdd:
		lookupSQL.addStaticItem(_connection, _itemDict, doCommit)
	else:
		lookupSQL.updateStaticItem(_connection, _itemDict, doCommit)

def updateStaticItemSequence(_connection, _itemDict, doCommit=True):
	lookupSQL.updateStaticItemSequence(_connection, _itemDict, doCommit)
