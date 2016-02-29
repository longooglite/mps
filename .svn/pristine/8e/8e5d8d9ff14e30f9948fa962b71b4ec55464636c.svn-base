# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.caches.userCache as userCash
import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.services.userService as usrSvc
import MPSAuthSvc.services.userSearchService as usrSearchSvc
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractUserHandler(absHandler.AbstractHandler):
	def determineSite(self, _parms):
		site = _parms.get('targetSite', None)
		if not site:
			site = _parms.get('site', None)
		return site

class GetUserHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getUserHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getUserHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = inParms.get('site', None)
		community = inParms.get('community', 'default')
		username = inParms.get('username', None)

		userSvc = usrSvc.UserService()
		user = userSvc.getUser(site, community, username)
		self.write(tornado.escape.json_encode(user))


class UserListHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._userListHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _userListHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = inParms.get('site', None)
		app = inParms.get('app', None)

		userSvc = usrSvc.UserService()
		userList = userSvc.getUsersForSiteAndApplication(site, app)

		permissions = inParms.get('permissions', [])
		if permissions:
			filteredList = self.filterUserListByPermissions(site, app, userList, permissions)
			self.write(tornado.escape.json_encode(filteredList))
			return

		self.write(tornado.escape.json_encode(userList))

	def filterUserListByPermissions(self, _site, _app, _userList, _permissions):
		filteredList = []
		for userDict in _userList:
			community = userDict.get('community', 'default')
			username = userDict.get('username','')
			if username:
				userProfile = self.getOrCreateUser(_site, community, username)
				if self.profileHasAnyPermission(_app, userProfile, _permissions):
					filteredList.append(userDict)

		return filteredList

	def profileHasAnyPermission(self, _app, _userProfile, _permissionList):
		userPermissions = self.buildFlatPermissionList(_app, _userProfile)
		for permission in _permissionList:
			if permission in userPermissions:
				return True
		return False

	def buildFlatPermissionList(self, _app, _userProfile):
		flat = {}
		for permDict in _userProfile.get('userPermissions', []):
			if permDict.get('appcode','') == _app:
				permCode = permDict.get('code','')
				if permCode:
					flat[permCode] = True
		return flat.keys()


class UserSearchHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = self.determineSite(inParms)
		searchCriteria = inParms.get('search_criteria', '')
		limit = inParms.get('limit', 0)
		offset = inParms.get('offset', 0)

		users = usrSearchSvc.UserSearchService().userSearch(site, None, searchCriteria, _limit=limit, _offset=offset)
		self.write(tornado.escape.json_encode(users))


class UserSearchCountHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = self.determineSite(inParms)
		searchCriteria = inParms.get('search_criteria', '')

		countDict = usrSearchSvc.UserSearchService().userSearchCount(site, searchCriteria)
		self.write(tornado.escape.json_encode(countDict))


class ProxyUserSearchHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getUserHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getUserHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = inParms.get('site', None)
		search_community = inParms.get('search_community', None)
		search_criteria = inParms.get('search_criteria', '')

		users = usrSearchSvc.UserSearchService().userSearch(site, search_community, search_criteria)
		self.write(tornado.escape.json_encode(users))


class UserProfileHandler(AbstractUserHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = self.determineSite(inParms)
		community = inParms.get('community', 'default')
		username = inParms.get('username', '')

		#   Get the user profile for the specified user.

		userProfile = self.getOrCreateUser(site, community, username)
		if not userProfile:
			raise excUtils.MPSValidationException("Invalid User identifier")

		self.write(tornado.escape.json_encode(userProfile))


class AbstractUserSaveHandler(AbstractUserHandler):
	def _userValidation(self, _isAdd):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		inParms['community'] = inParms.get('community', 'default')
		
		communityError = self.checkStringRequired(inParms, 'community', "Community required")
		userError = self.checkStringRequired(inParms, 'username', "Username required")
		fnameError = self.checkStringRequired(inParms, 'first_name', "First Name required")
		lnameError = self.checkStringRequired(inParms, 'last_name', "Last Name required")
		errorList = []
		if communityError: errorList.append(communityError)
		if userError: errorList.append(userError)
		if fnameError: errorList.append(fnameError)
		if lnameError: errorList.append(lnameError)
		if errorList:
			raise excUtils.MPSValidationException(errorList)

		site = self.determineSite(inParms)
		siteProfile = self.getOrCreateSite(site)
		if not siteProfile:
			raise excUtils.MPSValidationException("Invalid Site code identifier")

		community = inParms.get('community', 'default')
		username = inParms.get('username', None)
		if _isAdd:
			username = username.lower()
		else:
			userProfile = self.getOrCreateUser(site, community, username)
			if not userProfile:
				raise excUtils.MPSValidationException("Invalid Username identifier")

		userDict = {}
		userDict['site'] = site
		userDict['community'] = community
		userDict['username'] = username
		userDict['first_name'] = inParms['first_name']
		userDict['last_name'] = inParms['last_name']
		userDict['email'] = inParms.get('email', '')
		userDict['active'] = inParms.get('active', 'false')
		if 'auth_override' in inParms:
			userDict['auth_override'] = inParms.get('auth_override', '')
		if 'password' in inParms:
			userDict['password'] = inParms.get('password', '')
		if 'apps' in inParms:
			userDict['apps'] = inParms.get('apps', [])
		if 'roles' in inParms:
			userDict['roles'] = inParms.get('roles', [])
		return userDict


class UserAddHandler(AbstractUserSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._userAddHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _userAddHandlerImpl(self):
		userDict = self._userValidation(True)
		usrSvc.UserService().addUser(userDict)
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "User added" }))

class UserSaveHandler(AbstractUserSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._userSaveHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _userSaveHandlerImpl(self):
		userDict = self._userValidation(False)
		usrSvc.UserService().saveUser(userDict)
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "User saved" }))


#   All URL mappings for this module.
urlMappings = [
	(r'/getuser', GetUserHandler),
	(r'/userlist', UserListHandler),
	(r'/usersearch', UserSearchHandler),
	(r'/usersearchcount', UserSearchCountHandler),
	(r'/proxyusersearch', ProxyUserSearchHandler),
	(r'/userprofile', UserProfileHandler),
	(r'/useradd', UserAddHandler),
	(r'/usersave', UserSaveHandler),
]
