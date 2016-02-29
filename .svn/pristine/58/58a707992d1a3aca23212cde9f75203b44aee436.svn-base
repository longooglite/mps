# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.userService as userSvc
import MPSCore.utilities.stringUtilities as stringUtils

#   User Info.

class UserInfo():

	def __init__(self, _site, _community, _username):
		self.setSite(_site)
		self.setCommunity(_community)
		self.setUsername(_username)
		self.initUserPreferences()
		self.initUserApplications()
		self.initUserRoles()
		self.initUserPermissions()

	def getSite(self): return self.site
	def setSite(self, _site): self.site = _site

	def getCommunity(self): return self.community
	def setCommunity(self, _community): self.community = _community

	def getUsername(self): return self.username
	def setUsername(self, _username): self.username = _username

	def getUserPreferences(self): return self.userPreferences
	def setUserPreferences(self, _userPreferences): self.userPreferences = _userPreferences
	def initUserPreferences(self): self.setUserPreferences({})

	def getUserApplications(self): return self.userApplications
	def setUserApplications(self, _userApplications): self.userApplications = _userApplications
	def initUserApplications(self): self.setUserApplications([])

	def getUserRoles(self): return self.userRoles
	def setUserRoles(self, _userRoles): self.userRoles = _userRoles
	def initUserRoles(self): self.setUserRoles([])

	def getUserPermissions(self): return self.userPermissions
	def setUserPermissions(self, _userPermissions): self.userPermissions = _userPermissions
	def initUserPermissions(self): self.setUserPermissions([])

	def buildUser(self, _optionalCommunity=None, _optionalUsername=None):
		community = _optionalCommunity if _optionalCommunity else self.getCommunity()
		username = _optionalUsername if _optionalUsername else self.getUsername()
		userService = userSvc.UserService()
		prefDict = userService.getUser(self.getSite(), community, username)
		fn = prefDict.get('first_name', '')
		ln = prefDict.get('last_name', '')
		prefDict['full_name'] = stringUtils.constructFullName(fn, ln)
		prefDict['description'] = "%s (%s)" % (prefDict['full_name'], prefDict.get('username', ''))

		appList = userService.getUserApplications(self.getSite(), community, username)
		for item in appList:
			item['url'] = item['url'].replace('${site}', self.getSite())

		roleList = userService.getUserRoles(self.getSite(), community, username)
		permissionList = userService.getUserPermissions(self.getSite(), community, username)

		self.setUserPreferences(prefDict)
		self.setUserApplications(appList)
		self.setUserRoles(roleList)
		self.setUserPermissions(permissionList)


	def profile(self):
		myProfile = dict()
		myProfile['site'] = self.getSite()
		myProfile['community'] = self.getCommunity()
		myProfile['username'] = self.getUsername()
		myProfile['userPreferences'] = self.getUserPreferences()
		myProfile['userApplications'] = self.getUserApplications()
		myProfile['userRoles'] = self.getUserRoles()
		myProfile['userPermissions'] = self.getUserPermissions()
		return myProfile
