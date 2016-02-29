# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os
import logging
import MPSAppt.core.constants as constants
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils

def buildContainer(containerCode, parameterBlock):
	containerDict = {}
	try:
		containerDict = parameterBlock.get("workflowCache",{}).get(containerCode, None)
		if not containerDict:
			if parameterBlock.get('ignoreMissingContainers', False):
				parameterBlock['hasMissingContainers'] = True
				if not 'missingContainers' in parameterBlock:
					parameterBlock['missingContainers'] = []
				parameterBlock['missingContainers'].append(containerCode)

				containerDict = {}
				containerDict['code'] = containerCode
				containerDict['descr'] = 'Missing'
				containerDict['className'] = 'Missing'
				parameterBlock['containerDict'] = containerDict
				from MPSAppt.core.containers.missing import Missing
				missingContainer = Missing(containerCode, parameterBlock)
				return missingContainer

			raise Exception("Container %s not found" % containerCode)

		parameterBlock['containerDict'] = containerDict
		className = containerDict.get('className', 'Container')
		importString = "from MPSAppt.core.containers.%s import %s" % (className.lower(), className)
		exec importString

		container = eval(className + '(containerCode, parameterBlock)')
		parameterBlock.get("componentInstanceCache",{})[containerCode] = container
		return container

	except Exception,e:
		import pprint
		logger = logging.getLogger(__name__)
		if logger.isEnabledFor(logging.DEBUG):
			logger.debug("\r###### WORKFLOW DEBUG ######")
			logger.debug(e.message)
			logger.exception(str(e))
			logger.debug("container code: %s" % (containerCode))
			logger.debug("containerDict: %s" % (pprint.pformat(containerDict)))
			logger.debug("parameterBlock: %s" % (pprint.pformat(parameterBlock)))
			logger.debug("\r###### END WORKFLOW DEBUG ######")


