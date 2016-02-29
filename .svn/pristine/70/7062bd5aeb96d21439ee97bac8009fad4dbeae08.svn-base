# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.jobPostingService as jobPostingService
import MPSAppt.services.qaService as qaService
import MPSAppt.services.uberService as uberService
import MPSAppt.core.constants as constants
import MPSCore.utilities.dateUtilities as dateUtilities

class JobPosting(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setJobPosting({})
		self.remainingPostingDays = 0


	#   Getters/Setters.

	def getJobPosting(self): return self.jobPostingDict
	def setJobPosting(self, _jobPostingDict): self.jobPostingDict = _jobPostingDict

	def getRemainingPostingDays(self): return self.remainingPostingDays
	def setRemainingPostingDays(self, _remainingPostingDays): self.remainingPostingDays = _remainingPostingDays


	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return
		resultDict = None
		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = jobPostingService.JobPostingService(self.getWorkflow().getConnection()).getJobPosting(jobTask.get('id',0))
		if not resultDict:
			resultDict = {}

		resultDict['isWaived'] = False
		if self.getConfigDict().get('waiverEnabled',False):
			requestedWaiver = False
			approvedWaiver = False
			dependencyContainerCodes = self.getConfigDict().get('waiverTasks',[])
			for dependencyContainerCode in dependencyContainerCodes:
				dependencyContainer = self.getWorkflow().getContainer(dependencyContainerCode)
				if dependencyContainer:
					if dependencyContainer.containerDict.get('className','') == constants.kContainerClassQuestionsAndAnswers:
						qaSVC = qaService.QAService(self.getWorkflow().getConnection())
						qaJobTask = self.getWorkflow().jobTaskCache.get(dependencyContainerCode,'')
						if qaJobTask:
							waiverCode = self.getConfigDict().get('waiverCode','')
							affirmativeResponse = self.getConfigDict().get('waivedAffirmativeResponse','')
							requestedWaiver = qaSVC.getIsWaived(qaJobTask,dependencyContainerCode,waiverCode,affirmativeResponse)

					elif dependencyContainer.containerDict.get('className','') == constants.kContainerClassUberForm:
						uberSVC = uberService.UberService(self.getWorkflow().getConnection())
						uberJobTask = self.getWorkflow().jobTaskCache.get(dependencyContainerCode,'')
						if uberJobTask:
							waiverQuestionCode = self.getConfigDict().get('waiverUberQuestionCode','')
							affirmativeResponse = self.getConfigDict().get('waiverUberAffirmativeResponse','')
							requestedWaiver = uberSVC.getIsWaived(dependencyContainer, waiverQuestionCode, affirmativeResponse)

					elif dependencyContainer.containerDict.get('className','') == constants.kContainerClassApproval:
						if dependencyContainer.isComplete():
							approvedWaiver = True
			if requestedWaiver and approvedWaiver:
				resultDict['isWaived'] = True
		if resultDict:
			self.setJobPosting(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/jobposting'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			argTuple = (prefix, jobActionIdStr, self.getCode())

			dataDict = {}
			dataDict['url'] = '%s/%s/%s' % argTuple
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			dataDict['remainingPostingDays'] = self.getRemainingPostingDays()
			dataDict['promptsDict'] = self.dictifyPromptsList(self.getConfigDict().get('prompts',[]))
			return dataDict
		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['button_text'] = 'Complete'
			context['button_url'] = self._getURL('/appt/jobaction/jobposting/complete')
			return context
		return {}

	def _getURL(self, _prefix='/appt/jobaction/jobposting'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):

		self.loadInstance()
		if self.getIsEnabled():
			posting = self.getJobPosting()
			if posting:
				if posting.get('isWaived',False):
					self.getContainerDict()['statusMsg'] = self.getConfigDict().get('postingWaivedStatusMsg','')
					return True
				if posting.has_key('date_posted'):
					if self.getConfigDict().get('days') == 0:
						return True
					exceedsBoundary,numDaysLeft = dateUtilities.datePlusDaysExceedsNow(posting.get('date_posted'),self.getConfigDict().get('days',0))
					if exceedsBoundary:
						self.getContainerDict()['statusMsg'] = self.getConfigDict().get('postingTimeMetStatusMsg','')
						return True
					else:
						self.setRemainingPostingDays(numDaysLeft)
			return False
		return True
