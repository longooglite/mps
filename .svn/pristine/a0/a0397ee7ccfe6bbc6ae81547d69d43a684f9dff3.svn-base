# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import urllib2

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.backgroundCheckSQL as backgroundCheckSQL
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.backgroundCheck.backgroundCheckUtils as bcUtils
import MPSAppt.core.sql.fileRepoSQL as fileRepoSQL


class BackgroundCheckService(AbstractTaskService):
	logger = logging.getLogger(__name__)

	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getBackgroundCheck(self, _jobTaskId):
		return backgroundCheckSQL.getBackgroundCheck(self.connection, _jobTaskId)

	def createBackgroundCheck(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.createBackgroundCheck(self.connection, _backgroundCheckDict, doCommit)

	def findPending(self):
		return backgroundCheckSQL.findPending(self.connection)


	#   Event Handlers.

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		backgroundCheckClassName = _container.getConfigDict().get('backgroundCheckClassName', '')
		if backgroundCheckClassName:
			try:
				bcObj = bcUtils.instantiateBackgroundCheck(_container, self.connection)
				orders = bcObj.getOrders(doCommit)
				if not orders:
					self.handleWaive(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit)
					return

				result = bcObj.submit(False)
				if result.get('status', 'error') == 'ok':
					_backgroundCheckDict['external_key'] = result.get('externalKey', '')
				else:
					raise Exception(result.get('error', 'Unknown error'))

			except Exception, e:
				_backgroundCheckDict['submitted_error'] = e.message
				self.handleSubmissionError(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit)
				return

		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckSubmitted, 'enactSubmittedStatus', doCommit=doCommit)

	def handleSubmissionError(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckSubmittedError, 'enactSubmittedErrorStatus', _dashboardConfigKeyName='submitDashboardEvents', _alertConfigKeyName='errorAlert',  _emailConfigKeyName='crook', doCommit=doCommit)

	def handleAccept(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckAccept, 'enactAcceptStatus', _dashboardConfigKeyName='completeDashboardEvents', _alertConfigKeyName='completeAlert', doCommit=doCommit)

	def handleAcceptWithFindings(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckAcceptFindings, 'enactAcceptStatus', _dashboardConfigKeyName='completeDashboardEvents', _alertConfigKeyName='completeAlert', doCommit=doCommit)

	def handleReject(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckRejected, 'enactRejectedStatus', _freezeConfigKeyName='rejectFreeze', _dashboardConfigKeyName='completeDashboardEvents', _alertConfigKeyName='completeAlert', _emailConfigKeyName='crook', doCommit=doCommit)

	def handleInProgress(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckInProgress, 'enactInProgressStatus', _emailConfigKeyName='crook', doCommit=doCommit)

	def handleComplete(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckComplete, 'enactCompleteStatus', _dashboardConfigKeyName='completeDashboardEvents', _alertConfigKeyName='completeAlert', doCommit=doCommit)

	def handleCompleteWithFindings(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckCompleteWithFindings, 'enactCompleteStatus', _dashboardConfigKeyName='findingsDashboardEvents', _alertConfigKeyName='findingsAlert', _emailConfigKeyName='crook', doCommit=doCommit)

	def handleWaive(self, _jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, doCommit=True):
		self.handle(_jobActionDict, _jobTaskDict, _backgroundCheckDict, _container, _profile, _formData, _now, _username, constants.kJobActionLogVerbBackgroundCheckWaived, 'enactWaivedStatus', _dashboardConfigKeyName='completeDashboardEvents', _alertConfigKeyName='waivedAlert', _emailConfigKeyName='crook', doCommit=doCommit)

	def handle(self,
			_jobActionDict,
			_jobTaskDict,
			_backgroundCheckDict,
			_container,
			_profile,
			_formData,
			_now,
			_username,
			_verb,
			_enactMethodName,
			_activityLogConfigKeyName='activityLog',
			_dashboardConfigKeyName='dashboardEvents',
			_freezeConfigKeyName='freeze',
			_alertConfigKeyName='alert',
			_emailConfigKeyName='emails',
			doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Enact specified status.
			actionString = '''self.%s(_backgroundCheckDict, doCommit=False)''' % _enactMethodName
			exec actionString

			#   Activity Log Text override.
			_container.getConfigDict().get(_activityLogConfigKeyName, {})['activityLogText'] = constants.kJobActionBlurbDict.get(_verb, "Background Check")

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = _verb
				logDict['item'] = _container.getDescr()
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName=_activityLogConfigKeyName, _dashboardConfigKeyName=_dashboardConfigKeyName, _freezeConfigKeyName=_freezeConfigKeyName, _alertConfigKeyName=_alertConfigKeyName, _emailConfigKeyName=_emailConfigKeyName, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e


	#   Status update handler.

	def getCandidateStatus(self, _jobActionDict, _container, _profile, _now, _username, doCommit=True):
		_container.loadInstance()
		jobTaskDict = _container.getPrimaryJobTaskDict()
		if jobTaskDict:
			backgroundCheckDict = _container.getBackgroundCheck()
			if backgroundCheckDict:
				externalKey = backgroundCheckDict.get('external_key', '')
				if externalKey:
					try:
						bcObj = bcUtils.instantiateBackgroundCheck(_container, self.connection)
						result = bcObj.getCandidateStatus(externalKey, False)
						if result.get('status', 'error') == 'ok':
							if result.get('complete', False):
								flagged = result.get('flagged', False)
								backgroundCheckDict['status_date'] = _now
								backgroundCheckDict['completed_date'] = _now
								backgroundCheckDict['flagged'] = flagged
								backgroundCheckDict['updated'] = _now
								backgroundCheckDict['lastuser'] = _username

								#   Try to obtain and store actual report content.
								reportURL = backgroundCheckDict.get('report_url', '')
								if reportURL:
									try:
										req = urllib2.Request(reportURL)
										response = urllib2.urlopen(req)
										rawresult = response.read()
										backgroundCheckDict['report_content'] = fileRepoSQL._encodeContent(str(rawresult))
									except Exception, e:
										if not (isinstance(e, excUtils.MPSException)):
											e = excUtils.wrapMPSException(e)
										self.logger.exception(e.getDetailMessage())

								if flagged:
									self.handleCompleteWithFindings(_jobActionDict, jobTaskDict, backgroundCheckDict, _container, _profile, {}, _now, _username)
								else:
									self.handleComplete(_jobActionDict, jobTaskDict, backgroundCheckDict, _container, _profile, {}, _now, _username)
							else:
								if backgroundCheckDict.get('status', '') != constants.kBackgroundCheckStatusInProgress:
									backgroundCheckDict['status_date'] = _now
									backgroundCheckDict['updated'] = _now
									backgroundCheckDict['lastuser'] = _username
									self.handleInProgress(_jobActionDict, jobTaskDict, backgroundCheckDict, _container, _profile, {}, _now, _username)
						else:
							raise Exception(result.get('error', 'Unknown error'))

					except Exception, e:
						if not (isinstance(e, excUtils.MPSException)):
							e = excUtils.wrapMPSException(e)
						self.logger.exception(e.getDetailMessage())


	#   Lastest report handler.

	def getCandidateReport(self, _jobActionDict, _container, _profile, _now, _username, doCommit=True):
		_container.loadInstance()
		jobTaskDict = _container.getPrimaryJobTaskDict()
		if jobTaskDict:
			backgroundCheckDict = _container.getBackgroundCheck()
			if backgroundCheckDict:
				externalKey = backgroundCheckDict.get('external_key', '')
				if externalKey:
					try:
						bcObj = bcUtils.instantiateBackgroundCheck(_container, self.connection)
						result = bcObj.getCandidateReport(externalKey, False)
						if result.get('status', 'error') == 'ok':
							url = result.get('url', '')
							backgroundCheckDict['report_url'] = url
							backgroundCheckDict['updated'] = _now
							backgroundCheckDict['lastuser'] = _username
							backgroundCheckSQL.updateReportURL(self.connection, backgroundCheckDict, doCommit=doCommit)
						else:
							raise Exception(result.get('error', 'Unknown error'))

					except Exception, e:
						if not (isinstance(e, excUtils.MPSException)):
							e = excUtils.wrapMPSException(e)
						self.logger.exception(e.getDetailMessage())


	#   Make It So, Mister Worf.

	def enactSubmittedStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactSubmittedStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactSubmittedErrorStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactSubmittedErrorStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactWaivedStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactWaivedStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactInProgressStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactInProgressStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactCompleteStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactCompleteStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactAcceptStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactAcceptStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactAcceptFindingsStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactAcceptFindingsStatus(self.connection, _backgroundCheckDict, doCommit)

	def enactRejectedStatus(self, _backgroundCheckDict, doCommit=True):
		backgroundCheckSQL.enactRejectedStatus(self.connection, _backgroundCheckDict, doCommit)
