# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.containers.attest as attestTask
import MPSAppt.core.constants as constants
import MPSAppt.services.personalInfoService as personalInfoSvc

class PersonalInfoSummary(attestTask.Attest):
	def __init__(self, containerCode, parameterBlock):
		attestTask.Attest.__init__(self, containerCode, parameterBlock)

	def getEditContext(self, _sitePreferences):
		context = attestTask.Attest.getEditContext(self, _sitePreferences)

		#   Override the site-specific form name with a standard, generic one.
		#   Include the referenced UberForm control's data.

		context['form'] = 'personalInfoSummary.html'
		context['personal_info'] = {}
		context['personal_info_prompts'] = {}

		personalInfoContainer = self.locateEnabledPersonalInfoContainer()
		if personalInfoContainer:
			if personalInfoContainer.getClassName() == constants.kContainerClassUberForm:
				pInfoService = personalInfoSvc.PersonalInfoService(self.getWorkflow().getConnection())
				supplementalContext = pInfoService.getContextForReadOnlyPersonalInfoDisplay(self, personalInfoContainer, _sitePreferences)
				context.update(supplementalContext)

		return context
