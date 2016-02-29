# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import tornado.httpclient
import json

import MPSLogin.handlers.abstractHandler as absHandler
import MPSLogin.utilities.environmentUtils as envUtils


class AbstractLoginHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _getHandlerImpl(self, **kwargs):

		#   Check for maintenance mode.
		site = self.request.headers.get('Site', '')
		if self.isUnderMaintenance(site):
			context = {}
			context['additionalMessage'] = self.getMaintenanceModeMessage()
			self.render(self.resolveHTMLPath("maintenance.html"), context=context)
			return

		#   Get site profile.
		siteProfile = self.postToAuthSvcFromLogin("/siteprofile", { 'site': site }, 'raise')

		#   A cookie on the request indicates a message to be displayed on the Login page.
		initialMessage = ''
		msgid = self.getCookie('msgid')
		if msgid:
			messageDict = self.postToAuthSvcFromLogin("/getMessage", { 'msgid': msgid }, 'ignore')
			initialMessage = messageDict.get('message', '')

		#   Prompt Community if there are more than one.
		promptCommunity = False
		communityList = siteProfile.get('siteCommunities', [])
		if len(communityList) > 1:
			if not kwargs.get('includeDefaultCommunity', False):
				communityList = self.removeDefaultCommunity(communityList)
			if len(communityList) > 1:
				promptCommunity = True

		#   Render the Login page.
		sitePreferences = {}
		if siteProfile:
			sitePreferences = siteProfile.get('sitePreferences', {})
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['siteInfo'] = sitePreferences
		context['skin'] = sitePreferences.get('skin', 'default')
		context['errormessage'] = initialMessage
		context['loginURL'] = kwargs.get('loginURL', '/mps/login')
		context['logincobrand'] = sitePreferences.get('descr','')

		if 'guid' in kwargs:
			context['guid'] = kwargs.get('guid', '')
		if 'jobactionid' in kwargs:
			context['jobactionid'] = kwargs.get('jobactionid', '')
		if promptCommunity:
			context['promptCommunity'] = True
			context['communityList'] = communityList

		if context['skin'] == 'redux':
			self.render(self.resolveHTMLPath("login_redux.html"), context=context, skin=context['skin'])
		else:
			self.render(self.resolveHTMLPath("login.html"), context=context, skin=context['skin'])

		#   Whack any existing cookies.
		self.clear_all_cookies()

	def _postHandlerImpl(self):

		#   Authenticate using the given credentials:
		#   site, community, username, and password.
		responseDict = self.postToAuthSvcFromLogin("/authenticate", self.request.body, 'error')

		#   A JSON data dictionary is always returned. Error conditions are indicated by the
		#   presence of either the 'error' or 'exception' keywords in the returned dictionary.
		if 'error' in responseDict:
			self.doError(responseDict['error'])
			return

		if 'exception' in responseDict:
			userMessage = responseDict.get('userMessage', '')
			exceptionMessage = responseDict.get('exceptionMessage', '')
			if userMessage:
				if exceptionMessage:
					userMessage = userMessage + '<br/>' + exceptionMessage
			else:
				userMessage = exceptionMessage
			self.doError(userMessage)
			return

		#   No mpsid returned ==> we're outta here.
		#   No shirt, no shoes, no service.
		mpsid = responseDict.get('mpsid', None)
		if not mpsid:
			self.doError('User not found')
			return

		#   'userProfile' must be in the response.
		if 'userProfile' in responseDict:
			userProfile = responseDict['userProfile']

			#   If a guid or jobactionid is present on the posted form, save it in the session's data area.
			formData = json.loads(self.request.body)
			if ('guid' in formData) or ('jobactionid' in formData):
				payload = {}
				payload['site'] = self.request.headers.get('Site', '')
				payload['mpsid'] = mpsid
				payload['app'] = envUtils.getEnvironment().getAppCode()
				if 'guid' in formData:
					payload['key'] = 'guid'
					payload['value'] = formData['guid']
				else:
					payload['key'] = 'jobactionid'
					payload['value'] = formData['jobactionid']
				response = self.postToAuthSvcFromLogin("/putRandomSessionData", payload, 'error')

			#   'userApplications' gives us a list of the applications available
			#   for this user, in priority order. We go to the 1st one.
			applications = userProfile.get('userApplications', [])
			for app in applications:
				code = app.get('code', '')
				url = app.get('url', '')
				if code and url and code != 'LOGIN':
					self.clear_all_cookies()
					self.set_cookie("mpsid",mpsid)
					self.doRedirect(url)
					return

		self.doError('No authorized application found')

	def removeDefaultCommunity(self, _communityList):
		newList = []
		for communityDict in _communityList:
			if communityDict.get('code', '') != 'default':
				newList.append(communityDict)
		return newList

	def doError(self, _message):
		self.writeResponseHeaders()
		self.write(tornado.escape.json_encode({'error': _message}))

	def doRedirect(self, _url):
		self.writeResponseHeaders()
		self.write(tornado.escape.json_encode({'redirect': _url}))


#   LoginHandler is the 'regular' login handler.

class LoginHandler(AbstractLoginHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			kwargs['loginURL'] = '/mps/login'
			kwargs['includeDefaultCommunity'] = False
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.logger.exception(e.message)
			self.send_error(500)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.logger.exception(e.message)
			self.doError(e.message)


#   MPSLoginHandler forces display of the 'regular' login screen.
#   It's useful for sites using Shibboleth, as it permits us to
#   bypass the shibboleth processing and log on as mpsadmin.

class MPSLoginHandler(AbstractLoginHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			kwargs['loginURL'] = '/mps/mpslogin'
			kwargs['includeDefaultCommunity'] = True
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.logger.exception(e.message)
			self.send_error(500)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.logger.exception(e.message)
			self.doError(e.message)


class ToastHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	#   Render the "You are no loner a valid session" screen.

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):

		#   A cookie on the request indicates a message to be displayed on the Login page.
		initialMessage = ''
		msgid = self.getCookie('msgid')
		if msgid:
			messageDict = self.postToAuthSvcFromLogin("/getMessage", { 'msgid': msgid }, 'ignore')
			initialMessage = messageDict.get('message', '')

		#   Try to log out, no biggie if we can't.
		try:
			payload = { 'mpsid': self.getCookie('mpsid') }
			self.clear_cookie('mpsid')
			self.postToAuthSvcFromLogin("/logout", payload, 'ignore')
		except Exception:
			pass

		#   Render the Toast page, no questions asked.
		self.setProfile({})
		context = self.getInitialTemplateContext(self.getEnvironment())
		context['errormessage'] = initialMessage
		context['loginURL'] = '/mps/login'
		self.render("toast.html", context=context, skin=context['skin'])


#   All URL mappings for this module.

urlMappings = [
	(r'/mps/login/(?P<guid>[a-f0-9]{32,32})', LoginHandler),
	(r'/mps/login/ja/(?P<jobactionid>[0-9]{1,9})', LoginHandler),
	(r'/mps/login', LoginHandler),
	(r'/mps/mpslogin', MPSLoginHandler),
	(r'/mps/toast', ToastHandler),
]
