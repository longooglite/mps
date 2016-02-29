# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService

class PermissionService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def getPermissionsForSite(self, site):
		return self.getDbaseUtils().getPermissionsForSite(site)
