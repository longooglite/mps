# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.caches.abstractCache
import MPSAuthSvc.caches.userInfo

#   Global User Cache.

kCacheKeyDelimiter = "|||"

class UserCache(MPSAuthSvc.caches.abstractCache.AbstractCache):

	#   Public methods.

	def getUserInfo(self, _site, _community, _username):
		if _site and _username:
			cacheKey = self._getCacheKey(_site, _community, _username)
			if cacheKey in self._getCache():
				return self._getCache()[cacheKey]
		return None

	def addUser(self, _site, _community, _username):
		if _site and _username:
			userInfo = MPSAuthSvc.caches.userInfo.UserInfo(_site, _community, _username)
			userInfo.buildUser()
			self._getCache()[self._getCacheKey(_site, _community, _username)] = userInfo

	def invalidateUser(self, _site, _community, _username):
		if _site and _username:
			cacheKey = self._getCacheKey(_site, _community, _username)
			if cacheKey in self._getCache():
				del self._getCache()[cacheKey]

	def profile(self, _site, _community, _username):
		userInfo = self.getUserInfo(_site, _community, _username)
		if userInfo:
			return userInfo.profile()
		return {}

	def _getCacheKey(self, _site, _community, _username):
		return _site + kCacheKeyDelimiter + _community + kCacheKeyDelimiter + _username


#	Create a default global User Cache instance,
#   and provide methods to retrieve it.

gUserCache = UserCache()

def getUserCache():
	global gUserCache
	return gUserCache
