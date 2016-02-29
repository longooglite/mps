# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSLogin.handlers.abstractHandler as absHandler


class ShibbolethHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.logger.exception(e.message)
			self.send_error(500)

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

		#   Shibboleth authentication.
		credentials = {}
		credentials['site'] = site
		credentials['username'] = self._getUsername(siteProfile)
		credentials['sessionid'] = self._getShibSessionId(siteProfile)
		credentials['identityprovider'] = self._getShibIdentifyProvider(siteProfile)
		responseDict = self.postToAuthSvcFromLogin("/authenticateshib", credentials, 'error')

		#   A JSON data dictionary is always returned. Error conditions are indicated by the
		#   presence of either the 'error' or 'exception' keywords in the returned dictionary.
		if ('error' in responseDict) or ('exception' in responseDict):
			self._urToast()
			return

		#   No mpsid returned ==> we're outta here.
		#   No shirt, no shoes, no service.
		mpsid = responseDict.get('mpsid', None)
		if not mpsid:
			self._urToast()
			return

		#   'userProfile' must be in the response.
		if 'userProfile' in responseDict:
			userProfile = responseDict['userProfile']

			#   'userApplications' gives us a list of the applications available
			#   for this user, in priority order. We go to the 1st one.
			applications = userProfile.get('userApplications', [])
			for app in applications:
				code = app.get('code', '')
				url = app.get('url', '')
				if code and url and code != 'LOGIN':
					self.clear_all_cookies()
					self.set_cookie("mpsid",mpsid)
					self.redirect(url)
					return

		self._urToast()

	def _getUsername(self, _siteProfile):
		sitePreferences = _siteProfile.get('sitePreferences', {})
		usernameKey = sitePreferences.get('shibusernamekey', 'Remote_user')
		rawUsername = self.request.headers.get(usernameKey, '')
		idx = rawUsername.find('@')
		if idx < 0:
			return rawUsername
		return rawUsername[0:idx]

	def _getShibSessionId(self, _siteProfile):
		sitePreferences = _siteProfile.get('sitePreferences', {})
		sessionKey = sitePreferences.get('shibsessionkey', 'Shib-Session-Id')
		return self.request.headers.get(sessionKey, '')

	def _getShibIdentifyProvider(self, _siteProfile):
		sitePreferences = _siteProfile.get('sitePreferences', {})
		sessionKey = sitePreferences.get('shibidentityproviderkey', 'Shib-Identity-Provider')
		return self.request.headers.get(sessionKey, '')

	def _urToast(self):
		self.redirect('/appt/visitor/unauthorized')


#   All URL mappings for this module.

urlMappings = [
	(r'/mps/shiblogin', ShibbolethHandler),
]
