# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime
import logging
import MPSAuthSvc.caches.sessionCache as sessionCache
import MPSAuthSvc.utilities.environmentUtils as envUtils

gSessionWatcherTaskLogger = logging.getLogger(__name__)

#   Expire sessions that have been idle "too long".
#   This function is call periodically by the tornado web framework.

def sessionWatcherTask():
	global gSessionWatcherTaskLogger

	sessionCacheInstance = sessionCache.getSessionCache()
	cash = sessionCacheInstance.getCache()
	sessionKeys = cash.keys()
	if gSessionWatcherTaskLogger.isEnabledFor(logging.DEBUG):
		gSessionWatcherTaskLogger.debug("checking %i sessions" % len(sessionKeys))

	utcTimestampNow = datetime.datetime.utcnow()
	for mpsid in sessionKeys:
		sessionInfo = cash[mpsid]
		lastTimestamp = envUtils.getEnvironment().parseUTCDate(sessionInfo.getLastTimestamp())
		sessionIdleTimeoutMilliseconds = long(sessionInfo.getSessionIdleTimeoutMilliseconds())
		timeSessionWillExpire = lastTimestamp + datetime.timedelta(milliseconds=sessionIdleTimeoutMilliseconds)

		if utcTimestampNow > timeSessionWillExpire:
			sessionCacheInstance.invalidateSession(mpsid, isTimeout=True)
			if gSessionWatcherTaskLogger.isEnabledFor(logging.DEBUG):
				gSessionWatcherTaskLogger.debug("%s expired (%s/%s)" % (sessionInfo.getMpsid(), sessionInfo.getSite(), sessionInfo.getUsername()))
