# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.caches.siteCache as siteCash
import MPSAuthSvc.caches.userCache as userCash
import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.services.applicationService as appSvc
import MPSAuthSvc.services.roleService as roleSvc
import MPSCore.utilities.exceptionUtils as excUtils


class AbstractRoleSaveHandler(absHandler.AbstractHandler):
	def _roleValidation(self, _isDelete=False):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		self.validateStringRequired(inParms, 'targetSite', "Site code required")
		self.validateStringRequired(inParms, 'targetApp', "App code required")
		self.validateStringRequired(inParms, 'code', "Role code required")
		if not _isDelete:
			self.validateStringRequired(inParms, 'descr', "Role description required")

		siteCode = inParms.get('targetSite', None)
		siteProfile = self.getOrCreateSite(siteCode)
		if not siteProfile:
			raise excUtils.MPSValidationException("Invalid Site code identifier")

		appCode = inParms.get('targetApp', None)
		appList = appSvc.ApplicationService().getApplicationForCode(appCode)
		if not appList:
			raise excUtils.MPSValidationException("Invalid Application code identifier")

		roleDict = {}
		roleDict['site'] = siteCode
		roleDict['app'] = appCode
		roleDict['code'] = inParms.get('code', None)
		if not _isDelete:
			roleDict['descr'] = inParms['descr']
		if 'permissions' in inParms:
			roleDict['permissions'] = inParms.get('permissions', [])
		return roleDict


class RoleAddHandler(AbstractRoleSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._roleAddHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _roleAddHandlerImpl(self):
		roleDict = self._roleValidation()
		roleSvc.RoleService().addRole(roleDict)
		siteCash.getSiteCache().invalidateCache()
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Role added" }))

class RoleSaveHandler(AbstractRoleSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._roleSaveHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _roleSaveHandlerImpl(self):
		roleDict = self._roleValidation()
		roleSvc.RoleService().saveRole(roleDict)
		siteCash.getSiteCache().invalidateCache()
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Role saved" }))


class RoleDeleteHandler(AbstractRoleSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._roleDeleteHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _roleDeleteHandlerImpl(self):
		roleDict = self._roleValidation(_isDelete=True)
		roleSvc.RoleService().deleteRole(roleDict)
		siteCash.getSiteCache().invalidateCache()
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Role deleted" }))


#   All URL mappings for this module.
urlMappings = [
	(r'/roleadd', RoleAddHandler),
	(r'/rolesave', RoleSaveHandler),
	(r'/roledelete', RoleDeleteHandler),
]