class BaseContainer:

	#   Base class for Containers and Tasks.

	def __init__(self,containerCode, parameterBlock):
		self.setWorkflow(parameterBlock.get('workflow',None))
		self.setCode(containerCode)
		self.setContainerDict(parameterBlock.get('containerDict',{}))
		self.setIsLoaded(False)
		self.setIsBlocked(False)

		myBlockersList = []
		for componentName in self.getContainerDict().get('blockers', []):
			theInstance = parameterBlock.get('componentInstanceCache',{}).get(componentName, None)
			if theInstance and theInstance not in myBlockersList:
				myBlockersList.append(theInstance)
		self.setBlockers(myBlockersList)


	#   Getters/Setters.

	def getWorkflow(self): return self.workflow
	def setWorkflow(self, _workflow): self.workflow = _workflow

	def getCode(self): return self.code
	def setCode(self, _code): self.code = _code

	def getContainerDict(self): return self.containerDict
	def setContainerDict(self, _containerDict): self.containerDict = _containerDict

	def getComponentType(self): return self.getContainerDict().get('componentType', '').upper()
	def getAffordanceType(self): return self.getContainerDict().get('affordanceType', '').upper()
	def getDescr(self): return self.getContainerDict().get('descr', '')
	def getHeader(self): return self.getContainerDict().get('header', '')
	def getClassName(self): return self.getContainerDict().get('className', '')
	def getIsOptional(self): return self.getContainerDict().get('optional', False)
	def getIsFreezable(self): return self.getContainerDict().get('freezable', True)
	def getOverviewOnly(self): return self.getContainerDict().get('overviewOnly', False)
	def getIsLogEnabled(self): return self.getContainerDict().get('logEnabled', False)
	def getAccessPermissions(self): return self.getContainerDict().get('accessPermissions',[])
	def getViewPermissions(self): return self.getContainerDict().get('viewPermissions',[])
	def getStatusMsg(self): return self.getContainerDict().get('statusMsg', '')
	def getConfigDict(self): return self.getContainerDict().get('config', {})
	def getCommunity(self): return self.getWorkflow().getUserProfile().get('userProfile', {}).get('community', 'default')
	def getUsername(self): return self.getWorkflow().getUserProfile().get('userProfile', {}).get('username', '')
	def getIsMissing(self): return False

	def getIsEnabled(self):
		if self.hasPermission('isalmighty'):
			return True
		return self.getContainerDict().get('enabled', True)
	def setIsEnabled(self, _enabled): self.getContainerDict()['enabled'] = _enabled

	def getIsTask(self): return self.getComponentType() == 'TASK'
	def getIsContainer(self): return self.getComponentType() == 'CONTAINER'
	def getIsWorkflow(self): return self.getComponentType() == 'WORKFLOW'

	def getBlockers(self): return self.blockers
	def setBlockers(self, _blockers): self.blockers = _blockers

	def getIsLoaded(self): return self.isLoaded
	def setIsLoaded(self, _isLoaded): self.isLoaded = _isLoaded

	def getIsBlocked(self):
		if self.hasPermission('isalmighty'):
			return False
		return self.isBlocked
	def setIsBlocked(self, _isBlocked): self.isBlocked = _isBlocked


	#   Subclass override candidates.

	def isComplete(self):
		if not self.getIsEnabled():
			return True
		return False

	def isCompleteWithConsiderations(self):
		if (not self.getIsEnabled()) or self.getIsOptional():
			return True
		return self.isComplete()

	def getContainers(self):
		return []

	def getDeepContainers(self):
		containerList = []
		containerList.append(self)
		for each in self.getContainers():
			containers = each.getDeepContainers()
			containerList.extend(containers)
		return containerList

	def loadInstance(self):
		pass

	def hasViewPermission(self):
		return True

	def hasEditPermission(self):
		return True


	#   Logging.

	def getLogMessage(self, _verb, _item):
		blurb = constants.kJobActionBlurbDict.get(_verb, '')
		if blurb:
			return "%s %s" % (blurb, _item)

		return "%s %s" % (_verb, _item)


	#   Status calculation.

	def computeStatus(self):
		return ''


	def getRevisionsRequired(self):
		jobTask = self.getWorkflow().getJobTaskCache().get(self.getCode(),None)
		if jobTask and jobTask.get('revisions_required_approval_task',''):
			return True
		return False


	def getFieldLevelRevisionsRequired(self):
		if self.getConfigDict().get('isFieldLevelRevisable',False):
			revisionsCache = self.workflow.getFieldLevelRevisionsCache()
			if revisionsCache.get(self.getCode(),''):
				return True
		return False


	#   Task Blocking.

	def determineIfBlocked(self):
		for each in self.getBlockers():
			if not each.isCompleteWithConsiderations():
				return True
		return False


	#   Utility.

	def hasAnyPermission(self, _permissionList):
		if _permissionList:
			for permission in _permissionList:
				if self.hasPermission(permission):
					return True
		return False

	def hasPermission(self, _permission):
		if _permission:
			for permDict in self.getWorkflow().getUserPermissions():
				if permDict.get('code', '') == _permission:
					return True
		return False

	def clearJobTaskCache(self):
		self.getWorkflow().clearJobTaskCache()

	#   UI-related.

	def getDataDict(self, _sitePreferences):
		return {}

	def getAffordanceContainers(self):
		containerList = []
		if self.getIsEnabled():
			if self.getAffordanceType():
				containerList.append(self)
			for each in self.getContainers():
				containers = each.getAffordanceContainers()
				containerList.extend(containers)
		return containerList

	def getCommentPromptList(self, _activityLogKeyName):
		activityLogDict = self.getConfigDict().get(_activityLogKeyName,{})
		if activityLogDict.get('enabled', False):
			commentList = []
			for commentDict in activityLogDict.get('comments', []):
				if self.hasAnyPermission(commentDict.get('accessPermissions',[])):
					promptDict = {}
					promptDict['comment_code'] = commentDict.get('commentCode','')
					promptDict['comment_label'] = commentDict.get('commentLabel','')
					commentList.append(promptDict)
			return commentList
		return []

	def getCommentConfigForCommentCode(self, _commentCode):
		commentsList = self.getConfigDict().get('activityLog',{}).get('comments',{})
		for commentConfigDict in commentsList:
			if commentConfigDict.get('commentCode', '') == _commentCode:
				return commentConfigDict
		return None

	def extendEmailContext(self, _emailContext):
		#   Add/Change elements in the given _emailContext.
		pass

#   Site-specific folder access.

	def buildFullPathToSiteTemplate(self, _site, _templateName):
		lastPath = ''
		envUtils = coreEnvUtils.CoreEnvironment()
		site = _site.replace('-','_')
		pathList = envUtils.buildFullPathToSiteTemplatesList(site)
		for path in pathList:
			lastPath = os.path.join(path, _templateName)
			if os.path.exists(lastPath):
				return lastPath
		return lastPath

	def buildFullPathToSiteImage(self, _site, _imageName):
		lastPath = ''
		envUtils = coreEnvUtils.CoreEnvironment()
		site = _site.replace('-','_')
		pathList = envUtils.buildFullPathToSiteImagesList(site)
		for path in pathList:
			lastPath = os.path.join(path, _imageName)
			if os.path.exists(lastPath):
				return lastPath
		return lastPath
