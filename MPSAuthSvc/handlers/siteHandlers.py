# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.caches.siteCache as siteCash
import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.services.siteService as siteSvc
import MPSAuthSvc.utilities.environmentUtils as envUtils
import MPSCore.utilities.exceptionUtils as excUtils

class SiteProfileHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._siteProfileHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _siteProfileHandlerImpl(self):

		#   Do not need an authenticated session to use this method.
		#   Used to return site information to the MPS Login application.

		self.writePostResponseHeaders()
		inParms = tornado.escape.json_decode(self.request.body)
		site = inParms.get('site', None)
		if not site:
			raise excUtils.MPSValidationException("Site identifier required")

		profile = self.getOrCreateSite(site)
		if not profile:
			raise excUtils.MPSValidationException("Invalid Site identifier")

		self.write(tornado.escape.json_encode(profile))

class SiteProfileDetailHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._siteProfileDetailHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _siteProfileDetailHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		site = inParms.get('profileSite', None)
		if site == 'auth':
			detailProfileDetail = self._getSpecialProfileDetail('auth', 'MPS Authorization')
		elif site == 'autofill':
			detailProfileDetail = self._getSpecialProfileDetail('autofill', 'MPS Autofill', _dbname='autofill')
		else:
			ignoredProfile = self.getOrCreateSite(site)
			detailProfileDetail = siteCash.getSiteCache().profileDetail(site)

		self.write(tornado.escape.json_encode(detailProfileDetail))

	def _getSpecialProfileDetail(self, _code, _descr, _dbname=None):
		env = envUtils.getEnvironment()
		dbConnectionParms = env.getDbConnectionParms()

		prefsDict = {}
		prefsDict['code'] = _code
		prefsDict['descr'] = _descr
		prefsDict['dbhost'] = dbConnectionParms.getHost()
		prefsDict['dbport'] = dbConnectionParms.getPort()
		prefsDict['dbname'] = _dbname if _dbname else dbConnectionParms.getDbname()
		prefsDict['dbusername'] = dbConnectionParms.getUsername()
		prefsDict['dbpassword'] = dbConnectionParms.getPassword()

		profile = {}
		profile['site'] = _code
		profile['sitePreferences'] = prefsDict
		return profile

class SiteProfileDetailBypassHandler(SiteProfileDetailHandler):
	logger = logging.getLogger(__name__)

	def _siteProfileDetailHandlerImpl(self):
		self.writePostResponseHeaders()

		inParms = tornado.escape.json_decode(self.request.body)
		site = inParms.get('profileSite', None)
		ignoredProfile = self.getOrCreateSite(site)
		detailProfileDetail = siteCash.getSiteCache().profileDetail(site)
		self.write(tornado.escape.json_encode(detailProfileDetail))

class SiteListHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._siteListHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _siteListHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		siteList = siteSvc.SiteService().getAllSites()
		self.write(tornado.escape.json_encode(siteList))

class SiteListBypassHandler(SiteListHandler):
	logger = logging.getLogger(__name__)

	def _siteListHandlerImpl(self):
		self.writePostResponseHeaders()
		siteList = siteSvc.SiteService().getAllSites()
		self.write(tornado.escape.json_encode(siteList))

class SitePrefixListHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._sitePrefPrefixListHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _sitePrefPrefixListHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		prefixList = siteSvc.SiteService().getSitePreferencePrefixes()
		self.write(tornado.escape.json_encode(prefixList))

class SitePrefixDetailHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._sitePrefPrefixDetailHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _sitePrefPrefixDetailHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		prefix = inParms.get('prefix', None)
		prefList = siteSvc.SiteService().getSitePreferences(prefix)
		self.write(tornado.escape.json_encode(prefList))

class SitePreferenceDetailHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._sitePreferenceDetailHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _sitePreferenceDetailHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		id = inParms.get('id', None)
		prefList = siteSvc.SiteService().getOneSitePreference(id)
		self.write(tornado.escape.json_encode(prefList))


