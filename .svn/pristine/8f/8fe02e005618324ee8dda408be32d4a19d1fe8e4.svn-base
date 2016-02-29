# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSCV.services.cvRendererService as cvRendererSvc

class CVImporterService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def userHasCV(self,community,username):
		return True

	def getCVForUser(self,cvSubject,initalContext,sitePrefs,environment):
		uiPath,fullPath = cvRendererSvc.CVPrintService(self.connection,initalContext,cvSubject,sitePrefs,'printMain.html',environment).renderCVToPDF()
		return uiPath,fullPath



