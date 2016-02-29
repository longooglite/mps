# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAdmin.handlers.abstractHandler as absHandler
import MPSCore.handlers.adminUserHelper as userHelper

kKeyName = 'MPSADMIN_UserDisplayParms'

class AbstractUserHandler(absHandler.AbstractHandler):

	def _getUserDisplayParms(self):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		response = self.postToAuthSvc("/getRandomSessionData", payload, "Unable to obtain %s" % kKeyName)
		displayDict = response.get('value', None)
		if displayDict:
			return displayDict
		return self._getInitialUserDisplayParms()

	def _getInitialUserDisplayParms(self):
		displayDict = {}
		displayDict['site'] = self.request.headers.get('Site', '')
		return displayDict

	def _putUserDisplayParms(self, _displayDict):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		payload['value'] = _displayDict
		response = self.postToAuthSvc("/putRandomSessionData", payload, "Unable to save %s" % kKeyName)


class UserHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		parmsDict = self._getUserDisplayParms()
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['userView'])
		helper.handleUserListRequest(targetSite=parmsDict.get('site',''))


class UserEditHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		parmsDict = self._getUserDisplayParms()
		kwargs['targetSite'] = parmsDict.get('site','')
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['userEdit'])
		helper.handleEditUserRequest(**kwargs)


class UserAddHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		parmsDict = self._getUserDisplayParms()
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['userEdit'])
		helper.handleAddUserRequest(targetSite=parmsDict.get('site',''))


class UserSaveHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		parmsDict = self._getUserDisplayParms()
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['userEdit'])
		helper.handleSaveUserRequest(targetSite=parmsDict.get('site',''))


class ChangeSiteHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['userView'])

		parmsDict = self._getUserDisplayParms()
		formData = tornado.escape.json_decode(self.request.body)
		target = formData.get('target', '')
		parmsDict['site'] = target
		self._putUserDisplayParms(parmsDict)

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/admin/users'
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/users', UserHandler),
	(r'/admin/users/add', UserAddHandler),
	(r'/admin/users/edit/(?P<community>[^/]*)/(?P<username>[^/]*)', UserEditHandler),
	(r'/admin/users/save', UserSaveHandler),
	(r'/admin/users/site', ChangeSiteHandler),
]
