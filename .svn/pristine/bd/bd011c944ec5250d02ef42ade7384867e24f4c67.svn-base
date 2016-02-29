# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.utilities.environmentUtils as envUtils

class AbstractInvalidateCacheHandler(absHandler.AbstractHandler):

	def _postImpl(self, _cacheName, _permission, _postURL):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission(_permission)

		payload = self.getInitialPayload()
		responseDict =  self.postToAuthSvc(_postURL, payload, "Unable to invalidate %s cache" % _cacheName)
		self.write(tornado.escape.json_encode({ "message": "%s cache cleared" % _cacheName }))


class InvalidateSiteCacheHandler(AbstractInvalidateCacheHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postImpl("Site", "siteView", "/invalidateSiteCache")
		except Exception, e:
			self.handlePostException(e, self.logger)


class InvalidateUserCacheHandler(AbstractInvalidateCacheHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postImpl("User", "userView", "/invalidateUserCache")
		except Exception, e:
			self.handlePostException(e, self.logger)


class InvalidateSessionCacheHandler(AbstractInvalidateCacheHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postImpl("Session", "sessionView", "/invalidateSessionCache")
		except Exception, e:
			self.handlePostException(e, self.logger)


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/invalidateSiteCache', InvalidateSiteCacheHandler),
	(r'/admin/invalidateUserCache', InvalidateUserCacheHandler),
	(r'/admin/invalidateSessionCache', InvalidateSessionCacheHandler),
]
