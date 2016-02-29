# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.attestService as attestSvc
import MPSAppt.services.jobActionService as jaService
import MPSAppt.services.uberGapService as uberGapSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.stringUtilities as stringUtils

class Attest(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setAttestation({})


	#   Initialization.

	def initializeOnNewJobAction(self, _jobAction, _personDict, _profile, _now, _username, doCommit=True):
		self.initializeItemSharingOnNewJobAction(_jobAction, _profile, _now, _username, doCommit=doCommit)

		actionInfo = {}
		if _personDict:
			initItems = self.getConfigDict().get('initItems',[])
			for initItem in initItems:
				if initItem.has_key('findValidAttestation'):
					findValidAttestation = initItem.get('findValidAttestation',[])
					for validAttestConfig in findValidAttestation:
						lookbackDays = validAttestConfig.get('lookbackDays',0)
						codes = validAttestConfig.get('codes')
						attestService = attestSvc.AttestService(self.getWorkflow().getConnection())
						validAttest = attestService.findViableAttest(codes,lookbackDays,_personDict)
						if validAttest:
							validAttest['updated'] = _now
							validAttest['id'] = None
							jobTask = jaService.JobActionService(self.getWorkflow().getConnection()).getOrCreateJobTask(_jobAction,self,_now,_username)
							validAttest['job_task_id'] = jobTask.get('id',-1)
							attestService.updateAttestation(jobTask,validAttest)
						else:
							emailConfigs = validAttestConfig.get('emails')
							if emailConfigs:
								self.sendDirectiveEmail(emailConfigs,_personDict,_jobAction,self,_now,_profile)
								actionInfo['grantCandidateAccess'] = True

		return actionInfo


	#   Getters/Setters.

	def getAttestation(self): return self._attestationDict
	def setAttestation(self, __attestationDict): self._attestationDict = __attestationDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = attestSvc.AttestService(self.getWorkflow().getConnection()).getAttestation(jobTask.get('id',0))
			if resultDict:
				self.setAttestation(resultDict)


	#   Directive emails.

	def extendEmailContext(self, _emailContext):
		#   Add/Change elements in the given _emailContext.
		env = envUtils.getEnvironment()
		appCode = env.getAppCode()
		loginURI = env.getLoginUri()
		siteApplications = self.getWorkflow().getUserProfile().get('siteProfile',{}).get('siteApplications',[])
		urlPrefix = env.getApplicationURLPrefix(appCode, siteApplications)
		externalKey = self.getWorkflow().getJobActionDict().get('external_key', '')
		_emailContext['candidate_url'] = "%s%s/%s" % (urlPrefix, loginURI, externalKey)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/attest'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			argTuple = (prefix, jobActionIdStr, self.getCode())

			dataDict = {}
			dataDict['url'] = '%s/%s/%s' % argTuple
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences,isForPrint = False):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['enable_print'] = self.getConfigDict().get('print_enabled',True)
			context['button_text'] = 'Submit'
			context['button_url'] = self._getURL('/appt/jobaction/attest/complete')
			context['print_url'] = self._getURL('/appt/jobaction/attest/print')
			context['prompts'] = self.dictifyPromptsList(self.getConfigDict().get('prompts',{}))
			context.update(self.updateContextWithImage(self.getConfigDict().get('displayImage',False),
			                                           self.getConfigDict().get('displayImageScalePixelWidth',400),
			                                           self.getConfigDict().get('displayImageTaskCode',''),
			                                           isForPrint))

			#   the old way, left here for backward compatibility
			#   on new templates, use {tags} below
			fullName = ''
			candidate = jaService.JobActionService(self.getWorkflow().getConnection()).getCandidateDict(self.getWorkflow().getJobActionDict())
			if candidate:
				fullName = candidate.get('full_name')
			context['candidate_name'] = fullName
			context['submitText'] = self.getConfigDict().get('submitText','')
			if '%s' in context['submitText']:
				context['submitText'] = context['submitText'] % fullName.upper()
			else:
				#   the new way, allows for a candidate or a system user to attest
				if self._attestationDict.has_key('attestor_department'):
					attestor_department = self._attestationDict.get('attestor_department','')
					attestor_name = self._attestationDict.get('attestor_name','')
				else:
					attestor_name,attestor_department = self.getNameAndDepartment()
				submitText = str(context['submitText'])
				if submitText.find('{attestor_department}') > -1:
					submitText=submitText.replace('{attestor_department}',attestor_department)
				if submitText.find('{attestor_name}') > -1:
					submitText=submitText.replace('{attestor_name}',attestor_name)
				context['submitText'] = submitText

			configKeyName = 'uberGapsConfig'
			uberGapsConfig = self.getConfigDict().get(configKeyName, [])
			if uberGapsConfig:
				gapSoivice = uberGapSvc.UberGapService(self.getWorkflow().getConnection())
				gaps = gapSoivice.processContainer(self, _sitePreferences, _configKeyName=configKeyName, _returnLocalizedDates=True)
				if gaps:
					context['gapsList'] = gaps
					context['gapsEnforced'] = self.getConfigDict().get('uberGapsEnforced', True)
					context['gapsEnforcedDescr'] = self.getConfigDict().get('uberGapsEnforcedText', '')
					context['gapsPrintIntroText'] = self.getConfigDict().get('uberGapsPrintIntroText', '')
					if context['gapsEnforced']:
						context['disabled'] = True

			return context

		return {}

	def getNameAndDepartment(self):
		attestor_name = ''
		isCandidate = self.hasPermission('apptCandidate')
		if not isCandidate:
			attestor_name = self.workflow.userProfile.get('userProfile',{}).get('userPreferences',{}).get('full_name''')
		else:
			candidate = jaService.JobActionService(self.workflow.connection).getCandidateDict(self.workflow.getJobActionDict())
			if candidate:
				attestor_name = candidate.get('full_name')
		attestor_department = self.workflow.department.get('full_descr','')
		return attestor_name.upper(),attestor_department.upper()


	def _getURL(self, _prefix='/appt/jobaction/attest'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			return self.getAttestation().get('complete', False)
		return True
