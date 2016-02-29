# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.utilities.environmentUtils as envUtils

#   Session Info.

class SessionInfo():

	def __init__(self, _mpsid, _site, _community, _username, _sessionIdleTimeoutMilliseconds):
		self.setMpsid(_mpsid)
		self.setSite(_site)
		self.setCommunity(_community)
		self.setUsername(_username)
		self.updateLastTimestamp()
		self.setOriginTimestamp(self.getLastTimestamp())
		self.setSessionIdleTimeoutMilliseconds(_sessionIdleTimeoutMilliseconds)
		self.setRandomDataCache({})
		self.setTimeout(False)
		self.setCandidateView('false')
		self.setCandidateUsername('')

	def getMpsid(self): return self.mpsid
	def setMpsid(self, _mpsid): self.mpsid = _mpsid
	
	def getCommunity(self): return self.community
	def setCommunity(self, _community): self.community = _community

	def getSite(self): return self.site
	def setSite(self, _site): self.site = _site

	def getUsername(self): return self.username
	def setUsername(self, _username): self.username = _username

	def getSessionIdleTimeoutMilliseconds(self): return self.sessionIdleTimeoutMilliseconds
	def setSessionIdleTimeoutMilliseconds(self, _milliseconds): self.sessionIdleTimeoutMilliseconds = _milliseconds

	def getOriginTimestamp(self): return self.originTimestamp
	def setOriginTimestamp(self, _originTimestamp): self.originTimestamp = _originTimestamp

	def getLastTimestamp(self): return self.lastTimestamp
	def setLastTimestamp(self, _lastTimestamp): self.lastTimestamp = _lastTimestamp
	def updateLastTimestamp(self):
		self.setLastTimestamp(envUtils.getEnvironment().formatUTCDate())

	def getRandomDataCache(self): return self.randomDataCache
	def setRandomDataCache(self, _randomDataCache): self.randomDataCache = _randomDataCache

	def getRandomData(self, _key): return self.getRandomDataCache().get(_key, None) if _key else None
	def putRandomData(self, _key, _value):
		if _key: self.getRandomDataCache()[_key] = _value

	def getTimeout(self): return self.timeout
	def setTimeout(self, _timeout): self.timeout = _timeout

	def getCandidateView(self): return self.candidateView
	def setCandidateView(self, _candidateView): self.candidateView = _candidateView

	def getCandidateUsername(self): return self.candidateUsername
	def setCandidateUsername(self, _candidateUsername): self.candidateUsername = _candidateUsername

	def profile(self):
		myProfile = dict()
		myProfile['mpsid'] = self.getMpsid()
		myProfile['site'] = self.getSite()
		myProfile['community'] = self.getCommunity()
		myProfile['username'] = self.getUsername()
		myProfile['originTimestamp'] = self.getOriginTimestamp()
		myProfile['lastTimestamp'] = self.getLastTimestamp()
		myProfile['sessionIdleTimeoutMilliseconds'] = self.getSessionIdleTimeoutMilliseconds()
		myProfile['isTimeout'] = self.getTimeout()
		myProfile['isCandidateView'] = self.getCandidateView()
		myProfile['candidateUsername'] = self.getCandidateUsername()
		return myProfile
