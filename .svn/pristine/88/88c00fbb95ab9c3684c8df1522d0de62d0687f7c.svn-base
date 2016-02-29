# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.services.dumpRestoreService as dumpRestoreSvc
import MPSAdmin.utilities.environmentUtils as envUtils
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractDatabaseHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _getDatabaseProfile(self, _profileSite):
		payload = self.getInitialPayload()
		payload['profileSite'] = _profileSite
		return self.postToAuthSvc("/siteprofiledetail", payload, "Unable to obtain Site data")

	def _getDumpRestoreSiteList(self):
		siteList = []
		authSite = self._getSpecialSite('auth')
		if authSite:
			siteList.append(authSite)

		autofillSite = self._getSpecialSite('autofill')
		if autofillSite:
			siteList.append(autofillSite)

		if siteList:
			siteList.append({ "code": "", "descr": "" })

		realSites = self.postToAuthSvc("/sitelist", self.getInitialPayload(), "Unable to obtain Site data")
		siteList.extend(realSites)
		return siteList

	def _getSpecialSite(self, _siteCode):
		result = {}
		profile = self._getDatabaseProfile(_siteCode)
		if profile:
			sitePrefs = profile.get('sitePreferences', {})
			if sitePrefs:
				result['code'] = _siteCode
				result['descr'] = sitePrefs.get('descr', '')
		return result

	def _identifyDumpRestoreDatabase(self, _dumpSiteProfile):
		sitePrefs = _dumpSiteProfile.get('sitePreferences',{})
		host = sitePrefs.get('dbhost', '')
		port = sitePrefs.get('dbport', '')
		dbname = sitePrefs.get('dbname', '')
		username = sitePrefs.get('dbusername', '')
		password = sitePrefs.get('dbpassword', '')
		return dbConnParms.DbConnectionParms(host=host, port=port, dbname=dbname, username=username, password=password)


class DumpHandler(AbstractDatabaseHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('dbDump')

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['siteList'] = self._getDumpRestoreSiteList()
		self.render("dbDump.html", context=context, skin=context['skin'])

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('dbDump')

		formData = tornado.escape.json_decode(self.request.body)
		self.validateFormData(formData)
		dumpSite = formData.get('dumpSite', '')
		dumpFilename = formData.get('dumpFilename', '')

		#   Get configuration for the desired site.
		#   Dump the database.
		dumpSiteProfile = self._getDatabaseProfile(dumpSite)
		dbConnectionParms = self._identifyDumpRestoreDatabase(dumpSiteProfile)
		dumpRestoreSvc.DumpRestoreService().dump(dumpSite, dumpFilename, dbConnectionParms)

		responseDict = self.getPostResponseDict("Database dumped")
		responseDict['redirect'] = '/admin/db/dump'
		self.write(tornado.escape.json_encode(responseDict))

	def validateFormData(self, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['dumpSite','dumpFilename']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


class RestoreHandler(AbstractDatabaseHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('dbRestore')

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['siteList'] = self._getDumpRestoreSiteList()
		context['fileList'] = self._getDumpFileList()
		self.render("dbRestore.html", context=context, skin=context['skin'])

	def _getDumpFileList(self):
		authFileList = []
		autofillFileList = []
		otherFileList = []

		allFiles = dumpRestoreSvc.DumpRestoreService().getDumpFileList()
		for each in allFiles:
			site = each.get('site', '')
			if site == 'auth':
				authFileList.append(each)
			elif site == 'autofill':
				autofillFileList.append(each)
			else:
				otherFileList.append(each)

		return authFileList + autofillFileList + otherFileList

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('dbRestore')

		formData = tornado.escape.json_decode(self.request.body)
		self.validateFormData(formData)
		restoreSite = formData.get('restoreSite', '')
		dumpSite = formData.get('dumpSite', '')
		dumpFilename = formData.get('dumpFilename', '')

		#   Get configuration for the desired restoration site.
		#   Restore the database.
		restoreSiteProfile = self._getDatabaseProfile(restoreSite)
		dbConnectionParms = self._identifyDumpRestoreDatabase(restoreSiteProfile)
		migrationMessage = dumpRestoreSvc.DumpRestoreService().restore(restoreSite, dumpSite, dumpFilename, dbConnectionParms)
		if migrationMessage:
			msg = 'Migration Failure - use this database at your own risk'
		else:
			msg = 'Database restored'
		if restoreSite == 'auth':
			msg += ' - You should manually clear the Site and User caches'
		responseDict = self.getPostResponseDict(msg)
		responseDict['redirect'] = '/admin/db/restore'
		self.write(tornado.escape.json_encode(responseDict))

	def validateFormData(self, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['restoreSite','dumpSiteFilename']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		dumpSiteFilename = _formData.get('dumpSiteFilename', '')
		splitz = dumpSiteFilename.split('|')
		if len(splitz) != 2:
			jErrors.append({ 'code': 'dumpSiteFilename', 'field_value': dumpSiteFilename, 'message': 'Required' })
		else:
			_formData['dumpSite'] = splitz[0]
			_formData['dumpFilename'] = splitz[1]

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


class DeleteHandler(AbstractDatabaseHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('dbRestore')

		formData = tornado.escape.json_decode(self.request.body)
		self.validateFormData(formData)
		dumpSite = formData.get('dumpSite', '')
		dumpFilename = formData.get('dumpFilename', '')

		#   Delete the indicated file.
		dumpRestoreSvc.DumpRestoreService().delete(dumpSite, dumpFilename)

		responseDict = self.getPostResponseDict("File deleted")
		responseDict['redirect'] = '/admin/db/restore'
		self.write(tornado.escape.json_encode(responseDict))

	def validateFormData(self, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['dumpSiteFilename']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		dumpSiteFilename = _formData.get('dumpSiteFilename', '')
		splitz = dumpSiteFilename.split('|')
		if len(splitz) != 2:
			jErrors.append({ 'code': 'dumpSiteFilename', 'field_value': dumpSiteFilename, 'message': 'Required' })
		else:
			_formData['dumpSite'] = splitz[0]
			_formData['dumpFilename'] = splitz[1]

		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


#   All URL mappings for this module.

urlMappings = [
	(r'/admin/db/dump', DumpHandler),
	(r'/admin/db/restore', RestoreHandler),
	(r'/admin/db/delete', DeleteHandler),
]
