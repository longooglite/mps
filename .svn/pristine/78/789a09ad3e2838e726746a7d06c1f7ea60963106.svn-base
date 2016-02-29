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

kKeyName = 'MPSADMIN_SessionDisplayParms'

class AbstractSessionHandler(absHandler.AbstractHandler):

	def _getSessionDisplayParms(self):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		response = self.postToAuthSvc("/getRandomSessionData", payload, "Unable to obtain %s" % kKeyName)
		displayDict = response.get('value', None)
		if displayDict:
			return displayDict
		return self._getInitialSessionDisplayParms()

	def _getInitialSessionDisplayParms(self):
		displayDict = {}
		displayDict['site'] = self.request.headers.get('Site', '')
		return displayDict

	def _putSessionDisplayParms(self, _displayDict):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		payload['value'] = _displayDict
		response = self.postToAuthSvc("/putRandomSessionData", payload, "Unable to save %s" % kKeyName)

class SessionViewHandler(AbstractSessionHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('sessionView')

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		displayParmsDict = self._getSessionDisplayParms()
		context['displayParms'] = displayParmsDict

		realSiteList = self.postToAuthSvc("/sitelist", self.getInitialPayload(), "Unable to obtain Site data")
		siteList = [{'code':''}]
		siteList.extend(realSiteList)
		context['siteList'] = siteList

		site = displayParmsDict.get('site', self.request.headers.get('Site', ''))
		if site:
			siteProfileDetail = self._getSiteProfileDetail(site)
			context['siteProfileDetail'] = siteProfileDetail

		payload = self.getInitialPayload()
		payload['targetSite'] = site
		sessionResponse = self.postToAuthSvc("/sessionlist", payload, "Unable to obtain Session data")

		sessionList = sessionResponse.get('sessionList', [])
		sessionList = self._prepareSessionList(sessionList)
		expiredSessionList = sessionResponse.get('expiredSessionList', [])
		expiredSessionList = self._prepareSessionList(expiredSessionList)

		context['sessionList'] = sessionList
		context['expiredSessionList'] = expiredSessionList
		self.render("sessionList.html", context=context, skin=context['skin'])

	def _getSiteProfileDetail(self, _site):
		payload = self.getInitialPayload()
		payload['profileSite'] = _site
		return self.postToAuthSvc("/siteprofiledetail", payload, 'Unable to locate target site')

	def _prepareSessionList(self, _sessionList):
		env = envUtils.getEnvironment()
		self.localizeSessionListDates(_sessionList)
		for sessionInfo in _sessionList:
			sessionInfo['sortkey'] = "%s|%s" % (sessionInfo.get('site',''), sessionInfo.get('originTimestamp',''))
			sessionInfo['duration'] = ''
			try:
				originTS = env.parseUTCDate(sessionInfo['originTimestamp'])
				lastTS = env.parseUTCDate(sessionInfo['lastTimestamp'])
				sessionInfo['duration'] = "%s" % (lastTS - originTS,)
			except Exception, e:
				pass
		return sorted(_sessionList, key=operator.itemgetter('sortkey'), reverse=True)

	def localizeSessionListDates(self, _sessionList):
		if _sessionList:
			for sessionInfo in _sessionList:
				self.localizeOneSessionDates(sessionInfo)

	def localizeOneSessionDates(self, _sessionInfo):
		_sessionInfo['originTimestamp'] = self.localizeDate(_sessionInfo.get('originTimestamp', ''))
		_sessionInfo['lastTimestamp'] = self.localizeDate(_sessionInfo.get('lastTimestamp', ''))


class ChangeSiteHandler(AbstractSessionHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('sessionView')

		displayParmsDict = self._getSessionDisplayParms()
		formData = tornado.escape.json_decode(self.request.body)
		target = formData.get('target', '')
		displayParmsDict['site'] = target
		self._putSessionDisplayParms(displayParmsDict)

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/admin/sessions'
		self.write(tornado.escape.json_encode(responseDict))


class KillSessionHandler(AbstractSessionHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('sessionView')

		formData = tornado.escape.json_decode(self.request.body)
		sessionId = formData.get('sessionId', '')
		payload = self.getInitialPayload()
		payload['sessionId'] = sessionId
		response = self.postToAuthSvc("/sessionkill", payload, "Unable to terminate Session")

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/admin/sessions'
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/sessions', SessionViewHandler),
	(r'/admin/sessions/changesite', ChangeSiteHandler),
	(r'/admin/sessions/kill', KillSessionHandler),
]
