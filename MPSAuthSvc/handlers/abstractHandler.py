# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import tornado.web

import MPSAuthSvc.caches.siteCache as siteCache
import MPSAuthSvc.caches.userCache as userCache
import MPSAuthSvc.caches.sessionCache as sessionCache
import MPSAuthSvc.services.siteService as siteSvc
import MPSAuthSvc.services.userService as userSvc
import MPSAuthSvc.utilities.environmentUtils as envUtils
import MPSAuthSvc.utilities.messageCache as msgCache
import MPSCore.utilities.exceptionUtils as excUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

class AbstractHandler(tornado.web.RequestHandler):
	logger = logging.getLogger(__name__)

	def handleException(self, _exception, _logger):
		if isinstance(_exception, excUtils.MPSValidationException):
			message = _exception.message
			_logger.warn(message)
			msgid = msgCache.getMessageCache().addMessage(message)

			key = 'error'
			if type(message) == list:
				key = 'errorList'
			self.write(tornado.escape.json_encode({ key: message, 'msgid': msgid }))
			return

		if not (isinstance(_exception, excUtils.MPSException)):
			_exception = excUtils.wrapMPSException(_exception)

		message = _exception.getUserMessage()
		logMessage = _exception.getDetailMessage()
		_logger.exception(logMessage)

		exceptionDict = dict()
		exceptionDict['exception'] = True
		exceptionDict['exceptionMessage'] = logMessage
		exceptionDict['userMessage'] = message
		msgid = msgCache.getMessageCache().addMessage(message)
		exceptionDict['msgid'] = msgid
		self.write(tornado.escape.json_encode(exceptionDict))

	def writePostResponseHeaders(self):
		self.set_header('Content-Type','application/json')

	def getOrCreateSite(self, _site):
		siteProfile = siteCache.getSiteCache().profile(_site)
		if siteProfile:
			return siteProfile

		siteInfo = siteSvc.SiteService().getSite(_site)
		if not siteInfo:
			return None

		siteCache.getSiteCache().addSite(_site)
		return siteCache.getSiteCache().profile(_site)

	def _siteIsActive(self, _siteDict, _utcTimeNow=None):
		active_start = _siteDict.get('active_start', None)
		active_end = _siteDict.get('active_end', None)
		utcTimeNow = _utcTimeNow
		if not utcTimeNow:
			utcTimeNow = envUtils.getEnvironment().formatUTCDate()

		if active_start and utcTimeNow < active_start: return False
		if active_end and utcTimeNow > active_end: return False
		return True

	def getOrCreateUser(self, _site, _community, _username):
		userProfile = userCache.getUserCache().profile(_site, _community, _username)
		if userProfile:
			return userProfile

		userInfo = userSvc.UserService().getUser(_site, _community, _username)
		if not userInfo:
			return None

		username = userInfo.get('username', _username)
		userCache.getUserCache().addUser(_site, _community, username)
		return userCache.getUserCache().profile(_site, _community, username)

	def getCookie(self, _cookie):
		morsel = self.request.cookies.get(_cookie, None)
		if morsel:
			return morsel.value
		return None

	@mpsExceptionWrapper("Invalid Site identifier")
	def checkCallersCredentials(self):

		#   Once authenticated, MPS Client applications have only the unique MPS identifier.
		#   Clients provide the unique MPS identifier, site code, and application code.
		#   This routine validates that those credentials are authentic.

		credentials = tornado.escape.json_decode(self.request.body)
		site = credentials.get('site', None)
		mpsid = credentials.get('mpsid', None)
		app = credentials.get('app', None)
		if not mpsid or not site or not app:
			raise excUtils.MPSValidationException("Credentials required")

		#   Must find the indicated session.
		#   The site associated with the session must match they site provided by the Client app.

		sessionCacheInstance = sessionCache.getSessionCache()
		sessionInfo = sessionCacheInstance.getSessionInfo(mpsid)
		if not sessionInfo:
			raise excUtils.MPSValidationException("This session has been idle. As a safety measure you have been logged out.")

		sessionSite = sessionInfo.getSite()
		if site != sessionSite:
			raise excUtils.MPSValidationException("Invalid Session identifier")

		siteProfile = self.getOrCreateSite(site)
		if not siteProfile:
			raise excUtils.MPSValidationException("Invalid Site identifier")

		#   Return a tuple of:
		#       sessionInfo
		#       siteProfile

		sessionInfo.updateLastTimestamp()
		return (sessionInfo, siteProfile)

	def validateStringRequired(self, _srcDict, _srcKey, _errorMessage):
		value = _srcDict.get(_srcKey, '')
		if not value:
			raise excUtils.MPSValidationException(_errorMessage)

	def validateTimestampOptional(self, _srcDict, _srcKey, _errorMessage):
		value = _srcDict.get(_srcKey, '')
		if value:
			try:
				envUtils.getEnvironment().parseUTCDate(value)
			except Exception:
				raise excUtils.MPSValidationException(_errorMessage)

	def checkStringRequired(self, _srcDict, _srcKey, _errorMessage):
		value = _srcDict.get(_srcKey, '')
		if not value:
			return {'code':_srcKey, 'message': _errorMessage }
		return None
