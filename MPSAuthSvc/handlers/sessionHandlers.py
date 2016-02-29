# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.caches.sessionCache as sessionCash

class GetSessionsHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		messageDict = tornado.escape.json_decode(self.request.body)
		targetSite = messageDict.get('targetSite', '')
		allCurrentSessions = sessionCash.getSessionCache().getCache()
		allExpiredSessions = sessionCash.getSessionCache().getExpiredSessionList()

		currentSessionList = []
		for sessionInfo in allCurrentSessions.values():
			if not targetSite or \
				sessionInfo.getSite() == targetSite:
				currentSessionList.append(sessionInfo.profile())

		expiredSessionList = []
		for sessionInfo in allExpiredSessions:
			if not targetSite or \
				sessionInfo.getSite() == targetSite:
				expiredSessionList.append(sessionInfo.profile())

		self.write(tornado.escape.json_encode({ 'sessionList': currentSessionList, 'expiredSessionList': expiredSessionList }))


class KillSessionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		messageDict = tornado.escape.json_decode(self.request.body)
		sessionId = messageDict.get('sessionId', '')
		sessionCash.getSessionCache().invalidateSession(sessionId)
		self.write(tornado.escape.json_encode({ 'message': "Session terminated" }))


#   All URL mappings for this module.
urlMappings = [
	(r'/sessionlist', GetSessionsHandler),
	(r'/sessionkill', KillSessionHandler),
]
