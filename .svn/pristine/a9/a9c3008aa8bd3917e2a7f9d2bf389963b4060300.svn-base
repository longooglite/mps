# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.caches.abstractCache
import MPSAuthSvc.caches.sessionInfo
import MPSAuthSvc.services.authLogService as authLogSvc

#   Global Session Cache.

class SessionCache(MPSAuthSvc.caches.abstractCache.AbstractCache):

	def __init__(self):
		MPSAuthSvc.caches.abstractCache.AbstractCache.__init__(self)
		self.expiredSessionList = []


	#   Public methods.

	def getCache(self): return self._getCache()
	def getExpiredSessionList(self): return self.expiredSessionList

	def getSessionInfo(self, _mpsid):
		if _mpsid and _mpsid in self._getCache():
			return self._getCache()[_mpsid]
		return None

	def addSession(self, _mpsid, _site, _community, _username, _sessionIdleTimeoutMilliseconds):
		if _mpsid:
			sessionInfo = MPSAuthSvc.caches.sessionInfo.SessionInfo(_mpsid, _site, _community, _username, _sessionIdleTimeoutMilliseconds)
			self._getCache()[_mpsid] = sessionInfo
			authLogSvc.AuthLogService().logLogin(_site, _community, _username,_mpsid)

	def invalidateSession(self, _mpsid, isTimeout=False):
		if _mpsid and _mpsid in self._getCache():
			self.addExpiredSession(self._getCache()[_mpsid], isTimeout)
			del self._getCache()[_mpsid]
			authLogSvc.AuthLogService().logLogout(_mpsid)

	def addExpiredSession(self, _sessionInfo, isTimeout=False):
		if len(self.getExpiredSessionList()) >= 100:
			del self.getExpiredSessionList()[0]
		_sessionInfo.setTimeout(isTimeout)
		self.getExpiredSessionList().append(_sessionInfo)

	def updateLastTimestamp(self, _mpsid):
		sessionInfo = self.getSessionInfo(_mpsid)
		if sessionInfo:
			sessionInfo.updateLastTimestamp()

	def profile(self, _mpsid):
		sessionInfo = self.getSessionInfo(_mpsid)
		if sessionInfo:
			return sessionInfo.profile()
		return {}


#	Create a default global Session Cache instance,
#   and provide methods to retrieve it.

gSessionCache = SessionCache()

def getSessionCache():
	global gSessionCache
	return gSessionCache
