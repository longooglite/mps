# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.completionService as completionSvc

class Completion(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setCompletion({})


	#   Getters/Setters.

	def getCompletion(self): return self.completionDict
	def setCompletion(self, _completionDict): self.completionDict = _completionDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = completionSvc.CompletionService(self.getWorkflow().getConnection()).getCompletion(jobTask.get('id',0))
			if resultDict:
				self.setCompletion(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			dataDict = {}
			dataDict['url'] = self._getURL()
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['comment_prompt_list'] = self.getCommentPromptList('activityLog')

			if self.isComplete():
				context['effective'] = self.getCompletion().get('effective_date', '')
				context['scheduled'] = self.getCompletion().get('scheduled_date', '')

			return context

		return {}

	def _getURL(self):
		prefix = '/appt/jobaction/completion'
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/complete/%s/%s' % (prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if self.getCompletion().get('scheduled_date', ''):
				return True

			return False
		return True
