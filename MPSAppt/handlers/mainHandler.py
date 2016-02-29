# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.jobActionService as jobActionSvc
import MPSCore.utilities.stringUtilities as stringUtils

class MainHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()

		#   Render the page based on User Permissions.
		#   Special logic for candidates includes check that the correct Job Action GUID was included on the login URL.

		if self.hasPermission('apptCandidate'):
			url = self._locateCandidatePage()
			if url:
				self.redirect(url)
				return
		else:
			dashboardEnabled = self.hasPermission('apptDashboardView')
			rosterEnabled = self.hasPermission('apptRosterView')
			rosterFirst = stringUtils.interpretAsTrueFalse(self.getSitePreference('showrosterfirst', 'false'))

			if dashboardEnabled:
				if (not rosterEnabled) or (not rosterFirst):
					self.redirect("/appt/page/dashboard")
					return

			if rosterEnabled:
				self.redirect("/appt/page/roster")
				return

		self.redirect('/appt/visitor/unauthorized')

	def _locateCandidatePage(self):
		connection = self.getConnection()
		try:
			#   Find Job Actions associated with the current user.
			#   If none, then we're done.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			jobActionList = jobActionSvc.JobActionService(connection).getCurrentJobActionsForUser(community, username)
			if not jobActionList:
				return None

			#   Choose a job action based on configuration, and parameters supplied
			#   on the URL when the Candidate logged in.

			guidRequired = self.getSitePreferenceAsBoolean('apptcandidateguidreqd', 'true')
			if guidRequired:

				#   GUID required.
				#   Only return a URL if a guid was provided, and matches the external key of a job action.

				payload = self.getInitialPayload()
				payload['key'] = 'guid'
				response = self.postToAuthSvc("/getRandomSessionData", payload, "Unable to obtain guid")
				guid = response.get('value', None)
				if guid:
					for jobActionDict in jobActionList:
						if jobActionDict.get('external_key', '') == guid:
							return "/appt/jobaction/%s" % str(jobActionDict.get('id',0))
			else:

				#   GUID not an option.
				#   If a specific job action id was requested, then we must find that id.
				#   If if there is only one applicable job action, we return it.
				#	Or, if they have picked a rubber banded member, return the master.
				#	As a last resort, pick a valid key, any key.

				payload = self.getInitialPayload()
				payload['key'] = 'jobactionid'
				response = self.postToAuthSvc("/getRandomSessionData", payload, "Unable to obtain job action id")
				jobActionId = response.get('value', None)
				if jobActionId:
					for jobActionDict in jobActionList:
						if str(jobActionDict.get('id', 0)) == jobActionId:
							return "/appt/jobaction/%s" % str(jobActionId)
				else:
					if len(jobActionList) == 1:
						return "/appt/jobaction/%s" % str(jobActionList[0].get('id',0))
					else:
						masterId = jobActionSvc.JobActionService(connection).getParentRelatedJobAction(jobActionList[0].get('id',0))
						if masterId:
							return "/appt/jobaction/%s" % str(masterId)
						else:
							# as a last resort, pick last job action
							return "/appt/jobaction/%s" % str(jobActionList[len(jobActionList)-1].get('id',None))

		finally:
			self.closeConnection()

		return None


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
			self.clear_cookie('mpsid')
			self.postToAuthSvc("/logout", payload)
		except Exception:
			pass

		self.handleGetException(None, None)


#   All URL mappings for this module.

urlMappings = [
	(r'/appt', MainHandler),
	(r'/appt/logout', LogoutHandler),
]
