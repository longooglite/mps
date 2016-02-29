# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.services.permissionService as permissionSvc

class PermissionsListForSiteHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._appListHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _appListHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		targetSite = inParms.get('targetSite', None)

		permissionList = permissionSvc.PermissionService().getPermissionsForSite(targetSite)
		self.write(tornado.escape.json_encode(permissionList))


#   All URL mappings for this module.
urlMappings = [
	(r'/permissionlist', PermissionsListForSiteHandler),
]
