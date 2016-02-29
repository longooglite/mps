# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.core.containers.task import Task
import MPSAppt.services.serviceAndRankService as serviceAndRankSvc
import MPSAppt.services.lookupTableService as lookupTableSvc

class ServiceAndRank(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setServiceAndRank({})


	#   Getters/Setters.

	def getServiceAndRank(self): return self.serviceAndRankDict
	def setServiceAndRank(self, _serviceAndRankDict): self.serviceAndRankDict = _serviceAndRankDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = serviceAndRankSvc.ServiceAndRankService(self.getWorkflow().getConnection()).getServiceAndRank(jobTask.get('id',0))
			if resultDict:
				self.setServiceAndRank(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/serviceandrank'
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
			context['prompts'] = self._buildPromptList()
			buildings = serviceAndRankSvc.ServiceAndRankService(self.workflow.connection).getBuildings()
			buildingDict = {}
			for building in buildings:
				if building.get('address_lines',''):
					building['address_lines'] = json.loads(building['address_lines'])
				buildingDict[building.get('code')] = building
			context['buildingsJSON'] = json.dumps(buildingDict)
			buildingList = []
			for building in buildings:
				buildingList.append({'code':building.get('code',''),'descr':building.get('descr','')})
			context['buildings'] = buildingList
			context['states'] = lookupTableSvc.getCodeDescrListByKey(self.workflow.connection, 'cv_static_lookup', 'STATES', 'lookup_key', code='code',descr='descr')
			context['countries'] = lookupTableSvc.getCodeDescrListByKey(self.workflow.connection, 'cv_static_lookup', 'COUNTRIES', 'lookup_key', code='code',descr='descr')
			context['membershipCategories'] = self.getConfigDict().get('membershipCategories')
			return context
		return {}

	def _buildPromptList(self):
		promptList = []
		serviceAndRank = self.getServiceAndRank()
		for configPromptDict in self.getConfigDict().get('prompts', []):
			code = configPromptDict.get('code', '')
			promptDict = {}
			promptDict['enabled'] = configPromptDict.get('enabled',True)
			promptDict['label'] = configPromptDict.get('label', '')
			promptDict['code'] = code
			promptDict['required'] = configPromptDict.get('required', False)
			value = serviceAndRank.get(code,'')
			dataType = configPromptDict.get('data_type', '')
			if dataType == 'repeatingtext' and value:
				value = json.loads(value)
			promptDict['value'] = value
			promptDict['data_type'] = dataType
			promptList.append(promptDict)
		return promptList


	def _getURL(self, _prefix='/appt/jobaction/placeholder'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if not self.getServiceAndRank():
				return False
		return True
