# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.services.applicationService as applicationSvc

class ApplicationListHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._appListHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _appListHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		appList = applicationSvc.ApplicationService().getAllApplications()
		self.write(tornado.escape.json_encode(appList))


#   All URL mappings for this module.
urlMappings = [
	(r'/applist', ApplicationListHandler),
]
