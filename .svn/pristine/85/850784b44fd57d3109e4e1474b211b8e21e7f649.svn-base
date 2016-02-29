# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

from MPSAppt.core.abstractPeriodicTaskWorker import AbstractPeriodicTaskWorker
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.sqlUtilities as sqlUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.completionService as completionSvc


gJobActionCompletionTaskLogger = logging.getLogger(__name__)

#   Complete Job Actions that are scheduled for completion today.
#   This function is call once per day by the tornado web framework.

def JobActionCompletionTask():
	global gJobActionCompletionTaskLogger

	gJobActionCompletionTaskLogger.info("JobActionCompletionTask initiated")
	JobActionCompleter().run()
	gJobActionCompletionTaskLogger.info("JobActionCompletionTask completed")

class JobActionCompleter(AbstractPeriodicTaskWorker):

	def run(self):

		#   Process all sites.

		siteList = self.getSiteList()
		for siteDict in siteList:
			self.processSite(siteDict)

	def processSite(self, siteDict):
		global gJobActionCompletionTaskLogger

		siteCode = siteDict.get('code','')
		gJobActionCompletionTaskLogger.info("Processing site '%s'" % siteCode)

		profile = self.getProfileForSite(siteCode)
		dbConnParms = self.getConnectionParmsForSite(profile)

		connection = None
		now = dateUtils.formatUTCDateOnly()
		try:
			connection = sqlUtils.SqlUtilities(dbConnParms)
			jaService = jobActionSvc.JobActionService(connection)
			jobActionIdList = jaService.getCompletableJobActionsAsOf(now)
			for jobActionIdDict in jobActionIdList:
				id = jobActionIdDict.get('id',0)
				completionSvc.CompletionService(connection).completeJobAction(id, now, 'system')

		except Exception, e:
			gJobActionCompletionTaskLogger.exception(str(e))

		finally:
			if connection:
				connection.closeMpsConnection()
