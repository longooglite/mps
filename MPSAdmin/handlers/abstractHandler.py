# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.handlers.coreApplicationHandler as coreAppHandler
import MPSAdmin.utilities.environmentUtils as envUtils
from MPSAdmin.core.adminMenues import MENUES

class AbstractHandler(coreAppHandler.CoreApplicationHandler):

	def getEnvironment(self):
		return envUtils.getEnvironment()

	def getMenues(self):
		return self.buildMenuList(MENUES)

	def getAppMenues(self):
		return [self.buildApplicationMenu(self.getUserProfile().get('userApplications',[]))]

	def localizeSiteListDates(self, _siteList):
		if _siteList:
			for site in _siteList:
				self.localizeOneSiteDates(site)

	def localizeOneSiteDates(self, _siteDict):
		_siteDict['active_start'] = self.localizeDate(_siteDict.get('active_start', ''))
		_siteDict['active_end'] = self.localizeDate(_siteDict.get('active_end', ''))

	def getPostResponseDict(self, _message=None):
		responseDict = {}
		if _message:
			try:
				msgDict = self.postToAuthSvc("/putMessage", { 'message': _message })
				responseDict['msgid'] = msgDict.get('msgid', '')
			except Exception as e:
					pass
		return responseDict

	def getInitialTemplateContext(self, _environment=None):
		context = super(AbstractHandler, self).getInitialTemplateContext(_environment)
		context['windowTitle'] = 'MPS Admin'
		context['pageHeaderTitle'] = 'MPS Admin'
		return context

	def handleGetException(self, _exception, _logger, _optionalOverrideRedirect=None):
		super(AbstractHandler, self).handleGetException(_exception, _logger, _optionalOverrideRedirect)
		if not _optionalOverrideRedirect:
			self.redirect(envUtils.getEnvironment().getToastUri())
