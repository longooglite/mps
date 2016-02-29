# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.core.constants as constants
import MPSAppt.core.backgroundCheck.backgroundCheckUtils as bcUtils
import MPSAppt.services.backgroundCheckService as backgroundCheckSvc
import MPSAppt.services.personalInfoService as personalInfoSvc

class BackgroundCheck(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setBackgroundCheck({})


	#   Getters/Setters.

	def getBackgroundCheck(self): return self.backgroundCheckDict
	def setBackgroundCheck(self, _backgroundCheckDict): self.backgroundCheckDict = _backgroundCheckDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = backgroundCheckSvc.BackgroundCheckService(self.getWorkflow().getConnection()).getBackgroundCheck(jobTask.get('id',0))
			if resultDict:
				self.setBackgroundCheck(resultDict)


	#   Simple Questions.

	def isFlagged(self):
		return self.getBackgroundCheck().get('flagged', False)

	def hasReportUrl(self):
		if self.getBackgroundCheck().get('report_url', ''):
			return True
		return False

	def hasReportContent(self):
		if self.getBackgroundCheck().get('report_content', None):
			return True
		return False

	def hasSubmittedStatus(self):
		status = self.getBackgroundCheck().get('status', constants.kBackgroundCheckStatusUnknown)
		return status in [ \
			constants.kBackgroundCheckStatusSubmitted,
			constants.kBackgroundCheckStatusInProgress,
			constants.kBackgroundCheckStatusComplete,
			constants.kBackgroundCheckStatusAccepted,
			constants.kBackgroundCheckStatusAcceptedWithFindings,
			constants.kBackgroundCheckStatusRejected,
		]

	def hasCompletedStatus(self):
		status = self.getBackgroundCheck().get('status', constants.kBackgroundCheckStatusUnknown)
		if (status == constants.kBackgroundCheckStatusComplete) and (not self.isFlagged()):
			return True
		return status in [ \
			constants.kBackgroundCheckStatusAccepted,
			constants.kBackgroundCheckStatusAcceptedWithFindings,
			constants.kBackgroundCheckStatusRejected,
			constants.kBackgroundCheckStatusWaived,
		]

	def hasExternalCompletedStatus(self):
		status = self.getBackgroundCheck().get('status', constants.kBackgroundCheckStatusUnknown)
		return status in [ \
			constants.kBackgroundCheckStatusComplete,
			constants.kBackgroundCheckStatusAccepted,
			constants.kBackgroundCheckStatusAcceptedWithFindings,
			constants.kBackgroundCheckStatusRejected,
			constants.kBackgroundCheckStatusWaived,
		]

	def isResubmittable(self):
		status = self.getBackgroundCheck().get('status', constants.kBackgroundCheckStatusUnknown)
		return status in [ \
			constants.kBackgroundCheckStatusUnknown,
			constants.kBackgroundCheckStatusNotSubmitted,
			constants.kBackgroundCheckStatusSubmitted,
			constants.kBackgroundCheckStatusSubmittedError,
			constants.kBackgroundCheckStatusInProgress,
		]

	def isDecisionRequired(self):
		status = self.getBackgroundCheck().get('status', constants.kBackgroundCheckStatusUnknown)
		return (status == constants.kBackgroundCheckStatusComplete) and (self.isFlagged())


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/backgroundcheck'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			argTuple = (prefix, jobActionIdStr, self.getCode())

			dataDict = {}
			dataDict['url'] = '%s/%s/%s' % argTuple
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()

			bgCheck = self.getBackgroundCheck()
			context['background_check'] = bgCheck
			if bgCheck:
				self._resolveBackgroundCheck(bgCheck, _sitePreferences)

				context['personal_info'] = {}
				context['personal_info_prompts'] = {}

				personalInfoContainer = self.locateEnabledPersonalInfoContainer()
				if personalInfoContainer:
					if personalInfoContainer.getClassName() == constants.kContainerClassUberForm:
						pInfoService = personalInfoSvc.PersonalInfoService(self.getWorkflow().getConnection())
						supplementalContext = pInfoService.getContextForReadOnlyPersonalInfoDisplay(self, personalInfoContainer, _sitePreferences)
						context.update(supplementalContext)

				context['offenses'] = []
				context['disclosure_prompts'] = []
				disclosureContainer = self.locateEnabledDisclosureContainer()
				if disclosureContainer:
					context['disclosure_prompts'] = disclosureContainer.getConfigDict().get('prompts',[])
					if disclosureContainer.isComplete():
						disclosureContainer.prepDisclosureForDisplay(disclosureContainer.getDisclosure(), _sitePreferences)
						context['offenses'] = disclosureContainer.getDisclosure().get('offenses', [])

				bcObj = bcUtils.instantiateBackgroundCheck(self, self.getWorkflow().getConnection())
				context['orders'] = bcObj.getOrders(True)

			self._setupViewCurrentReport(context)
			self._setupViewStoredReport(context)
			self._setupResubmittable(context)
			self._setupDecision(context)
			self._setupStatusing(context)
			return context

		return {}

	def locateEnabledDisclosureContainer(self):
		disclosureTaskCode = self.getConfigDict().get('disclosureTaskCode', '')
		if disclosureTaskCode:
			disclosureContainer = self.getWorkflow().getContainer(disclosureTaskCode)
			if disclosureContainer:
				if disclosureContainer.getClassName() == constants.kContainerClassDisclosure:
					if disclosureContainer.getIsEnabled():
						return disclosureContainer
		return None

	def _resolveBackgroundCheck(self, _backgroundCheckDict, _sitePreferences):
		_backgroundCheckDict['submitted_date'] =  self.convertTimestampToDisplayFormat(_sitePreferences, _backgroundCheckDict.get('submitted_date', ''))
		_backgroundCheckDict['status_date'] =  self.convertTimestampToDisplayFormat(_sitePreferences, _backgroundCheckDict.get('status_date', ''))
		_backgroundCheckDict['completed_date'] =  self.convertTimestampToDisplayFormat(_sitePreferences, _backgroundCheckDict.get('completed_date', ''))
		_backgroundCheckDict['created'] =  self.convertTimestampToDisplayFormat(_sitePreferences, _backgroundCheckDict.get('created', ''))
		_backgroundCheckDict['updated'] =  self.convertTimestampToDisplayFormat(_sitePreferences, _backgroundCheckDict.get('updated', ''))
		_backgroundCheckDict['submitted_status'] = self.getSubmittedStatus(_backgroundCheckDict)
		_backgroundCheckDict['current_status'] = self.getCurrentStatus(_backgroundCheckDict)

	def getSubmittedStatus(self, _backgroundCheckDict):
		status = self.getBackgroundCheck().get('status', constants.kBackgroundCheckStatusUnknown)
		if (status != constants.kBackgroundCheckStatusSubmitted) and (self.hasSubmittedStatus()):
			return '''%s on %s''' % (constants.kBackgroundCheckStatusBlurbDict.get(constants.kBackgroundCheckStatusSubmitted, 'Submitted'), _backgroundCheckDict.get('submitted_date', ''))
		return ''

	def getCurrentStatus(self, _backgroundCheckDict):
		status = _backgroundCheckDict.get('status', constants.kBackgroundCheckStatusUnknown)
		displayStatus = constants.kBackgroundCheckStatusBlurbDict.get(status, constants.kBackgroundCheckStatusBlurbDict.get(constants.kBackgroundCheckStatusUnknown, 'Unknown'))

		dateBlurb = ''
		displayDate = _backgroundCheckDict.get('status_date', '')

		if status in [constants.kBackgroundCheckStatusSubmitted, constants.kBackgroundCheckStatusSubmittedError]:
			dateBlurb = 'on'
			displayDate = _backgroundCheckDict.get('submitted_date', '')
		elif status == constants.kBackgroundCheckStatusInProgress:
			dateBlurb = 'as of'
		elif status == constants.kBackgroundCheckStatusComplete:
			dateBlurb = 'on'
			displayDate = _backgroundCheckDict.get('completed_date', '')
		elif status in [constants.kBackgroundCheckStatusAccepted, constants.kBackgroundCheckStatusAcceptedWithFindings, constants.kBackgroundCheckStatusRejected]:
			dateBlurb = 'on'

		if dateBlurb:
			displayStatus = '''%s %s %s''' % (displayStatus, dateBlurb, displayDate)
		return displayStatus

	def _setupViewCurrentReport(self, _context):
		_context['current_report_allowed'] = False
		_context['current_report_text'] = ''
		_context['current_report_url'] = ''
		if (self.hasReportUrl()) and (self.hasAnyPermission(self.getConfigDict().get('currentReportPermissions', []))):
			_context['current_report_allowed'] = True
			_context['current_report_text'] = self.getConfigDict().get('currentReportText', 'View Report')
			_context['current_report_url'] = self.getBackgroundCheck().get('report_url', '')

	def _setupViewStoredReport(self, _context):
		_context['stored_report_allowed'] = False
		_context['stored_report_text'] = ''
		_context['stored_report_url'] = ''
		if (self.hasReportUrl()) and (self.hasReportContent() ) and (self.hasAnyPermission(self.getConfigDict().get('storedReportPermissions', []))):
			_context['stored_report_allowed'] = True
			_context['stored_report_text'] = self.getConfigDict().get('storedReportText', 'Stored copy of Completed CBC report')
			_context['stored_report_url'] = self._getURL(_action='/storedreport')

	def _setupResubmittable(self, _context):
		_context['resubmit_allowed'] = False
		_context['resubmit_text'] = ''
		_context['resubmit_url'] = ''
		if (self.isResubmittable()) and (self.hasAnyPermission(self.getConfigDict().get('resubmitPermissions', []))):
			_context['resubmit_allowed'] = True
			_context['resubmit_text'] = self.getConfigDict().get('resubmitText', 'Resubmit Background Check request')
			_context['resubmit_url'] = self._getURL(_action='/submit')

	def _setupDecision(self, _context):
		_context['decision_allowed'] = False
		_context['decision_text'] = ''
		if (self.isDecisionRequired()) and (self.hasAnyPermission(self.getConfigDict().get('decisionPermissions', []))):
			_context['decision_allowed'] = True
			_context['decision_text'] = self.getConfigDict().get('decisionText', 'Decision')
			_context['accept_text'] = self.getConfigDict().get('acceptText', 'Accept')
			_context['accept_findings_text'] = self.getConfigDict().get('acceptFindingsText', 'Accept Findings and Proceed')
			_context['reject_text'] = self.getConfigDict().get('rejectText', 'Reject Hiring')
			_context['accept_url'] = self._getURL(_action='/accept')
			_context['accept_findings_url'] = self._getURL(_action='/acceptfindings')
			_context['reject_url'] = self._getURL(_action='/reject')
			_context['comment_prompt_list'] = self.getCommentPromptList('activityLog')

	def _setupStatusing(self, _context):
		_context['statusing_allowed'] = False
		if self.hasAnyPermission(self.getConfigDict().get('statusPermissions', [])):
			_context['statusing_allowed'] = True
			_context['submission_error_url'] = self._getURL(_action='/submissionerror')
			_context['inprogress_url'] = self._getURL(_action='/inprogress')
			_context['complete_url'] = self._getURL(_action='/complete')
			_context['complete_with_findings_url'] = self._getURL(_action='/completefindings')
			_context['waive_url'] = self._getURL(_action='/waive')

	def _getURL(self, _prefix='/appt/jobaction/backgroundcheck', _action='', _suffix=''):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s%s/%s/%s%s' % (_prefix, _action, jobActionIdStr, self.getCode(), _suffix)

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			return self.hasCompletedStatus()
		return True
