# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.placeholderService as placeholderSvc

class Placeholder(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setPlaceholder({})


	#   Getters/Setters.

	def getPlaceholder(self): return self.placeholderDict
	def setPlaceholder(self, _placeholderDict): self.placeholderDict = _placeholderDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = placeholderSvc.PlaceholderService(self.getWorkflow().getConnection()).getPlaceholder(jobTask.get('id',0))
			if resultDict:
				self.setPlaceholder(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/placeholder'
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
			context['button_text'] = 'Complete'
			context['button_url'] = self._getURL('/appt/jobaction/placeholder/complete')
			if self.isComplete():
				context['button_text'] = 'Undo'
				context['button_url'] = self._getURL('/appt/jobaction/placeholder/undo')
			return context
		return {}

	def _getURL(self, _prefix='/appt/jobaction/placeholder'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			return self.getPlaceholder().get('complete', False)

		return True
