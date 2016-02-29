# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.jobActionService as jobActionSvc
import logging

class ViewAsCandidateHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		jobactionid = kwargs.get('jobactionid', '')
		onoroff = kwargs.get('onoroff', '')
		connection = self.getConnection()
		try:
			jobActionService = jobActionSvc.JobActionService(connection)
			jobAction = jobActionService.getJobAction(jobactionid)
			candidate = jobActionService.getCandidateDict(jobAction)
			if candidate:
				payload = self.getInitialPayload()
				payload['value'] = 'true' if onoroff == 'on' else 'false'
				payload['username'] = candidate.get('username', '')
				self.postToAuthSvc('/setCandidateView', payload, "")
			self.redirect("/appt/jobaction/%s" % (jobactionid))
		finally:
			self.closeConnection()

urlMappings = [
	(r"/appt/viewascandidate/(?P<jobactionid>[^/]*)/(?P<onoroff>[^/]*)", ViewAsCandidateHandler),
]
