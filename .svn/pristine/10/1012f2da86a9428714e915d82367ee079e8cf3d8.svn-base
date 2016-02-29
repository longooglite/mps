# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.caches.abstractCache
import MPSAuthSvc.caches.siteInfo

#   Global Site Cache.

class SiteCache(MPSAuthSvc.caches.abstractCache.AbstractCache):

	#   Public methods.

	def getSiteInfo(self, _site):
		if _site and _site in self._getCache():
			return self._getCache()[_site]
		return None

	def addSite(self, _site):
		if _site:
			siteInfo = MPSAuthSvc.caches.siteInfo.SiteInfo(_site)
			siteInfo.buildSite()
			self._getCache()[_site] = siteInfo

	def invalidateSite(self, _site):
		if _site and _site in self._getCache():
			del self._getCache()[_site]

	def profile(self, _site):
		siteInfo = self.getSiteInfo(_site)
		if siteInfo:
			return siteInfo.profile()
		return {}

	def profileDetail(self, _site):
		siteInfo = self.getSiteInfo(_site)
		if siteInfo:
			return siteInfo.profileDetail()
		return {}


#	Create a default global Site Cache instance,
#   and provide methods to retrieve it.

gSiteCache = SiteCache()

def getSiteCache():
	global gSiteCache
	return gSiteCache
