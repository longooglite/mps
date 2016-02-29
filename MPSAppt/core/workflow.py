# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.core.containers.baseContainer import buildContainer
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.core.sql.workflowSQL as wfSQL
import MPSAppt.services.jobActionService as jaSvc
import MPSAppt.services.fileRepoService as frSvc
import MPSAppt.services.activityService as activitySvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.core.constants as const
import MPSAppt.services.fieldLevelRevisionsService as FLRRService
import MPSCore.utilities.stringUtilities as stringUtils

kCompleteText = 'Complete'
kRevisionRequiredText = 'Revisions Required'

class Workflow:
	def __init__(self, _dbConnection, _jobActionDict={}, _department = {}):
		self.connection =_dbConnection
		self.mainContainer = None
		self.userProfile = {}
		self.userPermissions = {}
		self.jobActionDict = _jobActionDict
		self.department = _department
		self.workflowContainerCode = ''
		self.workflowCache = {}
		self.jobTaskCache = None
		self.fileRepoCache = None
		self.fieldLevelRevisionsCache = None
		self.activityLogCache = None
		self.activityLogByTaskCodeCache = None
		self.permissionOverrideWhiteListCache = None
		self.permissionOverrideBlackListCache = None

	def getConnection(self): return self.connection
	def getMainContainer(self): return self.mainContainer
	def getUserProfile(self): return self.userProfile
	def getUserPermissions(self): return self.userPermissions
	def getJobActionDict(self): return self.jobActionDict
	def getWorkflowCache(self): return self.workflowCache


	#   Permission Override Caches
	def getPermissionOverrideWhiteListCache(self):
		if self.permissionOverrideWhiteListCache is None:
			community = self.getUserProfile().get('userProfile',{}).get('community','')
			username = self.getUserProfile().get('userProfile',{}).get('username','')
			departmentList = deptSvc.DepartmentService(self.getConnection()).getDepartmentsForUser(community, username)
			self.permissionOverrideWhiteListCache = jaSvc.JobActionService(self.getConnection()).getPermissionOverrideCache(self.getJobActionDict().get('id',0),True,departmentList)
		return self.permissionOverrideWhiteListCache

	def getPermissionOverrideBlackListCache(self):
		if self.permissionOverrideBlackListCache is None:
			community = self.getUserProfile().get('userProfile',{}).get('community','')
			username = self.getUserProfile().get('userProfile',{}).get('username','')
			departmentList = deptSvc.DepartmentService(self.getConnection()).getDepartmentsForUser(community, username)
			self.permissionOverrideBlackListCache = jaSvc.JobActionService(self.getConnection()).getPermissionOverrideCache(self.getJobActionDict().get('id',0),False,departmentList)
		return self.permissionOverrideBlackListCache

	#   Job Task Cache.

	def getJobTaskCache(self):
		if self.jobTaskCache is None:
			self.jobTaskCache = jaSvc.JobActionService(self.getConnection()).getJobTaskCache(self.getJobActionDict().get('id',0))
		return self.jobTaskCache

	def clearJobTaskCache(self):
		self.jobTaskCache = None

	#   File Repo Cache.

	def getFileRepoCache(self):
		if self.fileRepoCache is None:
			self.fileRepoCache = frSvc.FileRepoService(self.getConnection()).getFileRepoCache(self.getJobActionDict().get('id',0))
		return self.fileRepoCache

	#   Field Level Revisions Cache.

	def getFieldLevelRevisionsCache(self):
		if self.fieldLevelRevisionsCache is None:
			self.fieldLevelRevisionsCache = FLRRService.FieldLevelRevisions(self.getConnection()).getFieldLevelRevisionsCache(self.getJobActionDict())
		return self.fieldLevelRevisionsCache

	#   Activity Log Caches.

	def getActivityLogCache(self):
		if self.activityLogCache is None:
			actService = activitySvc.ActivityService(self.getConnection())
			self.activityLogCache = actService.getActivityLogCache(self.getJobActionDict().get('id',0))
			self.activityLogByTaskCodeCache = actService.getActivityLogByTaskCodeCache(self.activityLogCache)
		return self.activityLogCache

	def getActivityLogByTaskCodeCache(self):
		self.getActivityLogCache()
		return self.activityLogByTaskCodeCache

	def getActivityLogForTaskCode(self, _taskCode):
		return self.getActivityLogByTaskCodeCache().get(_taskCode, [])


	#   Construct a Workflow.

	def buildWorkflow(self, _containerCode, _parameterBlock, _overrideWorkflowCache=None):

		#   Parameter block contains:
		#
		#   userProfile - current user's profile
		#   userPermissions - current user's permission set
		#   titleCode - proposed title used for Title overrides. Optional.

		self.workflowContainerCode = _containerCode

		#   If an override Workflow Container Cache was provided (meaning this is a Completed Workflow),
		#   use it. Other, build it and apply title overrides using the database container definitions.

		if _overrideWorkflowCache:
			overrideCache = {}
			self.workflowCache = _overrideWorkflowCache
		else:
			overrideCache = self.buildOverrideCache(_containerCode, _parameterBlock.get('titleCode',''))
			self.workflowCache = self.buildWorkflowCache(overrideCache)


		#   Extend the Parameter block with the following:
		#
		#   overrideCache - dictionary of component overrides for the given Title, if any.
		#       key: component code
		#       value: dictionary of key/value overrides
		#   workflowCache - dictionary of all components involved in the workflow, with title overrides applied
		#       key: component code
		#       value: dictionary of raw component configuration info
		#   componentInstanceCache - actual class instances of the components as they are built.
		#       Initially empty, and constructed as the components are loaded.
		#       Specific uses include: blockers, ...
		#       key: component code
		#       value: component instance
		#   workflow - this object instance. Every component instance in the constructed workflow retains a
		#       reference to this Workflow object. Used to access the database connection, and possibly other stuff.

		componentInstanceCache = {}
		_parameterBlock.update({
			"workflowCache": self.getWorkflowCache(),
			"componentInstanceCache": componentInstanceCache,
			"overrideCache": overrideCache,
			"workflow": self})

		self.userProfile = _parameterBlock.get('userProfile', {})
		self.userPermissions = _parameterBlock.get('userPermissions', {})

		main = buildContainer(_containerCode, _parameterBlock)
		self.mainContainer = main
		self.injectItems()

	def injectItems(self):
		injectors = self.getMainContainer().workflow.getContainersForClassName(const.kContainerClassItemInjector)
		if injectors:
			for injector in injectors:
				injector.loadInstance()
				taskcodesStr = injector.injectedItemDict.get('task_codes','')
				if taskcodesStr:
					taskCodeDict = json.loads(injector.injectedItemDict.get('task_codes',''))
					numSets = len(injector.containerDict.get('config',{}).get('items',{}))
					i = 1
					while i <= numSets:
						key = 'set%i' % (i)
						i+=1
						thisSet = taskCodeDict.get(key,[])
						if thisSet:
							for taskCode in thisSet:
								container = self.getMainContainer().workflow.getContainer(taskCode)
								if container:
									container.containerDict['enabled'] = True
									container.containerDict['optional'] = False

	def buildOverrideCache(self, _workflowCode, _titleCode):
		returnDict = {}
		if _titleCode:
			overrides = wfSQL.getTitleOverrides(self.getConnection(), _workflowCode, _titleCode)
			for each in overrides:
				returnDict[each.get('component_code','')] = json.loads((each.get('value','{}')))
		return returnDict

	def buildWorkflowCache(self, _overrideCache):
		returnDict = {}
		components = wfSQL.getComponents(self.getConnection())
		for each in components:
			componentCode = each.get('code',None)
			componentDict = json.loads((each.get('value','{}')))
			if componentCode not in returnDict:
				returnDict[componentCode] = componentDict
			else:
				self.applyOverrides(returnDict.get(componentCode,{}), componentDict)
			if componentCode in _overrideCache:
				self.applyOverrides(returnDict.get(componentCode,{}), _overrideCache.get(componentCode,{}))

		return returnDict

	def applyOverrides(self, _origDict, _updateDict):
		#   'config' is a dictionary requiring special handling.
		configDict = _origDict.get('config',{}).copy()
		configDict.update(_updateDict.get('config',{}))
		_origDict.update(_updateDict)
		_origDict['config'] = configDict

	#   UI-related.

	def coreJADict(self):
		return {"common":{"code":"","title":""},
				"config":{},
				"data":{}}

	def flattenWorkflowUI(self):
		containerList = []

		for container in self.getMainContainer().getContainers():
			containers = container.getAffordanceContainers()
			containerList.extend(containers)
		return containerList

	def getNumeratorAndDenominator(self):
		numerator,denominator = 0,0
		flattenedWorkflow = self.flattenWorkflowUI()
		wfStatus = self.computeStatus()
		for workflowEntry in flattenedWorkflow:
			if workflowEntry.containerDict.get('affordanceType','').upper() == const.kAffordanceTypeItem:
				if workflowEntry.getIsEnabled() and not workflowEntry.getIsOptional():
					if workflowEntry.hasViewPermission() or wfStatus == 'Complete':
						if workflowEntry.isComplete():
							numerator += 1
						denominator += 1
		if numerator == 0 and denominator == 0:
			denominator = 1
		return numerator,denominator

	def getJobActionUI(self, _sitePreferences):
		# common - keys that are common to all containers, such as class of item, permissions
		# #config - configuration data for container/class
		# #data - data elements for display/persistence

		self.cascadeBlockers(self.getMainContainer())

		jaDict = self.coreJADict()
		jaDict['activity_log'] = self.getJobActionActivityLog(_sitePreferences)
		jaDict['container'] = []
		tabDict = None
		sectionDict = None

		flattenendList = self.flattenWorkflowUI()
		for container in flattenendList:
			if container.hasViewPermission():
				if container.getAffordanceType() == const.kAffordanceTypeTab:
					tabDict = self.coreJADict()
					tabDict['sections'] = []
					self.getUIData(container, tabDict, _sitePreferences)
					jaDict['container'].append(tabDict)

				elif container.getAffordanceType() == const.kAffordanceTypeSection:
					sectionDict = self.coreJADict()
					sectionDict['items'] = []
					self.getUIData(container, sectionDict, _sitePreferences)
					tabDict['sections'].append(sectionDict)

				elif container.getAffordanceType() == const.kAffordanceTypeItem:
					itemDict = self.coreJADict()
					self.getUIData(container, itemDict, _sitePreferences)
					sectionDict['items'].append(itemDict)

		self.removeEmptySections(jaDict)
		self.removeEmptyTabs(jaDict)
		return jaDict

	def getJobActionActivityLog(self, _sitePreferences, _optionalSingleTaskCodeOrListOfTaskCodes=None):
		timezone = _sitePreferences.get('timezone', 'US/Eastern')
		format = _sitePreferences.get('ymdhmformat', '%m/%d/%Y %H:%M')

		filterList = []
		iterationList = self.getActivityLogCache()
		if _optionalSingleTaskCodeOrListOfTaskCodes:
			if type(_optionalSingleTaskCodeOrListOfTaskCodes) == type([]):
				filterList = _optionalSingleTaskCodeOrListOfTaskCodes
			else:
				iterationList = self.getActivityLogForTaskCode(_optionalSingleTaskCodeOrListOfTaskCodes)

		logList = []
		for srcDict in iterationList:
			taskCode = srcDict.get('task_code','')
			if (not filterList) or (taskCode in filterList):
				logDict = {}
				logDict['task_code'] = srcDict.get('task_code','')
				logDict['activity'] = srcDict.get('activity','')
				logDict['created'] = self.localizeDate(srcDict.get('created',''), timezone, format)
				logDict['username'] = srcDict.get('username','')
				logDict['display_text'] = '''%s by %s at %s''' % (logDict['activity'], logDict['username'], logDict['created'])
				logDict['comments'] = []
				logList.append(logDict)

				srcCommentsList = srcDict.get('comments',[])
				if srcCommentsList:
					container = self.getContainer(logDict['task_code'])
					if container:
						for srcCommentDict in srcCommentsList:
							thisCommentCode = srcCommentDict.get('comment_code','')
							thisCommentConfigDict = container.getCommentConfigForCommentCode(thisCommentCode)
							if (thisCommentConfigDict) and (container.hasAnyPermission(thisCommentConfigDict.get('viewPermissions',[]))):
								logDict['comments'].append(srcCommentDict)
		return logList

	def localizeDate(self, _utcDate, _timezone, _format):
		localDate = dateUtils.localizeUTCDate(_utcDate, _timezone)
		return dateUtils.parseDate(localDate, _format)

	def getUIData(self, _container, _dictionary, _sitePreferences):
		self.populateCommons(_dictionary, _container, _sitePreferences)
		_dictionary['config'] = _container.getConfigDict()
		_dictionary['data'] = _container.getDataDict(_sitePreferences)

		viewDetails = True
		if _dictionary['common']['is_blocked']:
			viewDetails = False
		else:
			if (_container.getOverviewOnly()) and \
				(_container.hasViewPermission()) and \
				(not _container.hasEditPermission()):
				viewDetails = False
		if viewDetails:
			# If an item is marked as a protected candidate item,
			# and, we're in candidate view mode
			# all users will see the overview only view. Properly permissioned roles can view CBC auth, e.g., logged on as themselves
			if _container.containerDict.get('isProtectedCandidateItem',False):
				if _container.isComplete():
					if stringUtils.interpretAsTrueFalse(self.getUserProfile().get('sessionProfile',{}).get('isCandidateView','false')):
						viewDetails = False
		_dictionary['common']['view_details'] = viewDetails

	def populateCommons(self, _aDict, _container, _sitePreferences):
		_aDict['common']['code'] = _container.getCode()
		_aDict['common']['descr'] = _container.getDescr()
		_aDict['common']['header'] = _container.getHeader()
		_aDict['common']['class_name'] = _container.getClassName()
		_aDict['common']['optional'] = _container.getIsOptional()
		_aDict['common']['is_blocked'] = _container.getIsBlocked()
		_aDict['common']['is_complete'] = _container.isComplete()
		_aDict['common']['revisions_required'] = _container.getRevisionsRequired()
		_aDict['common']['field_revisions_required'] = _container.getFieldLevelRevisionsRequired()

	def cascadeBlockers(self, _container, _stopContainer=None):
		self.cascadeEnabled(_container)
		for container in _container.getContainers():
			if container.determineIfBlocked():
				container.setIsBlocked(True)
				flatList = container.getDeepContainers()
				for each in flatList:
					each.setIsBlocked(True)
					if _stopContainer and _stopContainer == each:
						return
			else:
				if _stopContainer and _stopContainer == container:
					return
				self.cascadeBlockers(container)

	def cascadeEnabled(self, _container):
		for container in _container.getContainers():
			if not container.getIsEnabled():
				flatList = container.getDeepContainers()
				for each in flatList:
					each.setIsEnabled(False)
			else:
				self.cascadeEnabled(container)

	def isContainerBlocked(self, _stopContainer):
		self.cascadeBlockers(self.getMainContainer(), _stopContainer)
		return _stopContainer.getIsBlocked()

	def removeEmptySections(self, _jaDict):
		for tabDict in _jaDict['container']:
			newSectionList = []
			for sectionDict in tabDict['sections']:
				if sectionDict['items']:
					newSectionList.append(sectionDict)
			tabDict['sections'] = newSectionList

	def removeEmptyTabs(self, _jaDict):
		newTabList = []
		for tabDict in _jaDict['container']:
			if tabDict['sections']:
				newTabList.append(tabDict)
		_jaDict['container'] = newTabList


	#   Workflow Admin Tool-related.

	def getWFAdminUI(self, _wfId, _titleId, _editMode, _viewMode):

		#   Variation of getJobActionUI that is used in the Workflow Admin tools.
		#   - no Activity Log
		#   - no blockers are computed
		#   - no complete is computed
		#   - no revisions required are computed
		#   - container view permissions are ignored

		jaDict = self.coreJADict()
		jaDict['activity_log'] = []
		jaDict['container'] = []
		tabDict = None
		sectionDict = None

		flattenendList = self.flattenWorkflowUI()
		for container in flattenendList:
			if container.getAffordanceType() == const.kAffordanceTypeTab:
				tabDict = self.coreJADict()
				tabDict['sections'] = []
				self.getWFAdminUIData(container, tabDict, _wfId, _titleId, _editMode, _viewMode)
				jaDict['container'].append(tabDict)

			elif container.getAffordanceType() == const.kAffordanceTypeSection:
				sectionDict = self.coreJADict()
				sectionDict['items'] = []
				self.getWFAdminUIData(container, sectionDict, _wfId, _titleId, _editMode, _viewMode)
				tabDict['sections'].append(sectionDict)

			elif container.getAffordanceType() == const.kAffordanceTypeItem:
				itemDict = self.coreJADict()
				self.getWFAdminUIData(container, itemDict, _wfId, _titleId, _editMode, _viewMode)
				sectionDict['items'].append(itemDict)

		self.removeEmptySections(jaDict)
		self.removeEmptyTabs(jaDict)
		return jaDict

	def getWFAdminUIData(self, _container, _dictionary, _wfId, _titleId, _editMode, _viewMode):
		_dictionary['common']['code'] = _container.getCode()
		_dictionary['common']['descr'] = _container.getDescr()
		_dictionary['common']['header'] = _container.getHeader()
		_dictionary['common']['class_name'] = _container.getClassName()
		_dictionary['common']['optional'] = _container.getIsOptional()
		_dictionary['common']['url'] = "/appt/wf/edit/%s/%s/%s/%s/%s" % (str(_wfId), str(_titleId), _container.getCode(), _editMode, _viewMode)
		_dictionary['config'] = _container.getConfigDict()


	#   Status.

	def computeStatus(self):
		if self.getJobActionDict().get('complete', False):
			return kCompleteText
		if self.getJobActionDict().get('revisions_required', False):
			return kRevisionRequiredText

		lastStatus = self.getMainContainer().getStatusMsg()
		for each in self.getMainContainer().getContainers():
			containerStatusMessage = each.computeStatus()
			if containerStatusMessage:
				lastStatus = containerStatusMessage

			theBuckStopsHere = not each.isCompleteWithConsiderations()
			if theBuckStopsHere:
				return lastStatus

		return lastStatus


	#   Container location and manipulation.

	def getContainer(self, _containerCode):
		if _containerCode:
			for container in self.flattenWorkflow():
				if container.getCode() == _containerCode:
					return container
		return None

	def getContainersForClassName(self, _className):
		containerList = []
		if _className:
			for container in self.flattenWorkflow():
				if container.getClassName() == _className:
					containerList.append(container)
		return containerList

	def flattenWorkflow(self):
		return self.getMainContainer().getDeepContainers()

	def getWorkflowContainerCodeList(self):
		codeList = []
		for container in self.flattenWorkflow():
			thisCode = container.getCode()
			if (thisCode) and (thisCode not in codeList):
				codeList.append(thisCode)
		return codeList

	def getWorkflowJsonForArchiving(self):
		archiveDict = {}
		archiveDict['workflowContainerCode'] = self.workflowContainerCode
		for code in self.getWorkflowContainerCodeList():
			thisDict = self.getWorkflowCache().get(code, None)
			if thisDict:
				archiveDict[code] = thisDict
		return json.dumps(archiveDict)

	def getFreezablePredecessorTasks(self, _stopTaskCode=None):

		#   Returns a list of all Freezable Tasks occurring in the workflow
		#   that precede the (optional) specified Task Code.

		taskList = []
		for thisContainer in self.flattenWorkflow():
			if _stopTaskCode and thisContainer.getCode() == _stopTaskCode:
				return taskList
			if thisContainer.getIsTask() and thisContainer.getIsFreezable():
				taskList.append(thisContainer)
		return taskList
