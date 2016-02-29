# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.caches.siteCache as siteCash
import MPSAuthSvc.caches.userCache as userCash
import MPSAuthSvc.caches.sessionCache as sessionCash

class InvalidateSiteCacheHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._invalidateSiteCacheHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _invalidateSiteCacheHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		siteCash.getSiteCache().invalidateCache()
		self.write(tornado.escape.json_encode({}))


class InvalidateUserCacheHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._invalidateUserCacheHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _invalidateUserCacheHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({}))


class InvalidateSessionCacheHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._invalidateSessionCacheHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _invalidateSessionCacheHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		sessionCash.getSessionCache().invalidateCache()
		self.write(tornado.escape.json_encode({}))


class GetRandomSessionDataHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getRandomSessionDataHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getRandomSessionDataHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		credentials = tornado.escape.json_decode(self.request.body)
		mpsid = credentials.get('mpsid', None)
		key = credentials.get('key', None)

		sessionCacheInstance = sessionCash.getSessionCache()
		sessionInfo = sessionCacheInstance.getSessionInfo(mpsid)
		value = sessionInfo.getRandomData(key)
		self.write(tornado.escape.json_encode({'value':value}))


class PutRandomSessionDataHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._putRandomSessionDataHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _putRandomSessionDataHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		credentials = tornado.escape.json_decode(self.request.body)
		mpsid = credentials.get('mpsid', None)
		key = credentials.get('key', None)
		value = credentials.get('value', None)

		sessionCacheInstance = sessionCash.getSessionCache()
		sessionInfo = sessionCacheInstance.getSessionInfo(mpsid)
		sessionInfo.putRandomData(key, value)
		self.write(tornado.escape.json_encode({}))


class SetCandidateViewHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _postImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		credentials = tornado.escape.json_decode(self.request.body)
		mpsid = credentials.get('mpsid', None)
		value = credentials.get('value', 'false')
		username = credentials.get('username', '')

		sessionCacheInstance = sessionCash.getSessionCache()
		sessionInfo = sessionCacheInstance.getSessionInfo(mpsid)
		sessionInfo.setCandidateView(value)
		sessionInfo.setCandidateUsername(username)
		self.write(tornado.escape.json_encode({}))


#   All URL mappings for this module.
urlMappings = [
	(r'/invalidateSiteCache', InvalidateSiteCacheHandler),
	(r'/invalidateUserCache', InvalidateUserCacheHandler),
	(r'/invalidateSessionCache', InvalidateSessionCacheHandler),
	(r'/getRandomSessionData', GetRandomSessionDataHandler),
	(r'/putRandomSessionData', PutRandomSessionDataHandler),
	(r'/setCandidateView', SetCandidateViewHandler),
]
