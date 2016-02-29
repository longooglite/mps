# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

from MPSCV.services import cvRendererService
import MPSCV.handlers.abstractHandler as absHandler

class AbstractPrintHandler(absHandler.AbstractHandler):

	def removeEmptyDicts(self, demDicts):
		keepers = []
		for each in demDicts:
			categoryDict = each.get('categoryDict')
			if categoryDict.get('displayFieldList',[]) <> []:
				keepers.append(each)

		return keepers

class PrintCVHandler(AbstractPrintHandler):
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
		if not username:
			self.redirect("/cv")
			return
		try:
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)
			cvSubject = self.getCVSubject(community, username)
			sitePrefs = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})
			initalContext = self.getInitialTemplateContext(self.getEnvironment())
			uiPath,fullPath = cvRendererService.CVPrintService(connection,initalContext,cvSubject,sitePrefs,kwargs.get('template','printMain.html'),self.getEnvironment()).renderCVToPDF()
			self.redirect(uiPath)
		finally:
			self.closeConnection()

class PrintCategoryCVHandler(AbstractPrintHandler):
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
		categoryCode = kwargs.get('categoryCode', '')
		if not username:
			self.redirect("/cv")
			return

		try:
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)
			cvSubject = self.getCVSubject(community, username)
			sitePrefs = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})
			initalContext = self.getInitialTemplateContext(self.getEnvironment())
			uiPath,fullPath = cvRendererService.CVPrintService(connection,initalContext,cvSubject,sitePrefs,kwargs.get('template','printMain.html'),self.getEnvironment()).renderCVToPDF(categoryCode)
			self.redirect(uiPath)
		finally:
			self.closeConnection()


#   All URL mappings for this module.
urlMappings = [
	(r"/cv/print/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<categoryCode>[^/]*)/(?P<template>[^/]*)", PrintCategoryCVHandler),
	(r"/cv/print/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<template>[^/]*)", PrintCVHandler),
]
