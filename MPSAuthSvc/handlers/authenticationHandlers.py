# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json
import logging
import tornado.escape

import MPSAuthSvc.authenticators.mpsAuthenticator as mpsAuth
import MPSAuthSvc.authenticators.ldapAuthenticator as ldapAuth
import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.caches.sessionCache as sessionCache
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAuthSvc.services.authLogService as authLogSvc
import MPSAuthSvc.caches.userInfo as userNfo

class AbstractAuthenticateHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _getCredentials(self):
		credentialsJson = tornado.escape.json_decode(self.request.body)
		if type(credentialsJson) == dict:
			credentials = credentialsJson
		else:
			credentials = json.loads(credentialsJson)
		if 'community' not in credentials:
			credentials['community'] = 'default'
		return credentials

	def _validateSite(self, _site):
		if not _site:
			raise excUtils.MPSValidationException("Site identifier required")

		siteProfile = self.getOrCreateSite(_site)
		if not siteProfile:
			raise excUtils.MPSValidationException("Invalid Site identifier")
		sitePreferences = siteProfile.get('sitePreferences', {})
		if not self._siteIsActive(sitePreferences):
			raise excUtils.MPSValidationException("Site is inactive")
		return siteProfile, sitePreferences

	def _initialChecks(self, _functionName):

		#   Site is required.
		#   Site must be both valid and active.

		credentials = self._getCredentials()
		if self.logger.isEnabledFor(logging.DEBUG):
			credentialsCopy = credentials.copy()
			if 'password' in credentialsCopy:
				del credentialsCopy['password']
			self.logger.debug("%s %s" % (_functionName, credentialsCopy))

		site = credentials.get('site', '')
		siteProfile, sitePreferences = self._validateSite(site)

		#   Community is required.

		community = credentials.get('community', '').strip()
		if not community:
			raise excUtils.MPSValidationException("Community required")

		#   Username is required.

		username = credentials.get('username', '').strip()
		if not username:
			raise excUtils.MPSValidationException("Username required")

		return siteProfile, sitePreferences, credentials

	def _postHandlerImpl(self, _credentialsOnly=False):
		self.writePostResponseHeaders()

		#   Initial validations.

		func = 'checkcredentials' if _credentialsOnly else 'authenticate'
		siteProfile, sitePreferences, credentials = self._initialChecks(func)

		site = credentials.get('site', '')
		community = credentials.get('community', '').strip()
		username = credentials.get('username', '').strip()

		try:
			userProfile = {}
			try:
				userProfile = self.getOrCreateUser(site, community, username)
				username = userProfile.get('username', username)
			except Exception, e:
				pass
			if not _credentialsOnly:
				if not userProfile:
					raise excUtils.MPSValidationException("Invalid User identifier")
				if not userProfile.get('userPreferences', {}).get('active', False):
					raise excUtils.MPSValidationException("Invalid User identifier")

			#   Authenticate the given credentials against any external
			#   authentication service specified for this site. This either
			#   returns a new MPS Session identifier, or throws an error.

			mpsid = self._authenticate(siteProfile, userProfile, credentials)

		except Exception, e:
			authLogSvc.AuthLogService().logLoginUnsuccessful(site, community, username)
			raise excUtils.MPSValidationException("Incorrect Username or Password")

		#   User is authenticated. Return their unique session identifier,
		#      plus profiles of the site and user.

		response = {}
		response['mpsid'] = mpsid
		if not _credentialsOnly:
			response['siteProfile'] = siteProfile
			response['userProfile'] = userProfile
		self.write(tornado.escape.json_encode(response))

		#   Finally, remember their session identifier.

		if not _credentialsOnly:
			sessionIdleTimeoutMilliseconds = sitePreferences.get('sessionidletimeoutmilliseconds', '600000')
			sessionCache.getSessionCache().addSession(mpsid, site, community, username, sessionIdleTimeoutMilliseconds)

	def _authenticate(self, _siteProfile, _userProfile, _credentials):
		community = _credentials.get('community', '').strip()
		username = _credentials.get('username', '').strip()
		password = _credentials.get('password', '').strip()

		#   Use the User-specific authorization method, if specified.
		#   Otherwise, use the Site value.

		auth = _userProfile.get('userPreferences', {}).get('auth_override', '')
		if not auth:
			auth = _siteProfile.get('sitePreferences', {}).get('auth', '')

		if auth.lower() == 'mps':
			return mpsAuth.MpsAuthenticator().authenticate(_siteProfile, community, username, password)
		if auth.lower() == 'ldap':
			return ldapAuth.MpsAuthenticator().authenticate(_siteProfile, community, username, password)

		raise excUtils.MPSValidationException("Unknown authentication method")

