# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.autofillService as autoPhilSvc
import MPSAppt.handlers.abstractHandler as absHandler
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.sqlUtilities as sqlUtils


class AutofillHandler(absHandler.AbstractHandler):
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
		srcjobactionid = kwargs.get('srcjobactionid', '')
		taskcodes = kwargs.get('taskcodes', '')

		connection = self.getConnection()
		autoPhilConnection = self.getAutoFillConnection()
		try:
			if autoPhilConnection:
				autoPhil = autoPhilSvc.AutofillService(connection,autoPhilConnection,self.profile)
				autoPhil.autofill(int(srcjobactionid),int(jobactionid),eval(taskcodes))

				jaService = jobActionSvc.JobActionService(connection)
				jobActionDict = jaService.getJobAction(jobactionid)
				self.updateRosterStatusForJobAction(connection, jobActionDict)

				self.redirect("/appt/jobaction/%s" % (jobactionid))
		finally:
			self.closeConnection()
			if autoPhilConnection:
				autoPhilConnection.closeMpsConnection()

	def getAutoFillConnection(self):
		autoFillConnection = None
		try:
			host = self.getSitePreferences().get('autofilldbhost','localhost')
			port = int(self.getSitePreferences().get('autofilldbport','5432'))
			dbname = self.getSitePreferences().get('autofilldbname','autofill')
			username = self.getSitePreferences().get('autofilldbusername','mps')
			password = self.getSitePreferences().get('autofilldbpassword','mps')
			connectionParms = dbConnParms.DbConnectionParms(host, port, dbname, username, password)
			autoFillConnection = sqlUtils.SqlUtilities(connectionParms)
		except Exception,e:
			pass
		finally:
			return autoFillConnection


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/autofill/(?P<jobactionid>[^/]*)/(?P<srcjobactionid>[^/]*)/(?P<taskcodes>[^/]*)", AutofillHandler),
]
