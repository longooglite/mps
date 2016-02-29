# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import json

import MPSCV.utilities.environmentUtils as envUtils
import MPSCV.handlers.abstractHandler as absHandler
import MPSCV.services.cvService as cvSvc

class AbstractExportHandler(absHandler.AbstractHandler):
	pass

class ExportJsonHandler(AbstractExportHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['cvView','cvEdit'])

		community = kwargs.get('community', 'default')
		username = kwargs.get('username', '')
		if (not community) or (not username):
			self.redirect("/cv")
			return

		try:
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)

			cvDict = cvSvc.getCVExportDataForUser(connection, community, username)

			env = envUtils.getEnvironment()
			dstFilePath = env.createGeneratedOutputFilePath('cv_', '.json')
			f = None
			try:
				f = open(dstFilePath, 'w')
				json.dump(cvDict, f, indent=4)
				f.flush()
			finally:
				if f:
					try: f.close()
					except Exception, e: pass

			self.redirect(env.getUxGeneratedOutputFilePath(dstFilePath))

		finally:
			self.closeConnection()


#   All URL mappings for this module.
urlMappings = [
	(r"/cv/exportjson/(?P<community>[^/]*)/(?P<username>[^/]*)", ExportJsonHandler),
]
