# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

import tornado.escape

#   Helper class to drive the User Administrative editing function
#   across multiple applications.

kPasswordMask = '********'

class AdminUserHelper():

	#   Initialization, getters/setters for stuff that should be specified or
	#   can be overridden.

	def __init__(self, _reqHandler, _requiredPermissionList=[]):
		self.reqHandler = _reqHandler
		self.setRequiredPermissionList(_requiredPermissionList)
		self.sacredUserNameList = ['mpsadmin', 'mpsguru', 'bindmountainpass']
		self.sacredApplicationNameList = ['MPSADMIN']

	def getRequiredPermissionList(self): return self.requiredPermissionList
	def setRequiredPermissionList(self, _requiredPermissionList): self.requiredPermissionList = _requiredPermissionList

	def isMPSAdmin(self):
		return self.reqHandler.getEnvironment().getAppCode() == 'MPSADMIN'

	def isMPSAppt(self):
		return self.reqHandler.getEnvironment().getAppCode() == 'APPT'

	def hasUnrestrictedAccess(self):
		return (self.isMPSAdmin()) and (self.reqHandler.hasAnyPermission(['unrestrictedAdmin']))

	def extendPayload(self, _payload, **kwargs):
		if self.isMPSAdmin():
			targetSite = kwargs.get('targetSite', None)
			if targetSite:
				_payload['targetSite'] = targetSite
			return targetSite
		return None


	#   Handler for rendering the User List page.

	def handleUserListRequest(self, _htmlFilename='adminUserList.html', **kwargs):
		self.reqHandler.verifyRequest()
		self.reqHandler.verifyAnyPermission(self.getRequiredPermissionList())

		payload = self.reqHandler.getInitialPayload()
		targetSite = self.extendPayload(payload, **kwargs)
		userList = self.reqHandler.postToAuthSvc("/usersearch", payload, "Unable to obtain User data")
		countDict = self.reqHandler.postToAuthSvc("/usersearchcount", payload, "Unable to obtain User count")
		count = 0
		if countDict:
			count = countDict.get('count', 0)

		#   Show Community if there are more than one.
		displaySite = self._getDisplaySite(**kwargs)
		communityList = self._getCommunityListForSite(displaySite)

		#   Remove sacred users when using satellite applications.
		if not self.isMPSAdmin():
			userList, count = self._removeSacredUsers(userList, count)

		#   Render the page.
		context = self.reqHandler.getInitialTemplateContext(self.reqHandler.getEnvironment())
		context['userList'] = userList
		context['count'] = count
		context['countDisplayString'] = "%i Users" % count
		if len(communityList) > 1:
			context['showCommunity'] = True

		if self.isMPSAdmin():
			siteList = self.reqHandler.postToAuthSvc("/sitelist", self.reqHandler.getInitialPayload(), "Unable to obtain Site data")
			context['siteList'] = siteList
			context['isMPSAdmin'] = True
			if targetSite:
				payload = self.reqHandler.getInitialPayload()
				payload['profileSite'] = targetSite
				context['siteProfileDetail'] = self.reqHandler.postToAuthSvc("/siteprofiledetail", payload, 'Unable to locate target site')

		self.reqHandler.render(_htmlFilename, context=context, skin=context['skin'])


	#   Handler for rendering the Edit User page.

	def handleEditUserRequest(self, _htmlFilename='adminUserDetail.html', **kwargs):
		self.reqHandler.verifyRequest()
		self.reqHandler.verifyAnyPermission(self.getRequiredPermissionList())

		username = kwargs.get('username', '')
		community = kwargs.get('community', '')
		if (not username) or (not community):
			self.reqHandler.redirect('/' + self.reqHandler.getEnvironment().getAppUriPrefix())
			return

		payload = self.reqHandler.getInitialPayload()
		self.extendPayload(payload, **kwargs)
		payload['username'] = username
		payload['community'] = community
		subjectProfile = self.reqHandler.postToAuthSvc("/userprofile", payload, "Unable to obtain User data")
		appList = self._buildAppList(subjectProfile)
		roleList = self._buildRoleList(subjectProfile)

		#   Show Community if there are more than one.
		displaySite = self._getDisplaySite(**kwargs)
		communityList = self._getCommunityListForSite(displaySite)

		#   Render the page.
		context = self.reqHandler.getInitialTemplateContext(self.reqHandler.getEnvironment())
		context['mode'] = 'edit'
		context['subjectProfile'] = subjectProfile
		context['appList'] = appList
		context['roleList'] = roleList
		context['disabledApps'] = json.dumps(self._getDisabledCodeList(appList, 'code'))
		context['disabledRoles'] = json.dumps(self._getDisabledCodeList(roleList, 'key'))
		if len(communityList) > 1:
			context['showCommunity'] = True
			for communityDict in communityList:
				if communityDict.get('code', '') == community:
					subjectProfile['community_descr'] = communityDict.get('descr', '')

		if self.isMPSAdmin():
			context['isMPSAdmin'] = True
			userPrefs = context.get('subjectProfile', {}).get('userPreferences', {})
			if userPrefs.get('password', ''):
				userPrefs['password'] = kPasswordMask

		if self.isMPSAppt():
			context['isMPSAppt'] = True
			self.reqHandler.addEditCallback(context, **kwargs)

		self.reqHandler.render(_htmlFilename, context=context, skin=context['skin'])


	#   Handler for rendering the Add User page.

	def handleAddUserRequest(self, _htmlFilename='adminUserDetail.html', **kwargs):
		self.reqHandler.verifyRequest()
		self.reqHandler.verifyAnyPermission(self.getRequiredPermissionList())

		subjectProfile = { 'site': kwargs.get('targetSite', ''), 'community': 'default' }
		appList = self._buildAppList(subjectProfile)
		roleList = self._buildRoleList(subjectProfile)

		#   Prompt Community if there are more than one.
		displaySite = self._getDisplaySite(**kwargs)
		communityList = self._getCommunityListForSite(displaySite)

		#   Render the page.
		context = self.reqHandler.getInitialTemplateContext(self.reqHandler.getEnvironment())
		context['mode'] = 'add'
		context['subjectProfile'] = subjectProfile
		context['appList'] = appList
		context['roleList'] = roleList
		context['disabledApps'] = json.dumps(self._getDisabledCodeList(appList, 'code'))
		context['disabledRoles'] = json.dumps(self._getDisabledCodeList(roleList, 'key'))
		if len(communityList) > 1:
			if not self.isMPSAdmin():
				communityList = self._removeDefaultCommunity(communityList)
			if len(communityList) > 1:
				context['promptCommunity'] = True
				context['communityList'] = communityList
			else:
				subjectProfile['community'] = communityList[0].get('code', 'default')

		if self.isMPSAdmin():
			context['isMPSAdmin'] = True

		if self.isMPSAppt():
			context['isMPSAppt'] = True
			self.reqHandler.addEditCallback(context, **kwargs)

		self.reqHandler.render(_htmlFilename, context=context, skin=context['skin'])


	#   Handler for saving a User.

	def handleSaveUserRequest(self, **kwargs):
		self.reqHandler.writePostResponseHeaders()
		self.reqHandler.verifyRequest()
		self.reqHandler.verifyAnyPermission(self.getRequiredPermissionList())

		formData = tornado.escape.json_decode(self.reqHandler.request.body)
		isAdd = formData.get('mode', '') == 'add'
		username = formData.get('username', '')
		if isAdd:
			username = username.lower()

		payload = self.reqHandler.getInitialPayload()
		self.extendPayload(payload, **kwargs)
		payload['site'] = self.reqHandler.request.headers.get('Site', '')
		payload['community'] = formData.get('community', '')
		payload['username'] = username
		payload['first_name'] = formData.get('first_name', '')
		payload['last_name'] = formData.get('last_name', '')
		payload['email'] = formData.get('email', '')
		payload['active'] = formData.get('active', 'false')

		if self.isMPSAdmin():
			payload['auth_override'] = formData.get('auth_override', '')
			formPassword = formData.get('password', '')
			if formPassword != kPasswordMask:
				payload['password'] = formPassword

		appFormData = formData.get('apps', '')
		if type(appFormData) == type([]):
			apps = appFormData
		else:
			apps = []
			if appFormData:
				apps.append(appFormData)
		apps.extend(json.loads(formData.get('disabledApps', '[]')))
		payload['apps'] = apps

		roleFormData = formData.get('roles', '')
		if type(roleFormData) == type([]):
			roles = roleFormData
		else:
			roles = []
			if roleFormData:
				roles.append(roleFormData)
		roles.extend(json.loads(formData.get('disabledRoles', '[]')))
		payload['roles'] = roles

		if isAdd:
			ignoredResponseDict = self.reqHandler.postToAuthSvc("/useradd", payload, "Unable to add User data")
		else:
			ignoredResponseDict = self.reqHandler.postToAuthSvc("/usersave", payload, "Unable to save User data")

		if self.isMPSAppt():
			self.reqHandler.saveCallback(formData, **kwargs)

		responseDict = self.reqHandler.getPostResponseDict("User saved")
		responseDict['redirect'] = '/' + self.reqHandler.getEnvironment().getAppUriPrefix() + '/users'
		self.reqHandler.write(tornado.escape.json_encode(responseDict))


	#   Handler for granting Candidate access to a User.

	def handleGrantCandidateAccessRequest(self, _personDict):

		#   Tell Whoville to add the indicated User.
		#   Ignore errors (the User may already exist).

		payload = self.reqHandler.getInitialPayload()
		payload['username'] = _personDict.get('username','')
		payload['first_name'] = _personDict.get('first_name','')
		payload['last_name'] = _personDict.get('last_name','')
		try:
			self.reqHandler.postToAuthSvc("/useradd", payload, "Unable to add User data")
		except Exception, e:
			pass

		#   Now tell to update with the appropriate settings.

		appCode = self.reqHandler.getEnvironment().getAppCode()
		roles = []
		siteRolePref = self.reqHandler.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('apptcandidaterole','')
		siteRolePrefSplits = siteRolePref.split(",")
		for roleName in siteRolePrefSplits:
			roles.append("%s|%s" % (appCode, roleName))

		payload['email'] = _personDict.get('email', '')
		payload['active'] = 'true'
		payload['apps'] = [appCode]
		payload['roles'] = roles
		self.reqHandler.postToAuthSvc("/usersave", payload, "Unable to save User data")


	#   Internal companion routines.

	def _buildAppList(self, _subjectProfile):
		appList = []
		subjectHasAppList = ['LOGIN']
		userHasAppList = []

		#   First add all the apps that the User currently has access to.
		#   Each is 'checked' because the User can already use them.
		#   Take out LOGIN, end-users don't need to see it.

		for appDict in _subjectProfile.get('userApplications', []):
			thisCode = appDict.get('code', '')
			if thisCode not in subjectHasAppList:
				appDict['checked'] = 'checked'
				appList.append(appDict)
				subjectHasAppList.append(thisCode)

		#   Supplement with apps the current User is allowed to use, if any.
		#   These are not 'checked' since they weren't found in the subject's app list.

		for appDict in self.reqHandler.getProfile().get('userProfile',{}).get('userApplications',[]):
			thisCode = appDict.get('code', '')
			userHasAppList.append(thisCode)
			if thisCode not in subjectHasAppList:
				appDict['checked'] = ''
				appList.append(appDict)

		#   Mark apps as 'disabled' if the current user does not have access to them.
		#   You can't grant access to something you don't have :-)

		for appDict in appList:
			appDict['disabled'] = ''
			thisCode = appDict.get('code', '')
			if thisCode not in userHasAppList:
				appDict['disabled'] = 'disabled'

		#   Remove sacred apps when using satellite applications.
		if not self.isMPSAdmin():
			return self._removeSacredApps(appList)

		return appList

	def _buildRoleList(self, _subjectProfile):
		roleList = []
		subjectHasRoleList = []
		userHasRoleList = []

		#   First add all the roles that the User currently has access to.
		#   Each is 'checked' because the User can already use them.

		for roleDict in _subjectProfile.get('userRoles', []):
			thisCode = roleDict.get('code', '')
			if thisCode not in subjectHasRoleList:
				roleDict['checked'] = 'checked'
				roleList.append(roleDict)
				subjectHasRoleList.append(thisCode)

		#   Supplement with roles the current User is allowed to use, if any.
		#   These are not 'checked' since they weren't found in the subject's role list.

		roles = self.reqHandler.getProfile().get('userProfile',{}).get('userRoles',[])
		if self.hasUnrestrictedAccess():
			payload = self.reqHandler.getInitialPayload()
			payload['profileSite'] = _subjectProfile.get('site','')
			siteProfile = self.reqHandler.postToAuthSvc("/siteprofiledetail", payload, 'Unable to locate target site')
			roles = siteProfile.get('siteRoles', [])
			for each in roles:
				each['application_code'] = each.get('app_code', '')
				each['application_descr'] = each.get('app_descr', '')

		for roleDict in roles:
			thisCode = roleDict.get('code', '')
			userHasRoleList.append(thisCode)
			if thisCode not in subjectHasRoleList:
				roleDict['checked'] = ''
				roleList.append(roleDict)

		#   Mark roles as 'disabled' if the current user does not have access to them.
		#   You can't grant access to something you don't have :-)
		#   Assign row 'keys', a concatenation of app code and role code.

		for roleDict in roleList:
			roleDict['disabled'] = ''
			thisCode = roleDict.get('code', '')
			if thisCode not in userHasRoleList:
				roleDict['disabled'] = 'disabled'
			roleDict['key'] = "%s|%s" % (roleDict.get('application_code', ''), thisCode)

		#   Remove roles for sacred apps when using satellite applications.
		if not self.isMPSAdmin():
			return self._removeRolesForSacredApps(roleList)

		return roleList

	def _getDisabledCodeList(self, _list, _keyName):
		disabledList = []
		for aDict in _list:
			if aDict.get('disabled', ''):
				disabledList.append(aDict.get(_keyName, ''))
		return disabledList

	def _removeSacredUsers(self, _userList, _count):
		userList = []
		nbrSacred = 0
		for userDict in _userList:
			if userDict.get('username', '') in self.sacredUserNameList:
				nbrSacred += 1
			else:
				userList.append(userDict)

		count = _count - nbrSacred
		if count < 0:
			count = 0
		return userList, count

	def _removeSacredApps(self, _appList):
		appList = []
		for appDict in _appList:
			if appDict.get('code', '') not in self.sacredApplicationNameList:
				appList.append(appDict)
		return appList

	def _removeRolesForSacredApps(self, _roleList):
		roleList = []
		for roleDict in _roleList:
			if roleDict.get('application_code', '') not in self.sacredApplicationNameList:
				roleList.append(roleDict)
		return roleList

	def _getDisplaySite(self, **kwargs):
		targetSite = kwargs.get('targetSite', None)
		if targetSite:
			return targetSite
		return self.reqHandler.request.headers.get('Site', '')

	def _getCommunityList(self):
		return self.reqHandler.postToAuthSvc("/communitylist", self.reqHandler.getInitialPayload(), "Unable to obtain Community data")

	def _getCommunityListForSite(self, _siteCode):
		communityList = []
		if _siteCode:
			for communityDict in self._getCommunityList():
				if communityDict.get('site_code', '') == _siteCode:
					communityList.append(communityDict)
		return communityList

	def _removeDefaultCommunity(self, _communityList):
		newList = []
		for communityDict in _communityList:
			if communityDict.get('code', '') != 'default':
				newList.append(communityDict)
		return newList
