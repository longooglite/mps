# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task


class PacketDownload(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)

	#   Data loading.

	def loadInstance(self):
		pass


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		if self.getIsEnabled():
			dataDict = {}
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			dataDict['url'] = '/appt/jobaction/packet/' + jobActionIdStr + '/' + self.getCode()
			if self.getWorkflow().jobActionDict.get('complete',False):
				dataDict['disabled'] = False
			else:
				dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict
		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			context['url'] = '/appt/jobaction/packet/' + jobActionIdStr + '/' + self.getCode()
			context['download_url'] = '/appt/jobaction/packet/download/' + jobActionIdStr + '/' + self.getCode()
			context['packet_name'] = self.getContainerDict().get('descr','')
			return context
		return {}

	def isComplete(self):
		return False
