# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.uberResolverService as uberResolverService

class PersonalInfoService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	#   Given the following:
	#       primary container of any type
	#       personal info uberform container
	#       site preferences
	#
	#   this routine returns a display context for the primary container with the data necessary to
	#   display a read-only copy of the given personal info.

	def getContextForReadOnlyPersonalInfoDisplay(self, _primaryContainer, _personalInfoContainer, _sitePreferences):
		context = {}
		context['form'] = 'personalInfoSummary.html'

		summaryConfig = _primaryContainer.getConfigDict().get('personalInfoSummaryConfig', [])
		sectionCache = self._getSectionCache(_personalInfoContainer, _sitePreferences)
		resolverService = uberResolverService.UberResolverService(_primaryContainer.getWorkflow().getConnection(), _sitePreferences)

		chunkList = []
		for configItem in summaryConfig:
			sectionName = configItem.get('section', '')
			if sectionName:
				sectionDict = sectionCache.get(sectionName, {})
				if sectionDict:
					chunk = {}
					chunk['title'] = configItem.get('title', '')
					chunk['prompts'] = resolverService.resolveQuestionsInGroup(sectionDict)
					chunkList.append(chunk)

		context['rowData'] = chunkList
		return context

	def _getSectionCache(self, _personalInfoContainer, _sitePreferences):
		sectionCache = {}
		allSections = _personalInfoContainer.getEditContext(_sitePreferences).get('uber_instance', {}).get('questions', {}).get('elements', [])
		for section in allSections:
			sectionCode = section.get('code', '')
			if sectionCode:
				sectionCache[sectionCode] = section
		return sectionCache
