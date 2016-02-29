# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.utilities.environmentUtils as envUtils

class AbstractRoleHandler(absHandler.AbstractHandler):

	def _getSiteProfileDetail(self, _site):
		payload = self.getInitialPayload()
		payload['profileSite'] = _site
		return self.postToAuthSvc("/siteprofiledetail", payload, 'Unable to locate target site')

	def _getEnabledPermissionCodes(self, _permissionList):
		enabledPermissionList = []
		for permDict in _permissionList:
			key = "%s|%s" % (permDict.get('app_code',''), permDict.get('perm_code', ''))
			enabledPermissionList.append(key)
		return enabledPermissionList

	def _identifyEnabledPermissionss(self, _permissionList, _enabledPermissionList):
		for permDict in _permissionList:
			key = "%s|%s" % (permDict.get('app_code',''), permDict.get('code', ''))
			permDict['key'] = key
			permDict['checked'] = ''
			if key in _enabledPermissionList:
				permDict['checked'] = "checked"

class RoleViewHandler(AbstractRoleHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyPermission('roleView')

		site = kwargs.get('siteCode', self.request.headers.get('Site', ''))
		siteList = self.postToAuthSvc("/sitelist", self.getInitialPayload(), "Unable to obtain Site data")
		siteProfileDetail = self._getSiteProfileDetail(site)

		#   Render the page.

		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['siteList'] = siteList
		context['siteProfileDetail'] = siteProfileDetail
		context['disabled'] = "" if self.hasPermission('roleEdit') else "disabled"
		self.render("roleList.html", context=context, skin=context['skin'])


class RoleDetailHandler(AbstractRoleHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['roleView','roleEdit'])

		siteCode = kwargs.get('siteCode', '')
		appCode = kwargs.get('appCode', '')
		roleCode = kwargs.get('roleCode', '')
		siteProfileDetail = self._getSiteProfileDetail(siteCode)

		roleDict = {}
		for thisRoleDict in siteProfileDetail.get('siteRoles', []):
			if thisRoleDict.get('app_code', '') == appCode and thisRoleDict.get('code', '') == roleCode:
				roleDict = thisRoleDict
				break

		payload = self.getInitialPayload()
		payload['targetSite'] = siteCode
		permissionList = self.postToAuthSvc("/permissionlist", payload, "Unable to obtain Site Permission data")
		enabledPermissionList = self._getEnabledPermissionCodes(roleDict.get('permissionList', []))
		self._identifyEnabledPermissionss(permissionList, enabledPermissionList)

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = 'edit'
		context['siteProfileDetail'] = siteProfileDetail
		context['roleDict'] = roleDict
		context['appList'] = []
		context['permissionList'] = permissionList
		context['disabled'] = "" if self.hasPermission('roleEdit') else "disabled"
		self.render("roleDetail.html", context=context, skin=context['skin'])


class RoleAddHandler(AbstractRoleHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyPermission('roleEdit')

		site = kwargs.get('siteCode', '')
		siteProfileDetail = self._getSiteProfileDetail(site)
		appList = self.postToAuthSvc("/applist", self.getInitialPayload(), "Unable to obtain Application data")

		payload = self.getInitialPayload()
		payload['targetSite'] = site
		permissionList = self.postToAuthSvc("/permissionlist", payload, "Unable to obtain Site Permission data")
		self._identifyEnabledPermissionss(permissionList, [])

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = 'add'
		context['siteProfileDetail'] = siteProfileDetail
		context['roleDict'] = {}
		context['appList'] = appList
		context['permissionList'] = permissionList
		context['disabled'] = ""
		self.render("roleDetail.html", context=context, skin=context['skin'])


class RoleSaveHandler(AbstractRoleHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('roleEdit')

		formData = tornado.escape.json_decode(self.request.body)
		isAdd = formData.get('mode', '') == 'add'
		siteCode = formData.get('site_code', '')
		appCode = formData.get('app_code', '')
		code = formData.get('code', '')

		payload = self.getInitialPayload()
		payload['targetSite'] = siteCode
		payload['targetApp'] = appCode
		payload['code'] = code
		payload['descr'] = formData.get('descr', '')
		payload['permissions'] = formData.get('permissions', [])

		if isAdd:
			ignoredResponseDict = self.postToAuthSvc("/roleadd", payload, "Unable to add Role data")
		else:
			ignoredResponseDict = self.postToAuthSvc("/rolesave", payload, "Unable to save Role data")

		responseDict = self.getPostResponseDict("Role saved")
		responseDict['redirect'] = '/admin/roles/' + siteCode
		self.write(tornado.escape.json_encode(responseDict))


class RoleDeleteHandler(AbstractRoleHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyPermission('roleEdit')

		siteCode = kwargs.get('siteCode', '')
		appCode = kwargs.get('appCode', '')
		roleCode = kwargs.get('roleCode', '')

		payload = self.getInitialPayload()
		payload['targetSite'] = siteCode
		payload['targetApp'] = appCode
		payload['code'] = roleCode
		ignoredResponseDict = self.postToAuthSvc("/roledelete", payload, "Unable to delete Role")

		self.redirect('/admin/roles/' + siteCode)


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/role/save', RoleSaveHandler),
	(r'/admin/role/add/(?P<siteCode>[^/]*)', RoleAddHandler),
	(r'/admin/role/edit/(?P<siteCode>[^/]*)/(?P<appCode>[^/]*)/(?P<roleCode>[^/]*)', RoleDetailHandler),
	(r'/admin/role/delete/(?P<siteCode>[^/]*)/(?P<appCode>[^/]*)/(?P<roleCode>[^/]*)', RoleDeleteHandler),
	(r'/admin/roles/(?P<siteCode>[^/]*)', RoleViewHandler),
	(r'/admin/roles', RoleViewHandler),
]
