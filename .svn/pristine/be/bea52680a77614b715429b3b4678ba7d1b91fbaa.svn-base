# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import operator
import tornado.escape

import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.utilities.environmentUtils as envUtils

kKeyName = 'MPSADMIN_PrefDisplayParms'

class AbstractPrefHandler(absHandler.AbstractHandler):

	def _getPrefDisplayParms(self):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		response = self.postToAuthSvc("/getRandomSessionData", payload, "Unable to obtain %s" % kKeyName)
		displayDict = response.get('value', None)
		if displayDict:
			return displayDict
		return self._getInitialPrefDisplayParms()

	def _getInitialPrefDisplayParms(self):
		displayDict = {}
		displayDict['mode'] = 'site'
		displayDict['site'] = self.request.headers.get('Site', '')
		displayDict['prefix'] = ''
		return displayDict

	def _putPrefDisplayParms(self, _displayDict):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		payload['value'] = _displayDict
		response = self.postToAuthSvc("/putRandomSessionData", payload, "Unable to save %s" % kKeyName)

class PrefViewHandler(AbstractPrefHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('prefView')

		#   Render the page based on current settings.
		displayParmsDict = self._getPrefDisplayParms()
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['displayParms'] = displayParmsDict

		mode = displayParmsDict.get('mode', 'site')
		if mode == 'site':
			siteList = self.postToAuthSvc("/sitelist", self.getInitialPayload(), "Unable to obtain Site data")
			context['siteList'] = siteList

			site = displayParmsDict.get('site', self.request.headers.get('Site', ''))
			siteProfileDetail = self._getSiteProfileDetail(site)
			siteProfileDetail['sitePreferencesDetailList'] = self._organizeSiteDetailPreferencesForDisplay(siteProfileDetail.get('sitePreferencesDetailList', []))
			context['siteProfileDetail'] = siteProfileDetail
		else:
			if mode == 'prefix':
				prefixList = self.postToAuthSvc("/siteprefixlist", self.getInitialPayload(), "Unable to obtain Site prefix list")
				context['prefixList'] = prefixList

				prefix = displayParmsDict.get('prefix', '')
				sitePrefixDetail = self._getSitePrefixDetail(prefix)
				sitePrefixDetail = self._organizeSiteDetailPreferencesForDisplay(sitePrefixDetail)
				context['sitePrefixDetail'] = sitePrefixDetail

		context['disabled'] = "" if self.hasPermission('prefEdit') else "disabled"
		self.render("prefList.html", context=context, skin=context['skin'])

	def _getSiteProfileDetail(self, _site):
		payload = self.getInitialPayload()
		payload['profileSite'] = _site
		return self.postToAuthSvc("/siteprofiledetail", payload, 'Unable to locate target site')

	def _getSitePrefixDetail(self, _prefix):
		payload = self.getInitialPayload()
		payload['prefix'] = _prefix
		return self.postToAuthSvc("/siteprefixdetail", payload, 'Unable to locate target site prefix')

	def _organizeSiteDetailPreferencesForDisplay(self, _prefDetailList):
		self._addSortKeys(_prefDetailList)
		return sorted(_prefDetailList, key=operator.itemgetter('sortKey'))

	def _addSortKeys(self, _prefDetailList):
		for prefDict in _prefDetailList:
			prefDict['sortKey'] = self._buildOneKey(prefDict)

	def _buildOneKey(self, _prefDict):
		prefix = _prefDict.get('site_code', '')
		code = _prefDict.get('code', '')
		id = _prefDict.get('id', 0)
		return '%010d|%s|%010d' % (len(prefix), code, id)


class AbstractChangeSelectionHandler(AbstractPrefHandler):
	def _handle(self, _mode, _selectionKey):
		self.writePostResponseHeaders()
		self.verifyRequest()

		displayParmsDict = self._getPrefDisplayParms()
		if _mode:
			displayParmsDict['mode'] = _mode
		if _selectionKey:
			formData = tornado.escape.json_decode(self.request.body)
			target = formData.get('target', '')
			displayParmsDict[_selectionKey] = target
		self._putPrefDisplayParms(displayParmsDict)

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/admin/prefs'
		self.write(tornado.escape.json_encode(responseDict))

class ChangeSiteHandler(AbstractChangeSelectionHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self._handle('site', 'site')

class ChangePrefixHandler(AbstractChangeSelectionHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self._handle('prefix', 'prefix')

class ChangeModeHandler(AbstractChangeSelectionHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self._handle(None, 'mode')

class PrefEditDialogHandler(AbstractPrefHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('prefEdit')

		formData = tornado.escape.json_decode(self.request.body)
		target = formData.get('target', None)
		prefDict = {}

		#   Render the modal dialog.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		if target:
			context['mode'] = 'edit'
			context['modalTitle'] = 'Edit Site Preference'
			payload = self.getInitialPayload();
			payload['id'] = target
			prefList = self.postToAuthSvc("/sitepreferencedetail", payload, "Unable to obtain Site Preference data")
			if len(prefList) == 1:
				prefDict = prefList[0]
		else:
			context['mode'] = 'add'
			context['modalTitle'] = 'Add Site Preference'

		context['prefDict'] = prefDict
		content = self.render_string("prefEditModal.html", context=context, skin=context['skin'])

		#   Generate response.
		responseDict = self.getPostResponseDict()
		responseDict['content'] = content
		self.write(tornado.escape.json_encode(responseDict))

class PrefDeleteDialogHandler(AbstractPrefHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('prefEdit')

		formData = tornado.escape.json_decode(self.request.body)
		target = formData.get('target', None)
		prefDict = {}

		#   Render the modal dialog.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = 'delete'
		context['modalTitle'] = 'Delete Site Preference'
		payload = self.getInitialPayload();
		payload['id'] = target
		prefList = self.postToAuthSvc("/sitepreferencedetail", payload, "Unable to obtain Site Preference data")
		if len(prefList) == 1:
			prefDict = prefList[0]

		context['prefDict'] = prefDict
		content = self.render_string("prefDeleteModal.html", context=context, skin=context['skin'])

		#   Generate response.
		responseDict = self.getPostResponseDict()
		responseDict['content'] = content
		self.write(tornado.escape.json_encode(responseDict))


class PrefSaveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('prefEdit')

		formData = tornado.escape.json_decode(self.request.body)
		isAdd = formData.get('mode', '') == 'add'

		payload = self.getInitialPayload()
		payload['id'] = formData.get('id', 0)
		payload['site_code'] = formData.get('site_code', '')
		payload['code'] = formData.get('code', '')
		payload['value'] = formData.get('value', '')

		if isAdd:
			ignoredResponseDict = self.postToAuthSvc("/siteprefadd", payload, "Unable to add Site Preference data")
		else:
			ignoredResponseDict = self.postToAuthSvc("/siteprefsave", payload, "Unable to save Site Preference data")

		responseDict = self.getPostResponseDict("Site Preference saved")
		responseDict['redirect'] = '/admin/prefs'
		self.write(tornado.escape.json_encode(responseDict))


class PrefDeleteHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('prefEdit')

		formData = tornado.escape.json_decode(self.request.body)
		payload = self.getInitialPayload()
		payload['id'] = formData.get('id', 0)
		ignoredResponseDict = self.postToAuthSvc("/siteprefdelete", payload, "Unable to delete Site Preference data")

		responseDict = self.getPostResponseDict("Site Preference deleted")
		responseDict['redirect'] = '/admin/prefs'
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/prefs', PrefViewHandler),
	(r'/admin/prefs/changesite', ChangeSiteHandler),
	(r'/admin/prefs/changeprefix', ChangePrefixHandler),
	(r'/admin/prefs/changemode', ChangeModeHandler),
	(r'/admin/prefs/prefeditdialog', PrefEditDialogHandler),
	(r'/admin/prefs/prefdeletedialog', PrefDeleteDialogHandler),
	(r'/admin/prefs/save', PrefSaveHandler),
	(r'/admin/prefs/delete', PrefDeleteHandler),
]
