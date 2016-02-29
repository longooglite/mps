# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os.path
import tornado.web
import tornado.httpclient
import json

import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.sqlUtilities as sqlUtils
import MPSCore.utilities.stringUtilities as stringUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper
import MPSCore.utilities.coreEnvironmentUtils as coreEnv

#   Super-class for all application handler classes.
#   Intentionally NOT used by:
#       MPSAuthSvc

globalRequestData = {}

class CoreApplicationHandler(tornado.web.RequestHandler):

	def initialize(self):
		global globalRequestData
		globalRequestData.clear()

	#   Common profile, returned from MPS Authorization Service.

	def getProfile(self):
		if not hasattr(self, 'profile'):
			self.setProfile(None)
		return self.profile
	def setProfile(self, _profile): self.profile = _profile

	def getUserProfile(self):
		return self.getProfile().get('userProfile', {})

	def getUserProfileCommunity(self):
		return self.getUserProfile().get('community', 'default')

	def getUserProfileUsername(self):
		return self.getUserProfile().get('username', '')

	def getUserPermissions(self):
		return self.getUserProfile().get('userPermissions', [])

	def hasPermission(self, _permission):
		if _permission:
			for permDict in self.getUserPermissions():
				if permDict.get('code', '') == _permission:
					return True
		return False

	def hasAnyPermission(self, _permissionList):
		if _permissionList:
			for permission in _permissionList:
				if self.hasPermission(permission):
					return True
		return False

	@mpsExceptionWrapper("Operation not permitted")
	def verifyPermission(self, _permission):
		if not self.hasPermission(_permission):
			raise excUtils.MPSValidationException("Operation not permitted")

	@mpsExceptionWrapper("Operation not permitted")
	def verifyAnyPermission(self, _permissionList):
		if not self.hasAnyPermission(_permissionList):
			raise excUtils.MPSValidationException("Operation not permitted")


	#   Miscellaneous.

	def getCookie(self, _cookie):
		return self.get_cookie(_cookie, None)

	def getInitialTemplateContext(self, _environment=None):
		context = dict()
		context['site'] = self.request.headers.get('Site', '')
		context['mpsid'] = self.getCookie('mpsid')
		context['_xsrf'] = self.xsrf_token
		if _environment:
			context['envCode'] = _environment.getEnvCode()
			context['appCode'] = _environment.getAppCode()
			context['appUriPrefix'] = _environment.getAppUriPrefix()
			context['rootFolderPath'] = _environment.getSrcRootFolderPath()
			context['coreFolderPath'] = _environment.getSrcCoreFolderPath()
			context['coreHtmlFolderPath'] = os.path.join(context['coreFolderPath'], 'html')
			context['loginUri'] = _environment.getLoginUri()
			context['toastUri'] = _environment.getToastUri()
			context['utcDateFormat'] = _environment.getUTCDateFormat()

		auth = {}
		auth['appCode'] = context.get('appCode','')
		auth['site'] = context['site']
		auth['mpsid'] = context['mpsid']
		auth['_xsrf'] =  context['_xsrf']
		context['auth'] = auth

		theProfile = {}
		if hasattr(self, 'profile') and self.getProfile() is not None:
			theProfile = self.getProfile()
		context['siteProfile'] = theProfile.get('siteProfile', {})
		context['userProfile'] = theProfile.get('userProfile', {})
		context['menuList'] = self.getMenues()
		context['appMenuList'] = self.getAppMenues()
		context['skin'] = context.get('siteProfile',{}).get('sitePreferences',{}).get('skin', 'default')

		context['ofaText'] = context.get('siteProfile',{}).get('sitePreferences',{}).get('ofatext', 'Faculty Affairs')
		context['departmentText'] = context.get('siteProfile',{}).get('sitePreferences',{}).get('departmenttext', 'Department')

		msgid = self.getCookie('msgid')
		if msgid:
			try:
				messageDict = self.postToAuthSvc("/getMessage", { 'msgid': msgid })
				context['errormessage'] = messageDict.get('message', '')
				self.clear_cookie('msgid')
			except Exception as e:
					pass

		return context

	def writePostResponseHeaders(self):
		self.set_header('Content-Type','application/json')

	def writePostPDFResponseHeaders(self):
		self.set_header('Content-Type',"application/pdf")


	def localizeDate(self, _dateString):
		return self.getEnvironment().localizeUTCDate(_dateString, self.getSiteTimezone())

	#   Common timestamp format preference routines.

	def getSiteYearFormat(self): return self.getSitePreference('yformat', '%Y')
	def getSiteYearMonthFormat(self): return self.getSitePreference('ymformat', '%m/%Y')
	def getSiteYearMonthDayFormat(self): return self.getSitePreference('ymdformat', '%m/%d/%Y')
	def getSiteYearMonthDayHourFormat(self): return self.getSitePreference('ymdhformat', '%m/%d/%Y %H')
	def getSiteYearMonthDayHourMinuteFormat(self): return self.getSitePreference('ymdhmformat', '%m/%d/%Y %H:%M')
	def getSiteYearMonthDayHourMinuteSecondFormat(self): return self.getSitePreference('ymdhmsformat', '%m/%d/%Y %H:%M:%S')

	def getSitePreferences(self):
		return self.getProfile().get('siteProfile', {}).get('sitePreferences', {})

	def getSitePreference(self, _key, _defaultValue):
		return self.getSitePreferences().get(_key, _defaultValue)

	def getSitePreferenceAsInt(self, _key, _defaultValue):
		rawValue = self.getSitePreference(_key, _defaultValue)
		try:
			return int(rawValue)
		except Exception, e:
			return _defaultValue

	def getSitePreferenceAsBoolean(self, _key, _defaultValue):
		rawValue = self.getSitePreference(_key, _defaultValue)
		return stringUtils.interpretAsTrueFalse(rawValue)

	def getSiteCommunityList(self):
		return self.getProfile().get('siteProfile',{}).get('siteCommunities', [])

	def getSiteTimezone(self):
		return self.getProfile().get('siteProfile', {}).get('sitePreferences', {}).get('timezone', 'US/Eastern')

	def removeFormDataNoise(self):
		goodData = {}
		formData = tornado.escape.json_decode(self.request.body)
		for keyName in formData.keys():
			if keyName not in ['mpsid','appCode','site']:
				goodData[keyName] = formData[keyName]
		return goodData

	#   Common menu-building routines.

	def getMenues(self):
		#   Placeholder, intended to be overridden by subclasses.
		return []

	def getAppMenues(self):
		#   Placeholder, intended to be overridden by subclasses.
		return []

	def buildApplicationMenu(self, _userApplications):
		itemList = []
		title = 'Applications'

		appCode = 'BOGUS'
		try:
			appCode = self.getEnvironment().getAppCode()
		except Exception, e:
			pass

		for appDict in _userApplications:
			itemDict = {}
			itemDict['descr'] = appDict.get('descr', '?')
			itemDict['url'] = appDict.get('url', '#')
			itemDict['enabled'] = 'true'
			itemList.append(itemDict)
			if appDict.get('code', '?') == appCode:
				title = itemDict['descr']

		menuDict = {}
		menuDict['descr'] = title
		menuDict['itemList'] = itemList
		menuDict['enabled'] = 'true'
		menuDict['glyph'] = 'glyphicon-tasks'
		return menuDict

	def buildMenuList(self, _menues):
		menuList = []
		for menu in _menues:
			menuDict = self.buildOneMenu(menu)
			if menuDict:
				menuList.append(menuDict)
		return menuList

	def buildOneMenu(self, _menu):
		if not self.hasPermissionForMenu(_menu):
			return None

		itemList = []
		if _menu.get('rootid','') == 'print':
			itemList = self.buildPrintItemList()
		else:
			for menuItemDict in _menu.get('itemList', []):
				if self.hasPermissionForMenu(menuItemDict):
					itemDict = {}
					itemDict['descr'] = menuItemDict.get('descr', '?')
					if 'url' in menuItemDict:
						itemDict['url'] = menuItemDict.get('url', '#')
					if 'id' in menuItemDict:
						itemDict['id'] = menuItemDict.get('id', '#')
					if 'target' in menuItemDict:
						itemDict['target'] = menuItemDict.get('target', '_blank')
					if 'glyph' in menuItemDict:
						itemDict['glyph'] = menuItemDict.get('glyph', '')
					if 'divider' in menuItemDict:
						itemDict['divider'] = menuItemDict.get('divider', '')
					itemList.append(itemDict)

		menuDict = {}
		menuDict['descr'] = _menu.get('descr', '?')
		menuDict['glyph'] = _menu.get('glyph', '')
		menuDict['itemListHasGlyphs'] = _menu.get('itemListHasGlyphs', False)
		if 'url' in _menu:
			menuDict['url'] = _menu['url']
		if 'id' in _menu:
			menuDict['id'] = _menu['id']
		if 'rootid' in _menu:
			menuDict['rootid'] = _menu['rootid']
		if 'enabled' in _menu:
			menuDict['enabled'] = _menu['enabled']
		if 'divider' in _menu:
			menuDict['divider'] = _menu.get('divider', '')
		if itemList:
			menuDict['itemList'] = itemList
		return menuDict

	def buildPrintItemList(self):
		#   if there is a print menu config file, and there's only one entry, make it look like it always did
		#   if there is a print menu config file, and there's more than one entry, differentiate the menu items with the template description
		printAllURL = '/cv/print/{cvCommunity}/{cvOwner}/'
		printSectionURL = '/cv/print/{cvCommunity}/{cvOwner}/{categoryCode}/'
		itemList = []
		templateConfig = self.getTemplateConfig()
		if templateConfig:
			if self.hasPermission("cvView"):
				if len(templateConfig) == 1:
					itemList.append({'descr':'Print All','target':'_blank','url':printAllURL +  templateConfig[0].get('template','printMain.html')})
					itemList.append({'descr':'Print Section','altdescr':'','isSectionPrint':'True','target':'_blank','url':printSectionURL +  templateConfig[0].get('template','printMain.html')})
				else:
					for template in templateConfig:
						itemList.append({'descr':'Print All - %s' % template.get('descr'),'target':'_blank','url':printAllURL +  template.get('template','printMain.html')})
						itemList.append({'descr':'Print Section - %s' % template.get('descr'),'altdescr':template.get('descr'),'isSectionPrint':'True','target':'_blank','url':printSectionURL +  template.get('template','printMain.html')})
		return itemList

	def getTemplateConfig(self):
		config = None
		f = None
		try:
			templatePathList = coreEnv.CoreEnvironment().buildFullPathToCVSiteTemplatesList(self.getProfile().get('siteProfile',{}).get('site',''))
			for rootPath in templatePathList:
				fullPath = os.path.join(rootPath,'templateMenuConfig.json')
				if os.path.exists(fullPath):
					f = open(fullPath,'rU')
					content = f.read()
					config = json.loads(content)
					break
		except:
			pass
		finally:
			if f:
				f.close()
			return config

	def hasPermissionForMenu(self, _menu):
		permissions = self.gatherPermissionForMenu(_menu)
		if not permissions:
			return True
		return self.hasAnyPermission(permissions)

	def gatherPermissionForMenu(self, _menu):
		permissions = []
		for perm in _menu.get('permissions', []):
			if perm not in permissions:
				permissions.append(perm)

		for item in _menu.get('itemList', []):
			itemPermissions = self.gatherPermissionForMenu(item)
			for itemPerm in itemPermissions:
				if itemPerm not in permissions:
					permissions.append(itemPerm)

		return permissions


	#   Common database routines.

	def getDbConnection(self):
		if not hasattr(self, 'dbConnection'):
			self.setDbConnection(None)
		return self.dbConnection
	def setDbConnection(self, _dbConnection): self.dbConnection = _dbConnection

	def getConnection(self):
		parms = self.identifyDatabase()
		if parms:
			self.setDbConnection(sqlUtils.SqlUtilities(parms))
			return self.getDbConnection()
		return None

	def closeConnection(self):
		if self.getDbConnection():
			self.getDbConnection().closeMpsConnection()
			self.setDbConnection(None)

	def identifyDatabase(self):
		profile = self.getProfile()
		if not profile:
			return None

		sitePrefs = profile.get('siteProfile',{}).get('sitePreferences',{})
		host = sitePrefs.get('dbhost', '')
		port = sitePrefs.get('dbport', '')
		dbname = sitePrefs.get('dbname', '')
		username = sitePrefs.get('dbusername', '')
		password = sitePrefs.get('dbpassword', '')
		return dbConnParms.DbConnectionParms(host=host, port=port, dbname=dbname, username=username, password=password)


	#   Common housekeeping routines.

	def getInitialPayload(self):
		payload = {}
		payload['site'] = self.request.headers.get('Site', '')
		payload['mpsid'] = self.getCookie('mpsid')
		payload['app'] = self.getEnvironment().getAppCode()
		return payload

	@mpsExceptionWrapper("Unable verify user credentials")
	def verifyRequest(self):

		#   Verify that an incoming request is from a bona-fide authenticated user.
		#   Site must be on the request header.
		#   Mpsid must be a specified cookie.

		payload = self.getInitialPayload()
		responseDict =  self.postToAuthSvc("/verify", payload, "Unable verify user credentials")
		self.setProfile(responseDict)
		return responseDict

	@mpsExceptionWrapper("Unable to get data from MPS Authorization Service")
	def postToAuthSvc(self, _uri, _unJsonifiedPayload, _optionalErrorMessage="Unable to get data from MPS Authorization Service"):

		#   Ask the Authorization Service for something.

		response = ""
		authserviceurl = self.getEnvironment().getAuthServiceUrl()

		http_client = tornado.httpclient.HTTPClient()
		try:
			jsonResponse = http_client.fetch(
				authserviceurl + _uri,
				method='POST',
				headers = {'Content-Type':'application/json'},
				body=tornado.escape.json_encode(_unJsonifiedPayload))
			response = tornado.escape.json_decode(jsonResponse.body)
		finally:
			http_client.close()

		#   A JSON data dictionary is always returned. Error conditions are indicated by the
		#   presence of either the 'error' or 'exception' keywords in the returned dictionary.
		if (response is None):
			raise excUtils.MPSValidationException(_optionalErrorMessage)
		if ('errorList' in response):
			message = response.get('errorList', '')
			if not message: message = _optionalErrorMessage
			raise excUtils.MPSValidationException(message)
		if ('error' in response):
			message = response.get('error', '')
			if not message: message = _optionalErrorMessage
			raise excUtils.MPSValidationException(message)
		if ('exception' in response):
			message = response.get('userMessage', '')
			if not message: message = _optionalErrorMessage
			raise excUtils.MPSValidationException(message)

		return response

	def getEnvironment(self):
		#   Must be overridden by subclasses.
		pass


	#   Common Exception Handling.

	def handleGetException(self, _exception, _logger, _optionalOverrideRedirect=None):

		#   Handle Exceptions from 'Get' routines.
		#   Message is extracted, logged, and (attempted to) be registered
		#   with the Authorization Service. The user is redirected back to
		#   the Login screen.

		message = ''
		logMessage = ''
		if _exception:
			if isinstance(_exception, excUtils.MPSValidationException):
				message = _exception.message
				_logger.warn(message)
			elif isinstance(_exception, excUtils.MPSException):
				message = _exception.getUserMessage()
				logMessage = _exception.getDetailMessage()
			else:
				message = str(_exception)
				logMessage = message

		if logMessage:
			_logger.exception(logMessage)

		try:
			msgDict = self.postToAuthSvc("/putMessage", { 'message': message})
			msgid = msgDict.get('msgid', '')
			if msgid:
				self.set_cookie('msgid', msgid)
		except Exception as e:
			pass

		self.clear_all_cookies()
		if _optionalOverrideRedirect:
			self.redirect(_optionalOverrideRedirect)

	def handlePostException(self, _exception, _logger):

		#   Handle Exceptions from 'Post' routines.
		#   Message is returned to the caller.

		if isinstance(_exception, excUtils.MPSValidationException):
			self.write(tornado.escape.json_encode({ 'errors': _exception.message }))
			_logger.warn(_exception.message)
			return

		if not (isinstance(_exception, excUtils.MPSException)):
			_exception = excUtils.wrapMPSException(_exception)

		_logger.exception(_exception.getDetailMessage())

		exceptionDict = dict()
		exceptionDict['exception'] = True
		exceptionDict['exceptionMessage'] = _exception.getDetailMessage()
		exceptionDict['userMessage'] = _exception.getUserMessage()
		self.write(tornado.escape.json_encode(exceptionDict))
