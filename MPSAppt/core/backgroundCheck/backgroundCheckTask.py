# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import tornado.httpclient

import MPSAppt.core.constants as constants
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.sqlUtilities as sqlUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.backgroundCheckService as backgroundCheckSvc

gBackgroundCheckTaskLogger = logging.getLogger(__name__)

#   Update the status of outstanding Background Check requests.
#   This function is called periodically by the tornado web framework.

def BackgroundCheckTask():
	global gBackgroundCheckTaskLogger

	gBackgroundCheckTaskLogger.info("MPSAppt BackgroundCheckTask initiated")
	BackgroundChecker().run()
	gBackgroundCheckTaskLogger.info("MPSAppt BackgroundCheckTask completed")

class BackgroundChecker(object):
	global gBackgroundCheckTaskLogger


	def run(self):
		#   Process all sites.
		siteList = self.postToAuthSvc('/sitelistbypass', {})
		for siteDict in siteList:
			self.processSite(siteDict)

	def processSite(self, siteDict):
		try:
			siteCode = siteDict.get('code','')
			gBackgroundCheckTaskLogger.info("MPSAppt BackgroundCheckTask processing site '%s'" % siteDict.get('code',''))

			profile = self.getProfileForSite(siteCode)
			if not self.checkSiteProfileForAppAccess(profile):
				gBackgroundCheckTaskLogger.info("MPSAppt BackgroundCheckTask skipping site '%s': not authorized for this application" % siteDict.get('code',''))
				return

			connection = None
			dbConnParms = self.getConnectionParmsForSite(profile)
			try:
				#   Get a list of Job Actions with Background Check rows having either 'Submitted' or 'In Progress' status.
				connection = sqlUtils.SqlUtilities(dbConnParms)
				bcService = backgroundCheckSvc.BackgroundCheckService(connection)
				jobActionList = bcService.findPending()
				for jobAction in jobActionList:
					self.processJobAction(connection, jobAction, profile)

			finally:
				if connection:
					connection.closeMpsConnection()

		except Exception, e:
			if not (isinstance(e, excUtils.MPSException)):
				e = excUtils.wrapMPSException(e)
			gBackgroundCheckTaskLogger.exception(e.getDetailMessage())

	def processJobAction(self, _connection, _jobAction, _profile):

		#   Load the Workflow for the Job Action.
		#   Find the Background Check Tasks and process them.

		workflow = workflowSvc.WorkflowService(_connection).getWorkflowForJobAction(_jobAction, _profile)
		backgroundCheckContainers = workflow.getContainersForClassName(constants.kContainerClassBackgroundCheck)
		for container in backgroundCheckContainers:
			container.loadInstance()
			originalStatus = container.getBackgroundCheck().get('status','')
			if originalStatus in [constants.kBackgroundCheckStatusSubmitted, constants.kBackgroundCheckStatusInProgress]:
				#   Get latest copy of report.
				#   Get order status from 3rd-party service.
				now = dateUtils.formatUTCDate()
				bcService = backgroundCheckSvc.BackgroundCheckService(_connection)
				bcService.getCandidateReport(_jobAction, container, _profile, now, 'system')

				container.setIsLoaded(False)
				container.loadInstance()
				bcService.getCandidateStatus(_jobAction, container, _profile, now, 'system')

				#   Recompute roster status if container status has changed.
				container.setIsLoaded(False)
				container.loadInstance()
				if container.getBackgroundCheck().get('status','') != originalStatus:
					workflow = workflowSvc.WorkflowService(_connection).getWorkflowForJobAction(_jobAction, _profile)
					status = workflow.computeStatus()
					jaService = jobActionSvc.JobActionService(_connection)
					jaService.updateJobActionRosterStatus(_jobAction.get('id',0), status, now, 'system')


	#   Utility.

	def getProfileForSite(self, _siteCode):
		payload = {}
		payload['profileSite'] = _siteCode
		profile = self.postToAuthSvc("/siteprofiledetailbypass", payload)
		return profile

	def checkSiteProfileForAppAccess(self, _profile):
		appCode = envUtils.getEnvironment().getAppCode()
		if appCode:
			for siteApp in _profile.get('siteApplications', []):
				if siteApp.get('code','') == appCode:
					return True
		return False

	def getConnectionParmsForSite(self, _profile):
		sitePrefsDict = _profile.get('sitePreferences',{})
		connectionParms = dbConnParms.DbConnectionParms(sitePrefsDict.get('dbhost',''),
														sitePrefsDict.get('dbport',''),
														sitePrefsDict.get('dbname',''),
														sitePrefsDict.get('dbusername',''),
														sitePrefsDict.get('dbpassword',''))
		return connectionParms

	def postToAuthSvc(self, _uri, _unJsonifiedPayload):
		response = ""
		authserviceurl = envUtils.getEnvironment().getAuthServiceUrl()
		http_client = tornado.httpclient.HTTPClient()
		try:
			jsonResponse = http_client.fetch(
				authserviceurl + _uri,
				method='POST',
				headers = {'Content-Type':'application/json'},
				body=tornado.escape.json_encode(_unJsonifiedPayload))
			response = tornado.escape.json_decode(jsonResponse.body)
		finally:
			http_client.close()

		return response
