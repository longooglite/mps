# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils
import MPSAppt.utilities.environmentUtils as envUtils

class AbstractArtifact:
	def __init__(self, params):
		self.params = params
		self.dbConnection = params.get('dbConnection',None)
		self.context = params.get('context',{})
		self.env = params.get('env',None)
		self.workflow = params.get('workflow',None)
		self.packetCode = params.get('packetCode','')
		self.templateLoader = params.get('templateLoader',None)
		self.config = params.get('config',{})

	def getArtifact(self):
		return None

	def buildFullPathToSiteTemplate(self, _site, _templateName):
		site = _site.replace('-','_')
		lastPath = ''
		envUtils = coreEnvUtils.CoreEnvironment()
		pathList = envUtils.buildFullPathToSiteTemplatesList(site)
		for path in pathList:
			lastPath = os.path.join(path, _templateName)
			if os.path.exists(lastPath):
				return lastPath
		return lastPath

	def _resolveImageURL(self, _appCode, _skin, _imageFilename, _workflow,_isPDF=False):
		if _isPDF:
			skinFolderPath = envUtils.getEnvironment().getSkinFolderPath()
			args = ("file://%s" % skinFolderPath, _skin, _imageFilename)
		else:
			args = (self._getApplicationURLPrefix(_appCode, _workflow), _skin, _imageFilename)
		return '''%s/%s/images/%s''' % args

	def _getApplicationURLPrefix(self, _appCode,_workflow):
		appURL = self._getApplicationURL(_appCode, _workflow)
		return appURL[:appURL.rfind('/')]

	def _getApplicationURL(self, _appCode, _workflow):
		appList = _workflow.getUserProfile().get('siteProfile',{}).get('siteApplications',[])
		for appDict in appList:
			if appDict.get('code','') == _appCode:
				return appDict.get('url','')
		return ''
