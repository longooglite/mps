# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSCV.handlers.abstractHandler as absHandler
import MPSCore.handlers.adminUserHelper as userHelper

class UserHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['cvAdmin'])
		helper.handleUserListRequest()


class UserEditHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['cvAdmin'])
		helper.handleEditUserRequest(**kwargs)


class UserAddHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['cvAdmin'])
		helper.handleAddUserRequest()


class UserSaveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['cvAdmin'])
		helper.handleSaveUserRequest()


#   All URL mappings for this module.
urlMappings = [
	(r'/cv/users', UserHandler),
	(r'/cv/users/add', UserAddHandler),
	(r'/cv/users/edit/(?P<community>[^/]*)/(?P<username>[^/]*)', UserEditHandler),
	(r'/cv/users/save', UserSaveHandler),
]
