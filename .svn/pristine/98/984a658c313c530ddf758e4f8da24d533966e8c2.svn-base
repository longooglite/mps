# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.siteService as siteSvc
import MPSAuthSvc.services.roleService as roleSvc

#   Site Info.

class SiteInfo():

	def __init__(self, _site):
		self.setSite(_site)
		self.initSiteCommunities()
		self.initSitePreferences()
		self.initSitePreferencesDetailList()
		self.initSiteApplications()
		self.initSiteRoles()

	def getSite(self): return self.site
	def setSite(self, _site): self.site = _site

	def getSiteCommunities(self): return self.siteCommunities
	def setSiteCommunities(self, _siteCommunities): self.siteCommunities = _siteCommunities
	def initSiteCommunities(self): self.setSiteCommunities([])

	def getSitePreferences(self): return self.sitePreferences
	def setSitePreferences(self, _sitePreferences): self.sitePreferences = _sitePreferences
	def initSitePreferences(self): self.setSitePreferences({})

	def getSitePreferencesDetailList(self): return self.sitePreferencesDetailList
	def setSitePreferencesDetailList(self, _sitePreferencesDetailList): self.sitePreferencesDetailList = _sitePreferencesDetailList
	def initSitePreferencesDetailList(self): self.setSitePreferencesDetailList([])

	def getSiteApplications(self): return self.siteApplications
	def setSiteApplications(self, _siteApplications): self.siteApplications = _siteApplications
	def initSiteApplications(self): self.setSiteApplications([])

	def getSiteRoles(self): return self.siteRoles
	def setSiteRoles(self, _siteRoles): self.siteRoles = _siteRoles
	def initSiteRoles(self): self.setSiteRoles([])

	def buildSite(self):
		siteService = siteSvc.SiteService()
		roleService = roleSvc.RoleService(siteService.getDbaseUtils())

		commnityList = siteService.getSiteCommunities(self.getSite())

		prefDict = siteService.getSite(self.getSite())
		prefDetailList = []

		thisPrefList = siteService.getSitePreferences('')
		prefDetailList.extend(thisPrefList)
		self._applyPreferences(prefDict, thisPrefList)

		splits = self.getSite().split('.')
		splits.reverse()
		key = ''
		for item in splits:
			if key:
				key = item + '.' + key
			else:
				key = item
			thisPrefList = siteService.getSitePreferences(key)
			prefDetailList.extend(thisPrefList)
			self._applyPreferences(prefDict, thisPrefList)

		roleList = siteService.getSiteRoles(self.getSite())
		for roleDict in roleList:
			roleDict['permissionList'] = roleService.getRolePermissions(self.getSite(), roleDict['code'])

		appList = siteService.getSiteApplications(self.getSite())
		for item in appList:
			item['url'] = item['url'].replace('${site}', self.getSite())

		self.setSiteCommunities(commnityList)
		self.setSitePreferences(prefDict)
		self.setSitePreferencesDetailList(prefDetailList)
		self.setSiteRoles(roleList)
		self.setSiteApplications(appList)

	def _applyPreferences(self, _prefDict, _prefList):
		for pref in _prefList:
			key = pref['code'].lower()
			_prefDict[key] = pref['value']

	def profile(self):
		myProfile = dict()
		myProfile['site'] = self.getSite()
		myProfile['siteCommunities'] = self.getSiteCommunities()
		myProfile['sitePreferences'] = self.getSitePreferences()
		myProfile['siteApplications'] = self.getSiteApplications()
		return myProfile

	def profileDetail(self):
		myProfile = self.profile()
		myProfile['sitePreferencesDetailList'] = self.getSitePreferencesDetailList()
		myProfile['siteRoles'] = self.getSiteRoles()
		return myProfile