class AbstractSiteSaveHandler(absHandler.AbstractHandler):
	def _siteValidation(self, _isAdd):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		self.validateStringRequired(inParms, 'code', "Site code required")
		self.validateStringRequired(inParms, 'descr', "Site description required")
		self.validateTimestampOptional(inParms, 'active_start', "Invalid start date")
		self.validateTimestampOptional(inParms, 'active_end', "Invalid end date")

		code = inParms.get('code', None)
		if _isAdd:
			code = code.lower()
		else:
			profile = self.getOrCreateSite(code)
			if not profile:
				raise excUtils.MPSValidationException("Invalid Site code identifier")

		active_start = inParms.get('active_start', None)
		active_end = inParms.get('active_end', None)
		timezone = inParms.get('timezone', 'US/Eastern')
		if active_start: active_start = envUtils.getEnvironment().utcizeLocalDate(active_start, timezone)
		if active_end: active_end = envUtils.getEnvironment().utcizeLocalDate(active_end, timezone)

		siteDict = {}
		siteDict['code'] = code
		siteDict['descr'] = inParms['descr']
		siteDict['active_start'] = active_start
		siteDict['active_end'] = active_end
		if 'apps' in inParms:
			siteDict['apps'] = inParms.get('apps', [])
		return siteDict

class SiteAddHandler(AbstractSiteSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._siteAddHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _siteAddHandlerImpl(self):
		siteDict = self._siteValidation(True)
		siteSvc.SiteService().addSite(siteDict)
		siteCash.getSiteCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Site added" }))

class SiteSaveHandler(AbstractSiteSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._siteSaveHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _siteSaveHandlerImpl(self):
		siteDict = self._siteValidation(False)
		siteSvc.SiteService().saveSite(siteDict)
		siteCash.getSiteCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Site saved" }))


class AbstractSitePrefSaveHandler(absHandler.AbstractHandler):
	def _sitePrefValidation(self, _isAdd):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		self.validateStringRequired(inParms, 'code', "Code required")

		sitePrefDict = {}
		sitePrefDict['id'] = inParms.get('id', None)
		sitePrefDict['site_code'] = inParms.get('site_code', None)
		sitePrefDict['code'] = inParms.get('code', None)
		sitePrefDict['value'] = inParms.get('value', None)
		return sitePrefDict

class SitePrefAddHandler(AbstractSitePrefSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._sitePrefAddHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _sitePrefAddHandlerImpl(self):
		sitePrefDict = self._sitePrefValidation(True)
		siteSvc.SiteService().addSitePref(sitePrefDict)
		siteCash.getSiteCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Site Preference added" }))

class SitePrefSaveHandler(AbstractSitePrefSaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._sitePrefSaveHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _sitePrefSaveHandlerImpl(self):
		sitePrefDict = self._sitePrefValidation(False)
		siteSvc.SiteService().saveSitePref(sitePrefDict)
		siteCash.getSiteCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Site Preference saved" }))

class SitePrefDeleteHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._sitePrefDeleteHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _sitePrefDeleteHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		sitePrefDict = {}
		sitePrefDict['id'] = inParms.get('id', None)
		siteSvc.SiteService().deleteSitePref(sitePrefDict)
		siteCash.getSiteCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Site Preference deleted" }))


#   All URL mappings for this module.
urlMappings = [
	(r'/siteprofile', SiteProfileHandler),
	(r'/siteprofiledetail', SiteProfileDetailHandler),
	(r'/siteprofiledetailbypass', SiteProfileDetailBypassHandler),
	(r'/sitelist', SiteListHandler),
	(r'/sitelistbypass', SiteListBypassHandler),
	(r'/siteprefixlist', SitePrefixListHandler),
	(r'/siteprefixdetail', SitePrefixDetailHandler),
	(r'/sitepreferencedetail', SitePreferenceDetailHandler),
	(r'/siteadd', SiteAddHandler),
	(r'/sitesave', SiteSaveHandler),
	(r'/siteprefadd', SitePrefAddHandler),
	(r'/siteprefsave', SitePrefSaveHandler),
	(r'/siteprefdelete', SitePrefDeleteHandler),
]
