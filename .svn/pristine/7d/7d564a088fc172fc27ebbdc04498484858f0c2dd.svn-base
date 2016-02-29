# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.confirmTitleService as confirmedTitleSvc

class ConfirmTitle(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setConfirmedTitle({})


	#   Getters/Setters.

	def getConfirmedTitle(self): return self.confirmedTitleDict
	def setConfirmedTitle(self, _confirmedTitleDict): self.confirmedTitleDict = _confirmedTitleDict

	def getDepartmentId(self):
		self.loadInstance()
		return self.confirmedTitleDict.get('department_id',None)

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = confirmedTitleSvc.ConfirmedTitleService(self.getWorkflow().getConnection()).getConfirmedTitle(jobTask.get('id',0))
			if resultDict:
				self.setConfirmedTitle(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/confirmtitle'
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
			context['button_url'] = self._getURL('/appt/jobaction/confirmtitle/complete')
			return context
		return {}

	def _getURL(self, _prefix='/appt/jobaction/confirmtitle'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			return self.getConfirmedTitle().get('isactionable', False)

		return True

	def deleteYourself(self):
		self.loadInstance()
		if self.confirmedTitleDict:
			confirmedTitleSvc.ConfirmedTitleService(self.getWorkflow().getConnection()).deleteConfirmedTitle(self.confirmedTitleDict)
