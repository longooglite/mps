# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils

kLogin = "LOGIN"
kLogout = "LOGOUT"
kLoginFail = "FAIL"


class AuthLogService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def logLogin(self, _site, _community, _username, _mpsid):
		now = coreEnvUtils.CoreEnvironment().formatUTCDate()
		return self.getDbaseUtils().logLogin(now, _site, _community, _username, _mpsid, kLogin)

	def logLogout(self, _mpsid):
		now = coreEnvUtils.CoreEnvironment().formatUTCDate()
		return self.getDbaseUtils().logLogout(now, _mpsid, kLogout)

	def logLoginUnsuccessful(self, _site, _community, _username):
		now = coreEnvUtils.CoreEnvironment().formatUTCDate()
		return self.getDbaseUtils().logLoginUnsuccessful(now, _site, _community, _username, kLoginFail)