class AuthenticateHandler(AbstractAuthenticateHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl(_credentialsOnly=False)
		except Exception, e:
			self.handleException(e, self.logger)

class CheckCredentialsHandler(AbstractAuthenticateHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl(_credentialsOnly=True)
		except Exception, e:
			self.handleException(e, self.logger)


class ShibbolethLoginHandler(AbstractAuthenticateHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._shibLoginHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _shibLoginHandlerImpl(self):
		self.writePostResponseHeaders()

		#   Initial validations.
		siteProfile, sitePreferences, credentials = self._initialChecks('authenticateshib')

		#   Shibboleth Session ID is required.
		sessionId = credentials.get('sessionid', '').strip()
		if not sessionId:
			raise excUtils.MPSValidationException("Shibboleth Session ID required")

		#   Shibboleth Identity Provider is required, and
		#   must match the configured value for the site.
		identityProvider = credentials.get('identityprovider', '').strip()
		if not identityProvider:
			raise excUtils.MPSValidationException("Shibboleth Identity Provider required")
		if identityProvider <> sitePreferences.get('shibidentityprovider', ''):
			raise excUtils.MPSValidationException("Invalid Shibboleth Identity Provider")

		#   Authentication.
		site = credentials.get('site', '')
		community = credentials.get('community', '').strip()
		username = credentials.get('username', '').strip()
		try:
			userProfile = {}
			try:
				userProfile = self.getOrCreateUser(site, community, username)
				username = userProfile.get('username', username)
			except Exception, e:
				pass

			if not userProfile:
				raise excUtils.MPSValidationException("Invalid User identifier")
			if not userProfile.get('userPreferences', {}).get('active', False):
				raise excUtils.MPSValidationException("Invalid User identifier")

			#   Get any User-specific authorization method, if specified.
			#   Otherwise, assume the Site value.
			#   The authorization method must be Shibboleth.

			auth = userProfile.get('userPreferences', {}).get('auth_override', '')
			if not auth:
				auth = siteProfile.get('sitePreferences', {}).get('auth', '')
			if auth.lower() != 'shib':
				raise excUtils.MPSValidationException("Unknown authentication method")

		except Exception, e:
			authLogSvc.AuthLogService().logLoginUnsuccessful(site, community, username)
			raise e

		#   User is authenticated. Return their unique session identifier,
		#   plus profiles of the site and user.
		#   Remember their session identifier.

		response = {}
		response['mpsid'] = sessionId
		response['siteProfile'] = siteProfile
		response['userProfile'] = userProfile
		self.write(tornado.escape.json_encode(response))

		sessionIdleTimeoutMilliseconds = sitePreferences.get('sessionidletimeoutmilliseconds', '600000')
		sessionCache.getSessionCache().addSession(sessionId, site, community, username, sessionIdleTimeoutMilliseconds)


class LDAPSearchHandler(AbstractAuthenticateHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._searchHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _searchHandlerImpl(self):

		#   Handler to perform an LDAP search for a specified username.
		#   The site should have LDAP as their authentication protocol,
		#   although this is not checked or enforced.
		#
		#   This handler is invoked from the legacy MARTA application,
		#   so an existing session for the client is not required or
		#   even validated. Future LDAP searching from other client
		#   applications should probably enforce the usual You Gotta
		#   Have A Session checks.

		#   Initial validations.

		self.writePostResponseHeaders()
		siteProfile, sitePreferences, credentials = self._initialChecks('ldapsearch')

		#   Perform requested search.

		community = credentials.get('community', '').strip()
		username = credentials.get('username', '').strip()
		response = ldapAuth.MpsAuthenticator().search(siteProfile, community, username)
		self.write(tornado.escape.json_encode(response))


class VerifyHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._verifyHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _verifyHandlerImpl(self):
		self.writePostResponseHeaders()

		#   MPS Client applications have only the unique MPS identifier.
		#   They must call this service to retrieve site and user information.
		#   Clients provide the unique MPS identifier, site code, and application code.

		credentials = tornado.escape.json_decode(self.request.body)
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("verify %s" % credentials)

		sessionInfo, siteProfile = self.checkCallersCredentials()
		site = credentials.get('site', None)
		app = credentials.get('app', None)

		sitePreferences = siteProfile.get('sitePreferences', {})
		if not self._siteIsActive(sitePreferences):
			raise excUtils.MPSValidationException("Site is inactive")

		#   Get the user profile for the user associated with the session.
		#   The user must be authorized for the indicated application.

		userProfile = self.getOrCreateUser(site, sessionInfo.getCommunity(), sessionInfo.getUsername())
		if not userProfile:
			raise excUtils.MPSValidationException("Invalid User identifier")
		if not self.userHasAccessToApp(userProfile, app):
			raise excUtils.MPSValidationException("Application prohibited")

		#   Return profiles of the site, user, and session.

		response = {}
		response['siteProfile'] = siteProfile
		response['userProfile'] = userProfile
		response['sessionProfile'] = sessionInfo.profile()
		self.checkForCandidateView(response)
		self.write(tornado.escape.json_encode(response))

	def userHasAccessToApp(self, _userProfile, _app):
		if _userProfile and _app:
			for appDict in _userProfile.get('userApplications', []):
				appCode = appDict.get('code', '')
				if appCode and appCode == _app:
					return True
		return False

	def checkForCandidateView(self, _response):
		isCandidateView = stringUtils.interpretAsTrueFalse(_response.get('sessionProfile',{}).get('isCandidateView', 'false'))
		if isCandidateView:
			candidateViewCommunity = _response.get('sessionProfile',{}).get('candidateCommunity', 'default')
			candidateViewUser = _response.get('sessionProfile',{}).get('candidateUsername', '')
			if candidateViewCommunity and candidateViewUser:
				siteProfile = _response.get('siteProfile',{})
				site = siteProfile.get('site','')
				userInfo = userNfo.UserInfo(site, candidateViewCommunity, candidateViewUser)
				userInfo.buildUser(candidateViewCommunity, candidateViewUser)
				_response['userProfile'] = userInfo.profile()


class LogoutHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._logoutHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _logoutHandlerImpl(self):
		self.writePostResponseHeaders()

		#   Make our best efforts to find and delete the given MPS identifier.
		#   No error is given if anything fails.

		credentials = tornado.escape.json_decode(self.request.body)
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("logout %s" % credentials)

		sessionCache.getSessionCache().invalidateSession(credentials.get('mpsid', None))

		#   Return an empty response, regardless of what happened.

		self.write(tornado.escape.json_encode({}))


#   All URL mappings for this module.
urlMappings = [
	(r'/authenticate', AuthenticateHandler),
	(r'/checkcredentials', CheckCredentialsHandler),
	(r'/authenticateshib', ShibbolethLoginHandler),
	(r'/ldapsearch', LDAPSearchHandler),
	(r'/verify', VerifyHandler),
	(r'/logout', LogoutHandler),
]
