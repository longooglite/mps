# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.core.constants as constants
import MPSAppt.services.approvalService as approvalSvc

class Submit(Task):
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

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = approvalSvc.ApprovalService(self.getWorkflow().getConnection()).getApproval(jobTask.get('id',0))
			if resultDict:
				self.setApproval(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			dataDict = {}
			dataDict['url'] = '/appt/jobaction/submit/%s/%s' % (jobActionIdStr, self.getCode())
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = '/appt/jobaction/submit/%s/%s' % (jobActionIdStr, self.getCode())
			context['comment_prompt_list'] = self.getCommentPromptList('activityLog')
			context['prompts'] = self.dictifyPromptsList(self.getConfigDict().get('prompts',[]))
			configDict = self.getConfigDict()
			context['date_enabled'] = configDict.get('date', False)
			context['date_text'] = configDict.get('dateText', '')
			context['instructional'] = configDict.get('instructional', '')
			context['date_required'] = configDict.get('dateRequired', False)
			if self.isComplete() and context['date_enabled']:
				context['date'] = self.convertMDYToDisplayFormat(_sitePreferences, self.getApproval().get('approval_date',''))
			return context

		return {}

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if self.getApproval().get('approval','') == constants.kApprovalSubmit:
				return True

			return False
		return True

	def deleteYourself(self):
		self.loadInstance()
		if self.getApproval():
			approvalSvc.ApprovalService(self.getWorkflow().connection).deleteApproval(self.getApproval())
			departmentContainerCode = self.getConfigDict().get('departmentContainer',None)
			if departmentContainerCode:
				#leave blacklist alone. The primary department should never be able to do anythin, for any department, that was blacklisted
				whiteList = self.getConfigDict().get('whitelist',None)
				if whiteList:
					departmentContainer = self.getWorkflow().getContainer(departmentContainerCode)
					if departmentContainer:
						departmentId = departmentContainer.getDepartmentId()
						if departmentId:
							import MPSAppt.services.jobActionService as jobActionService
							jobActionService.JobActionService(self.getWorkflow().getConnection()).removeJobActionOverride(self.getWorkflow().jobActionDict.get('id',-1),departmentId,whiteList.get('containers',[]))
