# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.services.communityService as communitySvc
import MPSAuthSvc.caches.siteCache as siteCash
import MPSAuthSvc.caches.userCache as userCash
import MPSCore.utilities.exceptionUtils as excUtils

class CommunityListHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._communityListHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _communityListHandlerImpl(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		communityList = communitySvc.CommunityService().getAllCommunities()
		self.write(tornado.escape.json_encode(communityList))

class AbstractCommunitySaveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _communityValidation(self):
		self.writePostResponseHeaders()
		sessionInfo, siteProfile = self.checkCallersCredentials()

		inParms = tornado.escape.json_decode(self.request.body)
		self.validateStringRequired(inParms, 'targetSite', "Site code required")
		self.validateStringRequired(inParms, 'code', "Community code required")
		self.validateStringRequired(inParms, 'descr', "Community description required")

		siteCode = inParms.get('targetSite', None)
		siteProfile = self.getOrCreateSite(siteCode)
		if not siteProfile:
			raise excUtils.MPSValidationException("Invalid Site code identifier")

		communityDict = {}
		communityDict['site_id'] = siteProfile.get('sitePreferences', {}).get('id', 0)
		communityDict['code'] = inParms.get('code', None)
		communityDict['descr'] = inParms['descr']
		return communityDict


class CommunityAddHandler(AbstractCommunitySaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._communityAddHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _communityAddHandlerImpl(self):
		communityDict = self._communityValidation()
		communitySvc.CommunityService().addCommunity(communityDict)
		siteCash.getSiteCache().invalidateCache()
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Community added" }))


class CommunitySaveHandler(AbstractCommunitySaveHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._communitySaveHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _communitySaveHandlerImpl(self):
		communityDict = self._communityValidation()
		communitySvc.CommunityService().saveCommunity(communityDict)
		siteCash.getSiteCache().invalidateCache()
		userCash.getUserCache().invalidateCache()
		self.write(tornado.escape.json_encode({ "message": "Community saved" }))


#   All URL mappings for this module.
urlMappings = [
	(r'/communitylist', CommunityListHandler),
	(r'/communityadd', CommunityAddHandler),
	(r'/communitysave', CommunitySaveHandler),
]
