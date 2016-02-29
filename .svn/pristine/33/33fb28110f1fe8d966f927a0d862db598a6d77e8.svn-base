# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

from MPSAppt.core.abstractPeriodicTaskWorker import AbstractPeriodicTaskWorker
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.sqlUtilities as sqlUtils
import MPSAppt.services.reportingService as reportingSvc


gReportingArchiveWiperTaskLogger = logging.getLogger(__name__)

#   Delete reports that are older than X days, where X is a site preference (default = 90 days).
#   This function is call once per day by the tornado web framework.

def ReportingArchiveWiperTask():
	global gReportingArchiveWiperTaskLogger

	gReportingArchiveWiperTaskLogger.info("ReportingArchiveWiperTask initiated")
	ReportingArchiveWiper().run()
	gReportingArchiveWiperTaskLogger.info("ReportingArchiveWiperTask completed")

class ReportingArchiveWiper(AbstractPeriodicTaskWorker):

	def run(self):

		#   Process all sites.

		siteList = self.getSiteList()
		for siteDict in siteList:
			self.processSite(siteDict)

	def processSite(self, siteDict):
		global gReportingArchiveWiperTaskLogger

		siteCode = siteDict.get('code','')
		gReportingArchiveWiperTaskLogger.info("Processing site '%s'" % (siteCode,))

		profile = self.getProfileForSite(siteCode)
		try:
			reportPurgeDays = int(profile.get('sitePreferences', {}).get('reportpurgedays', '90'))
		except Exception, e:
			reportPurgeDays = 90
		gReportingArchiveWiperTaskLogger.info("  Report purge days: '%s'" % (str(reportPurgeDays),))

		connection = None
		now = dateUtils.formatUTCDateOnly()
		dbConnParms = self.getConnectionParmsForSite(profile)
		try:
			connection = sqlUtils.SqlUtilities(dbConnParms)
			rptSvc = reportingSvc.ReportingService(connection)
			staleReportList = rptSvc.getReportsCreatedBefore(reportPurgeDays, now)
			for each in staleReportList:
				id = each.get('id', 0)
				username = each.get('username', 'unknown')
				reportName = each.get('report_name', 'unknown')
				gReportingArchiveWiperTaskLogger.info("  Deleting: '%s':'%s'" % (username,reportName))
				rptSvc.deleteReport(id)

		except Exception, e:
			gReportingArchiveWiperTaskLogger.exception(str(e))

		finally:
			if connection:
				connection.closeMpsConnection()
