# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService

class UserService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def getUser(self, _site, _community, _username):
		return self.getDbaseUtils().getUser(_site, _community, _username)

	def getUserApplications(self, _site, _community, _username):
		return self.getDbaseUtils().getUserApplications(_site, _community, _username)

	def getUserRoles(self, _site, _community, _username):
		return self.getDbaseUtils().getUserRoles(_site, _community, _username)

	def getUserPermissions(self, _site, _community, _username):
		return self.getDbaseUtils().getUserPermissions(_site, _community, _username)

	def addUser(self, _userDict):
		self._persistUser(_userDict, True)

	def saveUser(self, _userDict):
		self._persistUser(_userDict, False)

	def _persistUser(self, _userDict, _isAdd):
		try:
			#   Update mpsuser table data
			if _isAdd:
				self.getDbaseUtils().addUser(_userDict, _shouldCloseConnection=False, _doCommit=False)
			else:
				self.getDbaseUtils().saveUser(_userDict, _shouldCloseConnection=False, _doCommit=False)

			#   Update list of allowed applications
			site = _userDict.get('site',None)
			community = _userDict.get('community', 'default')
			username = _userDict.get('username','').lower()
			if 'apps' in _userDict:
				#   Delete existing application association rows for this User.
				#   Then add the desired applications in the specified order.
				self.getDbaseUtils().disassociateAllApplicationsFromUser(site, community, username, _shouldCloseConnection=False, _doCommit=False)

				seqnbr = 1
				for appCode in _userDict.get('apps', []):
					self.getDbaseUtils().associateApplicationWithUser(site, community, username, appCode, seqnbr, _shouldCloseConnection=False, _doCommit=False)
					seqnbr += 1

			#   Update list of allowed roles
			if 'roles' in _userDict:
				#   Delete existing role association rows for this User.
				#   Then add the desired roles.
				self.getDbaseUtils().disassociateAllRolesFromUser(site, community, username, _shouldCloseConnection=False, _doCommit=False)

				for appRoleCode in _userDict.get('roles', []):
					splits = appRoleCode.split('|')
					appCode = splits[0]
					roleCode = splits[1]
					self.getDbaseUtils().associateRoleWithUser(site, community, username, appCode, roleCode, _shouldCloseConnection=False, _doCommit=False)

			#   Commit transaction
			self.getDbaseUtils().performCommit()
			self.getDbaseUtils().closeConnection()

		except Exception, e:
			try: self.getDbaseUtils().performRollback()
			except Exception, e1: pass
			raise e

	def getUsersForSiteAndApplication(self, _site, _appCode):
		return self.getDbaseUtils().getUsersForSiteAndApplication(_site, _appCode)
