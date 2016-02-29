# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService
import MPSAuthSvc.services.applicationService as applicationSvc

class SiteService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def getAllSites(self):
		return self.getDbaseUtils().getAllSites()

	def getSite(self, _site):
		return self.getDbaseUtils().getSite(_site)

	def getSiteCommunities(self, _site):
		return self.getDbaseUtils().getSiteCommunities(_site)

	def getSitePreferences(self, _site):
		return self.getDbaseUtils().getSitePreferences(_site)

	def getOneSitePreference(self, _id):
		return self.getDbaseUtils().getOneSitePreference(_id)

	def getSiteApplications(self, _site):
		return self.getDbaseUtils().getSiteApplications(_site)

	def getSiteRoles(self, _site):
		return self.getDbaseUtils().getSiteRoles(_site)

	def getSitePreferencePrefixes(self):
		return self.getDbaseUtils().getSitePreferencePrefixes()

	def addSite(self, _siteDict):
		self._persistSite(_siteDict, True)

	def saveSite(self, _siteDict):
		self._persistSite(_siteDict, False)

	def _persistSite(self, _siteDict, _isAdd):
		try:
			#   Update site table data
			if _isAdd:
				self.getDbaseUtils().addSite(_siteDict, _shouldCloseConnection=False, _doCommit=False)
			else:
				self.getDbaseUtils().saveSite(_siteDict, _shouldCloseConnection=False, _doCommit=False)

			#   Update list of allowed applications
			if 'apps' in _siteDict:
				siteCode = _siteDict.get('code', '')
				existingSiteAppDicts = self.getDbaseUtils().getSiteApplications(siteCode, _shouldCloseConnection=False)
				existingSiteAppCodes = []
				for each in existingSiteAppDicts:
					existingSiteAppCodes.append(each['code'])

				appSvc = applicationSvc.ApplicationService()
				allApps = appSvc.getAllApplications()
				desiredApps = _siteDict.get('apps', [])
				for appDict in allApps:
					thisAppCode = appDict.get('code','')
					if thisAppCode:
						if thisAppCode in desiredApps:
							#   Add this Application if not already associated with the Site
							if thisAppCode not in existingSiteAppCodes:
								self.getDbaseUtils().associateSiteWithApplication(siteCode, thisAppCode, _shouldCloseConnection=False, _doCommit=False)
						else:
							#   Remove this Application's association with the Site
							#   Remove this Application's association with the Site's Users
							self.getDbaseUtils().disassociateSiteApplication(siteCode, thisAppCode, _shouldCloseConnection=False, _doCommit=False)
							self.getDbaseUtils().disassociateSiteApplicationUsers(siteCode, thisAppCode, _shouldCloseConnection=False, _doCommit=False)

			#   Commit transaction
			self.getDbaseUtils().performCommit()
			self.getDbaseUtils().closeConnection()

		except Exception, e:
			try: self.getDbaseUtils().performRollback()
			except Exception, e1: pass
			raise e

	def addSitePref(self, _sitePrefDict):
		self.getDbaseUtils().addSitePref(_sitePrefDict)

	def saveSitePref(self, _sitePrefDict):
		self.getDbaseUtils().saveSitePref(_sitePrefDict)

	def deleteSitePref(self, _sitePrefDict):
		self.getDbaseUtils().deleteSitePref(_sitePrefDict)
