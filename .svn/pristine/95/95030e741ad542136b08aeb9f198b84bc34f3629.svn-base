# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import operator
import tornado.escape

import MPSCore.utilities.exceptionUtils as excUtils
import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.utilities.environmentUtils as envUtils

class SiteViewHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('siteView')

		siteList = self.postToAuthSvc("/sitelist", self.getInitialPayload(), "Unable to obtain Site data")
		self.localizeSiteListDates(siteList)

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['siteList'] = siteList
		context['disabled'] = "" if self.hasPermission('siteEdit') else "disabled"
		self.render("siteList.html", context=context, skin=context['skin'])


class SiteDetailHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['siteView','siteEdit'])

		#   Get the target site's profile.

		tgtSite = kwargs.get('targetSite', '')
		if not tgtSite:
			raise excUtils.MPSValidationException("Target site code required")
		tgtSiteProfile = self.postToAuthSvc("/siteprofile", { 'site': tgtSite }, 'Unable to locate target site')
		self.localizeOneSiteDates(tgtSiteProfile.get('sitePreferences', {}))

		appList = self.postToAuthSvc("/applist", self.getInitialPayload(), "Unable to obtain Application data")
		enabledAppCodeList = self._getEnabledAppCodes(tgtSiteProfile.get('siteApplications', []))
		self._identifyEnabledApps(appList, enabledAppCodeList)


		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = "edit"
		context['tgtSiteProfile'] = tgtSiteProfile
		context['disabled'] = "" if self.hasPermission('siteEdit') else "disabled"
		context['appList'] = appList
		context['prefsList'] = self._buildReadOnlyPrefsList(tgtSiteProfile.get('sitePreferences', {}))
		self.render("siteDetail.html", context=context, skin=context['skin'])

	def _getEnabledAppCodes(self, _appList):
		enabledAppCodeList = []
		for appDict in _appList:
			enabledAppCodeList.append(appDict['code'])
		return enabledAppCodeList

	def _identifyEnabledApps(self, _appList, _enabledAppCodeList):
		for appDict in _appList:
			appDict['checked'] = ""
			if appDict['code'] in _enabledAppCodeList:
				appDict['checked'] = "checked"

	def _buildReadOnlyPrefsList(self, _sitePreferences):
		ignoredList = [u'id',u'code',u'descr',u'active_start',u'active_end']
		sortedKeys = sorted(_sitePreferences, key=operator.itemgetter(0))
		resultList = []
		for key in sortedKeys:
			if key not in ignoredList:
				resultList.append((key,_sitePreferences[key]))
		return resultList


class SiteAddHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyPermission('siteEdit')

		appList = self.postToAuthSvc("/applist", self.getInitialPayload(), "Unable to obtain Application data")

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = "add"
		context['tgtSiteProfile'] = {}
		context['disabled'] = ""
		context['appList'] = appList
		self.render("siteDetail.html", context=context, skin=context['skin'])


class SiteSaveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('siteEdit')

		formData = tornado.escape.json_decode(self.request.body)
		isAdd = formData.get('mode', '') == 'add'
		code = formData.get('code', '')
		if isAdd:
			code = code.lower()

		payload = self.getInitialPayload()
		payload['code'] = code
		payload['descr'] = formData.get('descr', '')
		payload['active_start'] = formData.get('active_start', '')
		payload['active_end'] = formData.get('active_end', '')
		payload['timezone'] = self.getSiteTimezone()
		payload['apps'] = formData.get('apps', [])

		if isAdd:
			ignoredResponseDict = self.postToAuthSvc("/siteadd", payload, "Unable to add Site data")
		else:
			ignoredResponseDict = self.postToAuthSvc("/sitesave", payload, "Unable to save Site data")

		responseDict = self.getPostResponseDict("Site saved")
		responseDict['redirect'] = '/admin/site/detail/%s' % code
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/sites', SiteViewHandler),
	(r'/admin/site/detail/(?P<targetSite>[a-zA-Z0-9-]*)', SiteDetailHandler),
	(r'/admin/site/add', SiteAddHandler),
	(r'/admin/site/save', SiteSaveHandler),
]
