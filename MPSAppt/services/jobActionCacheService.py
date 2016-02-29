# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import operator

class JobActionCacheService():
	def __init__(self, _departmentList):

		#   Display Lists, which only reflect data values found in a generated Roster or Dashboard.
		#   These are built by the buildRosterDisplayLists(roster) and buildDashboardDisplayLists(dashboard) methods.

		self._initDisplayCaches()


		#   allowedDepts
		#   Dictionary of Department Codes to which the user has been given access.
		#       key = department code
		#       value = True

		self._buildAllowedDepartmentsCache(_departmentList)

	def _initDisplayCaches(self):
		self.displayDepartmentCache = {}
		self.displayTrackCache = {}
		self.displayTitleCache = {}
		self.displayJobActionTypeCache = {}
		self.displayJobActionStatusCache = {}
		self.displayPositionStatusCache = {}
		self.displayPrimalityCache = {}
		self.displayWorkflowCache = {}
		self.displayEventCache = {}

		self.displayDepartmentList = []
		self.displayTrackList = []
		self.displayTitleList = []
		self.displayJobActionTypeList = []
		self.displayJobActionStatusList = []
		self.displayPositionStatusList = []
		self.displayPrimalityList = []
		self.displayWorkflowList = []
		self.displayEventList = []

	def _buildAllowedDepartmentsCache(self, _departmentList):
		deptList = {}
		for deptDict in _departmentList:
			deptList[deptDict.get('code','')] = True
		self.allowedDepts = deptList


	#   Make display Lists (not caches) available to the outside world.

	def getDepartmentList(self): return self.displayDepartmentList
	def getTrackList(self): return self.displayTrackList
	def getTitleList(self): return self.displayTitleList
	def getJobActionTypeList(self): return self.displayJobActionTypeList
	def getJobActionStatusList(self): return self.displayJobActionStatusList
	def getPositionStatusList(self): return self.displayPositionStatusList
	def getPrimalityList(self): return self.displayPrimalityList
	def getWorkflowList(self): return self.displayWorkflowList
	def getEventList(self): return self.displayEventList


	#   Building Lists of data values actually present in Roster or Dashboard data.

	def buildRosterDisplayLists(self, _roster):
		self._initDisplayCaches()

		for pcnDict in _roster:
			self.cacheDepartment(pcnDict)
			self.cachePrimality(pcnDict)
			for appointmentDict in pcnDict.get('appointment_list', []):
				self.cacheDepartment(appointmentDict)
				self.cachePrimality(appointmentDict)
				self.cacheTitle(appointmentDict)
				self.cacheTrack(appointmentDict)
				self.cachePositionStatus(appointmentDict)
				for jobActionDict in appointmentDict.get('job_action_list', []):
					self.cacheDepartment(jobActionDict)
					self.cachePrimality(jobActionDict)
					self.cacheJobActionType(jobActionDict)
					self.cacheJobActionStatus(jobActionDict)
					self.cachePositionStatus(jobActionDict)
					self.cacheTitle(jobActionDict)
					self.cacheTrack(jobActionDict)

		self._buildLists()

	def buildDashboardDisplayLists(self, _dashboard):
		self._initDisplayCaches()

		for typeDict in _dashboard:
			self.cacheEvent(typeDict)
			for itemDict in typeDict.get('items', []):
				self.cacheDepartment(itemDict.get('department', {}), _codeKey='code', _descrKey='full_descr')
				self.cacheTitle(itemDict.get('title', {}), _codeKey='code', _descrKey='descr')
				self.cacheTrack(itemDict.get('track', {}), _codeKey='code', _descrKey='descr')
				self.cachePrimality(itemDict.get('position', {}))
				self.cacheJobActionType(itemDict.get('job_action_type', {}), _codeKey='code', _descrKey='descr')
				self.cacheJobActionStatus(itemDict.get('job_action', {}), _codeKey='current_status')
				self.cacheWorkflow(itemDict.get('workflow', {}), _codeKey='code', _descrKey='descr')

		self._buildLists()

	def _buildLists(self):
		self.displayDepartmentList = sorted(self.displayDepartmentCache.values(), key=operator.itemgetter('department_descr'))
		self.displayTitleList = sorted(self.displayTitleCache.values(), key=operator.itemgetter('title_descr'))
		self.displayTrackList = sorted(self.displayTrackCache.values(), key=operator.itemgetter('track_descr'))
		self.displayPrimalityList = sorted(self.displayPrimalityCache.values(), key=operator.itemgetter('primality'))
		self.displayJobActionTypeList = sorted(self.displayJobActionTypeCache.values(), key=operator.itemgetter('job_action_type_descr'))
		self.displayJobActionStatusList = sorted(self.displayJobActionStatusCache.values(), key=operator.itemgetter('job_action_status'))
		self.displayPositionStatusList = sorted(self.displayPositionStatusCache.values(), key=operator.itemgetter('status_descr'))
		self.displayWorkflowList = sorted(self.displayWorkflowCache.values(), key=operator.itemgetter('workflow_descr'))
		self.displayEventList = sorted(self.displayEventCache.values(), key=operator.itemgetter('event_descr'))


	#   Cachin'.

	def cacheDepartment(self, _dict, _codeKey='department_code', _descrKey='department_descr'):
		departmentCode = _dict.get(_codeKey, None)
		if departmentCode and \
			departmentCode in self.allowedDepts and \
			departmentCode not in self.displayDepartmentCache:
			self.displayDepartmentCache[departmentCode] = { 'department_code':departmentCode, 'department_descr' : _dict.get(_descrKey, '') }

	def cacheTitle(self, _dict, _codeKey='title_code', _descrKey='title_descr'):
		titleCode = _dict.get(_codeKey, None)
		if titleCode and titleCode not in self.displayTitleCache:
			self.displayTitleCache[titleCode] = { 'title_code':titleCode, 'title_descr' : _dict.get(_descrKey, '') }

	def cacheTrack(self, _dict, _codeKey='track_code', _descrKey='track_descr'):
		trackCode = _dict.get(_codeKey, None)
		if trackCode and trackCode not in self.displayTrackCache:
			self.displayTrackCache[trackCode] = { 'track_code':trackCode, 'track_descr' : _dict.get(_descrKey, '') }

	def cachePrimality(self, _dict, _codeKey='is_primary'):
		primary = _dict.get(_codeKey, True)
		key = 'primary' if primary else 'secondary'
		if key not in self.displayPrimalityCache:
			self.displayPrimalityCache[key] = { 'primality': key, 'descr': 'Primary' if primary else 'Secondary' }

	def cacheJobActionType(self, _dict, _codeKey='job_action_type_code', _descrKey='job_action_type_descr'):
		jobActionTypeCode = _dict.get(_codeKey, None)
		if jobActionTypeCode and jobActionTypeCode not in self.displayJobActionTypeCache:
			self.displayJobActionTypeCache[jobActionTypeCode] = { 'job_action_type_code':jobActionTypeCode, 'job_action_type_descr' : _dict.get(_descrKey, '') }

	def cacheJobActionStatus(self, _dict, _codeKey='job_action_status'):
		status = _dict.get(_codeKey, None)
		if status and status not in self.displayJobActionStatusCache:
			self.displayJobActionStatusCache[status] = { 'job_action_status': status }

	def cachePositionStatus(self, _dict, _codeKey='status_code', _descrKey='status_descr'):
		status = _dict.get(_codeKey, None)
		if status and status not in self.displayPositionStatusCache:
			self.displayPositionStatusCache[status] = { 'status_code': status, 'status_descr' : _dict.get(_descrKey, '') }

	def cacheWorkflow(self, _dict, _codeKey='workflow_code', _descrKey='workflow_descr'):
		workflow = _dict.get(_codeKey, None)
		if workflow and workflow not in self.displayWorkflowCache:
			self.displayWorkflowCache[workflow] = { 'workflow_code': workflow, 'workflow_descr' : _dict.get(_descrKey, '') }

	def cacheEvent(self, _dict, _codeKey='code', _descrKey='description'):
		event = _dict.get(_codeKey, None)
		if event and event not in self.displayEventCache:
			self.displayEventCache[event] = { 'event_code': event, 'event_descr' : _dict.get(_descrKey, '') }
