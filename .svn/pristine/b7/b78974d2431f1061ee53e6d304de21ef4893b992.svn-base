# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAdmin.handlers.abstractHandler as absHandler
import MPSAdmin.utilities.environmentUtils as envUtils

class MainHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()

		#   Render the page.
		env = envUtils.getEnvironment()
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['releaseVersion'] = env.getVersion()
		context['releaseCodeName'] = env.getReleaseCodeName()
		context['releaseStatus'] = env.getReleaseStatus()
		context['releaseBuildDate'] = env.getReleaseBuildDate().strftime('%m/%d/%Y %H:%M')
		self.render("admin.html", context=context, skin=context['skin'])

class LogoutHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):

		#   Try to log out, no biggie if we can't.
		#   Redirect to Login page.
		try:
			payload = { 'mpsid': self.getCookie('mpsid') }
			self.postToAuthSvc("/logout", payload)
		except Exception:
			pass

		self.handleGetException(None, None)


#   All URL mappings for this module.
urlMappings = [
	(r'/admin', MainHandler),
	(r'/admin/logout', LogoutHandler),
]
