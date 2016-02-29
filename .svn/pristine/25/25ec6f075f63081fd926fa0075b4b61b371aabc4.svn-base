# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.services.abstractResolverService import AbstractResolverService
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.core.sql.lookupTableSQL as lookupSQL
import MPSAppt.services.departmentService as deptSvc

class DepartmentResolverService(AbstractResolverService):
	def __init__(self, _connection, _sitePreferences):
		AbstractResolverService.__init__(self, _connection, _sitePreferences)
		self._initCaches()

	def _initCaches(self):
		self.pcnCache = {}
		self.departmentCache = {}
		self.cachesLoaded = False

	def _loadCaches(self):
		if self.cachesLoaded:
			return

		self.cachesLoaded = True
		self.pcnCache = lookupSvc.getLookupTable(self.connection, 'wf_pcn')
		self._loadDepartmentCache()

	def _loadDepartmentCache(self):
		self.departmentCache = deptSvc.DepartmentService(self.connection).getAllDepartmentsAsLookupTable()

		#   Setup parent hierarchy.

		for departmentId in self.departmentCache.keys():
			departmentDict = self.departmentCache[departmentId]
			departmentDict['parent'] = {}
			parentId = departmentDict.get('parent_id',0)
			if parentId:
				parentDict = self.departmentCache.get(parentId,{})
				if parentDict:
					departmentDict['parent'] = parentDict

		#   Sundry stuff.

		for departmentId in self.departmentCache.keys():
			departmentDict = self.departmentCache[departmentId]
			departmentDict['pcn'] = self.pcnCache.get(departmentDict.get('pcn_id', -1), {})
			departmentDict['full_address_lines'] = self._resolveDepartmentAddress(departmentDict)
			departmentDict['full_descr'] = self._resolveFullDepartmentDescr(departmentDict)
			departmentDict['department_chair'] = []
			departmentDict['users'] = []

		#   Department Chairs.

		chairList = lookupSQL.getLookupTable(self.connection, 'wf_department_chair', _orderBy='department_id ASC, seq ASC')
		for chairDict in chairList:
			chairDict['chair_titles_list'] = chairDict.get('chair_titles','').split('|')
			departmentId = chairDict.get('department_id', 0)
			if departmentId:
				departmentDict = self.departmentCache[departmentId]
				departmentDict['department_chair'].append(chairDict)

		#   Users.

		userList = lookupSQL.getLookupTable(self.connection, 'wf_username_department', _orderBy='department_id ASC, username ASC')
		for joinDict in userList:
			departmentId = joinDict.get('department_id', 0)
			if departmentId:
				departmentDict = self.departmentCache[departmentId]
				departmentDict['users'].append(joinDict.get('username', ''))


	def _resolveDepartmentAddress(self, _departmentDict):
		lines = []
		addressLinesJson = _departmentDict.get('address_lines','[]')
		try:
			addressLines = json.loads(addressLinesJson)
			if addressLines:
				lines.extend(addressLines)
		except Exception, e:
			pass

		cityStatePostal = stringUtils.constructCityStatePostal(_departmentDict.get('city',''), _departmentDict.get('state',''), _departmentDict.get('postal',''))
		if cityStatePostal:
			lines.append(cityStatePostal)
		suffix = _departmentDict.get('suffix','')
		if suffix:
			lines.append(suffix)

		return lines

	def _resolveFullDepartmentDescr(self, _departmentDict):
		descr = _departmentDict.get('descr','')
		parent = _departmentDict.get('parent',{})
		parentDescr = parent.get('descr','')
		if parentDescr and parent.get('parent_id',0):
			return " - ".join([parentDescr, descr])
		return descr


	#   Meat.

	def resolve(self, _departmentId):
		if _departmentId:
			self._loadCaches()
			return self.departmentCache.get(_departmentId, {})
		return {}
