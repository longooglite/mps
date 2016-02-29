# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractHandler as absHandler
import MPSCore.handlers.adminUserHelper as userHelper
import MPSAppt.services.departmentService as deptSvc

class AbstractAdminUserHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def addEditCallback(self, _context, **kwargs):

		connection = self.getConnection()
		try:
			departmentSvc = deptSvc.DepartmentService(connection)
			allDepartments = departmentSvc.getAllDepartments(False)
			departmentList = deptSvc.DepartmentService(connection).getDepartmentHierarchy(allDepartments)

			if _context.get('mode','') == 'edit':
				community = kwargs.get('community', 'default')
				username = kwargs.get('username', '')
				if username:
					userdepartmentLookupDict = departmentSvc.getDepartmentsForUserAsLookupTable(community, username)

					for entryDict in departmentList:
						children = entryDict.get('children', [])
						if children:
							for kiddo in children:
								if kiddo.get('id',0) in userdepartmentLookupDict:
									kiddo['checked'] = 'checked'
						else:
							if entryDict.get('id',0) in userdepartmentLookupDict:
								entryDict['checked'] = 'checked'

			_context['departmentList'] = departmentList

		finally:
			self.closeConnection()

class UserHandler(AbstractAdminUserHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['apptUserEdit'])
		helper.handleUserListRequest()


class UserEditHandler(AbstractAdminUserHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['apptUserEdit'])
		helper.handleEditUserRequest(**kwargs)


class UserAddHandler(AbstractAdminUserHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['apptUserEdit'])
		helper.handleAddUserRequest()


class UserSaveHandler(AbstractAdminUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		helper = userHelper.AdminUserHelper(self, _requiredPermissionList=['apptUserEdit'])
		helper.handleSaveUserRequest()

	def saveCallback(self, _formData, **kwargs):

		connection = self.getConnection()
		try:
			#   Update list of accessible Departments.

			deptFormData = _formData.get('departments', '')
			if type(deptFormData) == type([]):
				departmentCodeList = deptFormData
			else:
				departmentCodeList = []
				if deptFormData:
					departmentCodeList.append(deptFormData)

			community = _formData.get('community', 'default')
			username = _formData.get('username', '').lower()
			departmentSvc = deptSvc.DepartmentService(connection)
			departmentSvc.replaceDepartmentListForUser(community, username, departmentCodeList)

		finally:
			self.closeConnection()


#   All URL mappings for this module.
urlMappings = [
	(r'/appt/users', UserHandler),
	(r'/appt/users/add', UserAddHandler),
	(r'/appt/users/edit/(?P<community>[^/]*)/(?P<username>[^/]*)', UserEditHandler),
	(r'/appt/users/save', UserSaveHandler),
]
