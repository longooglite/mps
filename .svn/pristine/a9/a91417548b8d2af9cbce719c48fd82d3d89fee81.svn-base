# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService
import MPSAuthSvc.services.permissionService as permService

class RoleService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def getRolePermissions(self, _site, _role):
		return self.getDbaseUtils().getRolePermissions(_site, _role)

	def addRole(self, _roleDict):
		self._persistRole(_roleDict, True)

	def saveRole(self, _roleDict):
		self._persistRole(_roleDict, False)

	def _persistRole(self, _roleDict, _isAdd):
		try:
			#   Update Role table data
			if _isAdd:
				self.getDbaseUtils().addRole(_roleDict, _shouldCloseConnection=False, _doCommit=False)
			else:
				self.getDbaseUtils().saveRole(_roleDict, _shouldCloseConnection=False, _doCommit=False)

			#   Update list of permissions
			if 'permissions' in _roleDict:
				siteCode = _roleDict.get('site', '')
				roleAppCode = _roleDict.get('app', '')
				roleCode = _roleDict.get('code', '')
				existingRolePermissionDicts = self.getDbaseUtils().getRolePermissions(siteCode, roleCode, _shouldCloseConnection=False)
				existingRolePermissionKeys = []
				for each in existingRolePermissionDicts:
					existingRolePermissionKeys.append("%s|%s" % (each.get('app_code',''), each.get('perm_code','')))

				permSvc = permService.PermissionService()
				allPerms = permSvc.getPermissionsForSite(siteCode)
				desiredPerms = _roleDict.get('permissions', [])
				for permDict in allPerms:
					appCode = permDict.get('app_code','')
					permCode = permDict.get('code','')
					key = "%s|%s" % (appCode, permCode)
					if key in desiredPerms:
						#   Add this Permission if not already associated with the Role
						if key not in existingRolePermissionKeys:
							self.getDbaseUtils().associateRoleWithPermission(siteCode, roleAppCode, roleCode, appCode, permCode, _shouldCloseConnection=False, _doCommit=False)
					else:
						#   Remove this Permission's association with the Role
						self.getDbaseUtils().disassociateRolePermission(siteCode, roleAppCode, roleCode, appCode, permCode, _shouldCloseConnection=False, _doCommit=False)

			#   Commit transaction
			self.getDbaseUtils().performCommit()
			self.getDbaseUtils().closeConnection()

		except Exception, e:
			try: self.getDbaseUtils().performRollback()
			except Exception, e1: pass
			raise e

	def deleteRole(self, _roleDict):
		try:
			siteCode = _roleDict.get('site', '')
			roleAppCode = _roleDict.get('app', '')
			roleCode = _roleDict.get('code', '')
			self.getDbaseUtils().disassociateAllRolePermissions(siteCode, roleAppCode, roleCode, _shouldCloseConnection=False, _doCommit=False)
			self.getDbaseUtils().deleteRole(siteCode, roleAppCode, roleCode, _shouldCloseConnection=False, _doCommit=False)

			#   Commit transaction
			self.getDbaseUtils().performCommit()
			self.getDbaseUtils().closeConnection()

		except Exception, e:
			try: self.getDbaseUtils().performRollback()
			except Exception, e1: pass
			raise e
