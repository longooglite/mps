# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.dashboardSQL as dboardSQL
import MPSAppt.services.jobActionResolverService as jResolverSVC
import MPSAppt.services.jobActionService as jobactionService
import json

class DashboardService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def processDashboardEvents(self, _jobActionDict, _jobTaskDict, _container, _dashboardConfigKeyName, _now, _username, doCommit=True):
		configList = _container.getConfigDict().get(_dashboardConfigKeyName, [])
		for eventDict in configList:
			eventType = eventDict.get('eventType','')
			if eventType== 'create':
				self.createDashboardEvent(eventDict,  _jobActionDict, _now, _username, _container, doCommit)
			elif eventType == 'remove':
				self.removeDashboardEvent(eventDict,  _jobActionDict, _now, _username, _container, doCommit)
			elif eventType == 'removeAll':
				self.removeAllDashboardEvents(eventDict,  _jobActionDict, _now, _username, _container, doCommit)

	def createDashboardEvent(self, _eventDict, _jobActionDict, _now, _username, _container, doCommit=True):
		departmentOverride = _eventDict.get('department',None)
		department = _container.getDepartment(departmentOverride)
		if department:
			code = _eventDict.get('code','')
			if code:
				jobActionId = _jobActionDict.get('id', 0)
				doCreate = True
				precondition = _eventDict.get('component_precondition','')
				if precondition:
					preconditionContainer = _container.workflow.getContainer(precondition)
					if not preconditionContainer or not preconditionContainer.containerDict.get('enabled',False):
						doCreate = False
				if doCreate:
					if not dboardSQL.dashboardExists(self.connection, code, jobActionId):
						sortOrder = _eventDict.get('sortOrder','')
						permissionsList = json.dumps(_eventDict.get('permission',[]))
						description = _eventDict.get('eventDescription','')
						dboardSQL.createDashboard(self.connection, jobActionId, department.get('id',-1), code, description, permissionsList, sortOrder, _now, _username, doCommit)

	def removeDashboardEvent(self, _eventDict, _jobActionDict, _now, _username, _container, doCommit=True):
		codes = _eventDict.get('code','')
		if type(codes) <> list:
			codes = [codes]
		for code in codes:
			jobActionId = _jobActionDict.get('id', 0)
			dboardSQL.removeDashoardEvent(self.connection, code, jobActionId, doCommit)

	def manualRemoveDashboardEvent(self, code, jobActionId):
		dboardSQL.removeDashoardEvent(self.connection, code, jobActionId)

	def removeAllDashboardEvents(self, _eventDict, _jobActionDict, _now, _username, container, doCommit=True):
		jobActionId = _jobActionDict.get('id', 0)
		dboardSQL.removeAllDashoardEvents(self.connection, jobActionId, doCommit)

	def populateDashboard(self, _sitePreferences, _userPermissions, _userdepartmentList):
		dashBoardList = []
		currentEvent = {}
		jaSVC = jobactionService.JobActionService(self.connection)
		accesibleJobActionOverrides,inaccesibleJobActionOverrides = [],[]
		if not self.userHasPermisson(['facultyAffairsUser'],_userPermissions):
			alljobActionDepartmentOverrides = jaSVC.getAllOverridesForDepartmentList(_userdepartmentList)
			accesibleJobActionOverrides = self.__getApplicableDepartmentOverrides(alljobActionDepartmentOverrides)
			#inaccesibleJobActionOverrides = self.__getApplicableDepartmentOverrides(alljobActionDepartmentOverrides,False)

		resolver = jResolverSVC.JobActionResolverService(self.connection, _sitePreferences)
		rawDashboardItems = dboardSQL.getActiveDashboardItemsRestrictedByDepartment(self.connection,self.getDeptIdList(_userdepartmentList))
		for item in rawDashboardItems:
			if item.get('dash_active',False):
				dashBoardDict = self.extractObject(item, dboardSQL.kDashTableColumns, dboardSQL.kDashPrefix)
				jobActionDict = self.extractObject(item, dboardSQL.kJobActionTableColumns, dboardSQL.kJobActionPrefix)
				jobActionId = jobActionDict.get('id',-1)
				appointmentDict = self.extractObject(item, dboardSQL.kAppointmentTableColumns, dboardSQL.kAppointmentPrefix)
				positionDict = self.extractObject(item, dboardSQL.kPositionTableColumns, dboardSQL.kPositionPrefix)
				personDict = {}
				if jobActionDict.get('person_id', None):
					personDict = self.extractObject(item, dboardSQL.kPersonTableColumns, dboardSQL.kPersonPrefix)

				perms = json.loads(dashBoardDict.get('view_permission',[]))
				if self.userHasPermisson(perms, _userPermissions) and jobActionId not in inaccesibleJobActionOverrides:
					if currentEvent.get('code','---') <> dashBoardDict.get('code',''):
						currentEvent = {}
						currentEvent['code'] = dashBoardDict.get('code','')
						currentEvent['description'] = dashBoardDict.get('description','')
						currentEvent['items'] = []
						dashBoardList.append(currentEvent)

					resolvedJobAction = resolver.resolve(jobActionDict, _optionalAppointmentDict=appointmentDict, _optionalPositionDict=positionDict, _optionalPersonDict=personDict)
					resolvedJobAction['url'] = '/appt/jobaction/%i' % (jobActionDict.get('id',0))
					resolvedJobAction['created'] = resolver.convertTimestampToDisplayFormat(dashBoardDict.get('created',''))
					resolvedJobAction.get('department',{})['descr'] = resolvedJobAction.get('department',{}).get('full_descr','')
					currentEvent.get('items',[]).append(resolvedJobAction)

		return dashBoardList

	def __getApplicableDepartmentOverrides(self,alljobActionDepartmentOverrides,visibility = True):
		overrides = []
		if alljobActionDepartmentOverrides:
			for override in alljobActionDepartmentOverrides:
				if override.get('access_allowed',False) == visibility:
					overrides.append(override.get('job_action_id',-1))
		return overrides

	def extractObject(self, _rawItem, _columnNameList, _prefix):
		result = {}
		for columnName in _columnNameList:
			result[columnName] = _rawItem.get(_prefix + columnName, None)
		return result

	def userHasPermisson(self,perms,userPermissions):
		for perm in perms:
			for userPerm in userPermissions:
				if perm == userPerm.get('code',''):
					return True
		return False

	def getDeptIdList(self,departmentlist):
		idList = []
		for dept in departmentlist:
			idList.append(dept.get('id',0))
		return idList

	def removeEventsForJobActionId(self,_jobActionId,doCommit = True):
		dboardSQL.removeAllDashoardEvents(self.connection,_jobActionId,doCommit)