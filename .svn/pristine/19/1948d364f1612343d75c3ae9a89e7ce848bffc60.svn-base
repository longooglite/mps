# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSCore.utilities.exceptionUtils as excUtils
import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.utilities.environmentUtils as envUtils

class AbstractCommunityHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def getSiteList(self):
		return self.postToAuthSvc("/sitelist", self.getInitialPayload(), "Unable to obtain Site data")

	def getCommunityList(self):
		return self.postToAuthSvc("/communitylist", self.getInitialPayload(), "Unable to obtain Community data")


class CommunityViewHandler(AbstractCommunityHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('communityView')

		communityList = self.getCommunityList()

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['communityList'] = communityList
		context['disabled'] = "" if self.hasPermission('communityEdit') else "disabled"
		self.render("communityList.html", context=context, skin=context['skin'])


class CommunityDetailHandler(AbstractCommunityHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['communityEdit'])

		#   Site code and Community code required.
		siteCode = str(kwargs.get('siteCode', ''))
		if not siteCode:
			raise excUtils.MPSValidationException("Site code required")
		communityCode = str(kwargs.get('communityCode', ''))
		if not communityCode:
			raise excUtils.MPSValidationException("Community code required")

		#   Find site and community.
		communityDict = None
		communityList = self.getCommunityList()
		for thisDict in communityList:
			thisSiteCode = str(thisDict.get('site_code', ''))
			thisCommunityCodeCode = str(thisDict.get('code', ''))
			if (thisSiteCode == siteCode) and (thisCommunityCodeCode == communityCode):
				communityDict = thisDict
				break;
		if not communityDict:
			raise excUtils.MPSValidationException("Community code not found")

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = "edit"
		context['communityDict'] = communityDict
		context['disabled'] = "" if self.hasPermission('communityEdit') else "disabled"
		self.render("communityDetail.html", context=context, skin=context['skin'])


class CommunityAddHandler(AbstractCommunityHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['communityEdit'])

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['mode'] = "add"
		context['communityDict'] = {}
		context['siteList'] = self.getSiteList()
		context['disabled'] = "" if self.hasPermission('communityEdit') else "disabled"
		self.render("communityDetail.html", context=context, skin=context['skin'])


class CommunitySaveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('communityEdit')

		formData = tornado.escape.json_decode(self.request.body)
		isAdd = formData.get('mode', '') == 'add'
		code = formData.get('code', '')
		if isAdd:
			code = code.lower()

		payload = self.getInitialPayload()
		payload['code'] = code
		payload['descr'] = formData.get('descr', '')
		payload['targetSite'] = formData.get('sitecode', '')

		if isAdd:
		 	ignoredResponseDict = self.postToAuthSvc("/communityadd", payload, "Unable to add Community data")
		else:
		 	ignoredResponseDict = self.postToAuthSvc("/communitysave", payload, "Unable to save Community data")

		responseDict = self.getPostResponseDict("Community saved")
		responseDict['redirect'] = '/admin/communities'
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/admin/communities', CommunityViewHandler),
	(r'/admin/community/detail/(?P<siteCode>[^/]*)/(?P<communityCode>[^/]*)', CommunityDetailHandler),
	(r'/admin/community/add', CommunityAddHandler),
	(r'/admin/community/save', CommunitySaveHandler),
]
