# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils
import MPSAuthSvc.utilities.environmentUtils as envUtils

class AbstractAuthenticator():

	def seeIfPasswordRequired(self, _siteProfile):
		sitePreferences = _siteProfile.get('sitePreferences', {})
		return stringUtils.interpretAsTrueFalse(sitePreferences.get('authpassreqd', 'Yes'))

	def generateUniqueId(self):
		return envUtils.getEnvironment().generateUniqueId()
