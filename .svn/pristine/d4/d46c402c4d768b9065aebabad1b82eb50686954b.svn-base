# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import collections

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.core.sql.departmentSQL as deptSQL

class DepartmentService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getDepartmentCache(self,byCode=False):
		result = collections.OrderedDict()
		rowList = deptSQL.getAllDepartments(self.connection,False)
		for row in rowList:
			if byCode:
				result[row['code']] = row
			else:
				result[row['id']] = row
		return result

	def getDepartmentCacheWithFullDescr(self):
		parentCache = self.getDepartmentCache()
		departmentCache = self.getDepartmentCache(True)
		for departmentCode in departmentCache:
			department = departmentCache.get(departmentCode)
			self.addFullDescription(department,parentCache)
		return departmentCache

	def getDepartmentChair(self,deptId):
		return deptSQL.getDepartmentChair(self.connection,deptId)

	def getDepartment(self, _id):
		parentCache = self.getDepartmentCache()
		department =  deptSQL.getDepartment(self.connection, _id)
		self.addFullDescription(department,parentCache)
		return department

	def getDepartmentsForUser(self, _community, _username):
		parentCache = self.getDepartmentCache()
		departments = deptSQL.getDepartmentsForUser(self.connection, _community, _username)
		for dept in departments:
			self.addFullDescription(dept,parentCache)
		return departments

	def getDepartmentForJobAction(self,_jobAction):
		parentCache = self.getDepartmentCache()
		dept = deptSQL.getDepartmentForJobAction(self.connection,_jobAction)
		self.addFullDescription(dept,parentCache)
		return dept

	def getPrimaryDepartmentForPerson(self,_personId):
		parentCache = self.getDepartmentCache()
		dept = deptSQL.getPrimaryDepartmentForPerson(self.connection,_personId)
		self.addFullDescription(dept,parentCache)
		return dept

	def getPrimaryDepartmentForPersonByUniqueName(self, _community, _username):
		parentCache = self.getDepartmentCache()
		dept =  deptSQL.getPrimaryDepartmentForPersonByUniqueName(self.connection, _community, _username)
		if dept:
			self.addFullDescription(dept,parentCache)
		return dept

	def getDepartmentsForUserAsLookupTable(self, _community, _username, _key='id'):
		result = {}
		parentCache = self.getDepartmentCache()
		rowList = self.getDepartmentsForUser(_community, _username)
		for row in rowList:
			self.addFullDescription(row,parentCache)
			result[row[_key]] = row
		return result

	def getAllDepartmentsAsLookupTable(self):
		result = collections.OrderedDict()
		parentCache = self.getDepartmentCache()
		rowList = deptSQL.getAllDepartments(self.connection,False)
		for row in rowList:
			self.addFullDescription(row,parentCache)
			result[row['id']] = row
		return result

	def getDepartmentHierarchy(self, userdepartmentList, _includeChairs=False, _excludeInactive=False):
		departments = self.getAllDepartments(_includeChairs)
		departmentDict = self.dictifyDepartments(departments)
		hierarchy = self.buildHierarchy(departments, departmentDict, userdepartmentList, _excludeInactive)
		if (userdepartmentList is None) or (userdepartmentList == ['NoUserRestriction']):
			return hierarchy
		securedHierarchy = []
		for dept in hierarchy:
			if not dept.get('children'):
				if self.isDepartmentInDepartmentList(dept.get('code',''),userdepartmentList):
					securedHierarchy.append(dept)
			else:
				securedHierarchy.append(dept)
		return securedHierarchy

	def buildHierarchy(self, departments, departmentDict, userdepartmentList, _excludeInactive=False):
		hierarchyList = []
		for department in departments:
			if not departmentDict.has_key(department.get('parent_id',-1)):
				if (not _excludeInactive) or (department.get('active',False)):
					parentDict = {"id":department.get("id",-1),"code":department.get('code'),"active":department.get('active',False),"descr":department.get('descr'),"children":[],"chairs":department.get('chairs',[]),"full_descr":department.get('full_descr')}
					hierarchyList.append(parentDict)
		for department in departments:
			if (userdepartmentList is None) or (userdepartmentList == ['NoUserRestriction']):
				departmentNotRestricted = True
			else:
				departmentNotRestricted = self.isDepartmentInDepartmentList(department.get('code',''),userdepartmentList)
			if departmentNotRestricted:
				if departmentDict.has_key(department.get('parent_id',-1)):
					if (not _excludeInactive) or (department.get('active',False)):
						childDict = {"id":department.get("id",-1),"code":department.get('code'),"active":department.get('active',False),"descr":department.get('descr'),"chairs":department.get('chairs',[]),"full_descr":department.get('full_descr')}
						for parent in hierarchyList:
							if parent.get('id',-1) == department.get('parent_id',0):
								parent.get('children',[]).append(childDict)
		return hierarchyList

	def isDepartmentInDepartmentList(self, _deptCode, _departmentList):
		for departmentDict in _departmentList:
			thisDeptCode = departmentDict.get('code', '')
			if thisDeptCode == _deptCode:
				return True
		return False

	def dictifyDepartments(self,_departmentList):
		dictifiedDepartments = {}
		for dept in _departmentList:
			dictifiedDepartments[dept.get('id',0)] = dept
		return dictifiedDepartments

	def getAllDepartments(self, _includeChairs=False, _sortOrder = 'UPPER(descr)'):
		parentCache = self.getDepartmentCache()
		allDepartments = deptSQL.getAllDepartments(self.connection,True,_sortOrder)
		for dept in allDepartments:
			self.addFullDescription(dept,parentCache)
		if _includeChairs:
			deptCache = {}
			for each in allDepartments:
				each['chairs'] = []
				deptCache[each.get('id',0)] = each

			chairList = deptSQL.getDepartmentChairs(self.connection)
			for each in chairList:
				dept = deptCache.get(each.get('department_id', 0), {})
				if dept:
					dept['chairs'].append(each)

		return allDepartments

	def getRootDepartment(self):
		rootDept = deptSQL.getRootDepartment(self.connection)
		rootDept['full_descr'] = rootDept.get('descr','')
		return rootDept

	def replaceDepartmentListForUser(self, _community, _username, _departmentCodeList, doCommit=True):
		try:
			self.deleteAllDepartmentsForUser(_community, _username, doCommit=False)
			for departmentCode in _departmentCodeList:
				self.addDepartmentForUser(_community, _username, departmentCode, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def deleteAllDepartmentsForUser(self, _community, _username, doCommit=True):
		try:
			deptSQL.deleteAllDepartmentsForUser(self.connection, _community, _username, doCommit=False)
			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def addDepartmentForUser(self, _community, _username, _departmentCode, doCommit=True):
		try:
			deptSQL.addDepartmentForUser(self.connection, _community, _username, _departmentCode, doCommit=False)
			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def saveDepartment(self, _departmentDict, _isEdit, doCommit=True):
		try:
			_departmentDict['pcn_id'] = self.getOrCreatePCNForCode(_departmentDict.get('pcn', ''), doCommit=False)
			if _isEdit:
				deptSQL.updateDepartment(self.connection, _departmentDict, doCommit=False)
			else:
				deptSQL.createDepartment(self.connection, _departmentDict, doCommit=False)
				_departmentDict['id'] = self.connection.getLastSequenceNbr('wf_department')

			self.deleteAllChairsForDepartment(_departmentDict, doCommit=False)
			for chairDict in _departmentDict.get('chairs', []):
				chairDict['department_id'] = _departmentDict['id']
				self.createDepartmentChair(chairDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def getOrCreatePCNForCode(self, _pcnCode, doCommit=True):
		pcnDict = lookupTableSvc.getEntityByKey(self.connection, 'wf_pcn', _pcnCode, _key='code')
		if pcnDict:
			return pcnDict.get('id', 0)

		pcnDict = {}
		pcnDict['code'] = _pcnCode
		pcnDict['seq'] = 0
		deptSQL.createPCN(self.connection, pcnDict, doCommit)
		return self.connection.getLastSequenceNbr('wf_pcn')

	def deleteAllChairsForDepartment(self, _departmentDict, doCommit=True):
		try:
			deptSQL.deleteAllChairsForDepartment(self.connection, _departmentDict, doCommit=False)
			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def createDepartmentChair(self, _chairDict, doCommit=True):
		deptSQL.createDepartmentChair(self.connection, _chairDict, doCommit)

	def addFullDescription(self,department,parentCache):
		department['full_descr'] = department.get('descr','')
		if department.get('parent_id',{}):
			parent = parentCache.get(department.get('parent_id',-1))
			if parent and parent.get('parent_id',None):
				department['full_descr'] = "%s - %s" % (parent.get('descr',''),department.get('descr',''))
