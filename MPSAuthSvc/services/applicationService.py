# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService

class ApplicationService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def getAllApplications(self):
		return self.getDbaseUtils().getAllApplications()

	def getApplicationForCode(self, _appCode):
		return self.getDbaseUtils().getApplicationForCode(_appCode)
