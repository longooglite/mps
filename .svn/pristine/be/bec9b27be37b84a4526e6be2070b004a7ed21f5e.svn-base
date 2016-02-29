# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.core.constants as constants
import MPSAppt.services.approvalService as approvalSvc

class Approval(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setApproval({})


	#   Getters/Setters.

	def getApproval(self): return self.approvalDict
	def setApproval(self, _approvalDict): self.approvalDict = _approvalDict


	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTaskCache = self.getWorkflow().getJobTaskCache()
		jobTask = jobTaskCache.get(self.getCode(), None)
		if jobTask:
			resultDict = approvalSvc.ApprovalService(self.getWorkflow().getConnection()).getApproval(jobTask.get('id',0))
			if resultDict:
				self.setApproval(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/approval'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			argTuple = (prefix, jobActionIdStr, self.getCode())
			dataDict = {}
			dataDict['url'] = '%s/%s/%s' % argTuple
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			dataDict['approvalStatus'] = self.approvalDict.get('approval','')
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/approval'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			argTuple = (prefix, jobActionIdStr, self.getCode())

			context = self.getCommonEditContext(_sitePreferences)
			context['approve_url'] = '%s/approve/%s/%s' % argTuple
			context['deny_url'] = '%s/deny/%s/%s' % argTuple
			context['revisions_url'] = '%s/revise/%s/%s' % argTuple

			configDict = self.getConfigDict()
			context['config'] = configDict
			if configDict.get('revisionsRequired', False):
				freezeConfig = configDict.get('revisionsRequiredFreeze', {})
				options = freezeConfig.get('unfreezeOptions', [])
				if options:
					revisionsOptions = []
					for optionTaskCode in options:
						optionContainer = self.getWorkflow().getContainer(optionTaskCode)
						if optionContainer:
							container = self.getWorkflow().getContainer(optionTaskCode)
							if container.getIsEnabled():
								optionDict = {}
								optionDict['code'] = optionTaskCode
								optionDict['descr'] = optionContainer.getHeader()
								revisionsOptions.append(optionDict)
					context['revisions_options'] = revisionsOptions

			context['comment_prompt_list'] = self.getCommentPromptList('activityLog')
			context['vote_enabled'] = configDict.get('vote', False)
			context['date_enabled'] = configDict.get('date', False)
			context['date_text'] = configDict.get('dateText', '')
			context['date_required'] = configDict.get('dateRequired', False)
			context['prompts'] = self.dictifyPromptsList(self.getConfigDict().get('prompts',[]))

			activityLogTaskCodes = configDict.get('activityLogTaskCodes',[])
			if activityLogTaskCodes:
				context['activity_log'] = self.getTaskActivityLog(_sitePreferences, activityLogTaskCodes)

			if self.isComplete():
				context['approval'] = self.getApproval().get('approval','')
				context['approval_descr'] = self.getStatusMsg()
				if context['vote_enabled']:
					context['for'] = str(self.getApproval().get('vote_for',''))
					context['against'] = str(self.getApproval().get('vote_against',''))
					context['abstain'] = str(self.getApproval().get('vote_abstain',''))
				if context['date_enabled']:
					context['date'] = self.convertMDYToDisplayFormat(_sitePreferences, self.getApproval().get('approval_date',''))

			return context

		return {}

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if self.getApproval().get('approval','') in [constants.kApprovalDeny]:
				if self.getConfigDict().get("denyIsNotDone",False):
					return False
			if self.getApproval().get('approval','') in [constants.kApprovalApprove, constants.kApprovalDeny]:
				return True

			return False
		return True

	def getStatusMsg(self):
		if self.isComplete():
			if self.getApproval().get('approval','') == constants.kApprovalApprove:
				statusMsg = self.getConfigDict().get('approveStatusMsg','')
				if statusMsg:
					return statusMsg
			if self.getApproval().get('approval','') == constants.kApprovalDeny:
				statusMsg = self.getConfigDict().get('denyStatusMsg','')
				if statusMsg:
					return statusMsg
			if self.getApproval().get('approval','') == constants.kApprovalRevisionsRequired:
				statusMsg = self.getConfigDict().get('revisionsRequiredStatusMsg','')
				if statusMsg:
					return statusMsg
		return self.getContainerDict().get('statusMsg', '')

	def deleteYourself(self):
		self.loadInstance()
		if self.getApproval():
			approvalSvc.ApprovalService(self.getWorkflow().getConnection()).deleteApproval(self.getApproval())
