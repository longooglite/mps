# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.personService as personSvc

class IdentifyCandidate(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setPerson({})


	#   Getters/Setters.

	def getPerson(self): return self.personDict
	def setPerson(self, _personDict): self.personDict = _personDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobAction = self.getWorkflow().getJobActionDict()
		if jobAction:
			personId = jobAction.get('person_id', 0)
			if personId:
				resultDict = personSvc.PersonService(self.getWorkflow().getConnection()).getPerson(personId)
				if resultDict:
					self.setPerson(resultDict)


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
			context['prompts'] = self._buildPromptList()
			context['candidate_name'] = self._getCandidateName()
			return context

		return {}

	def _buildPromptList(self):
		promptList = []
		for configPromptDict in self.getConfigDict().get('prompts', []):
			if configPromptDict.get('enabled', False):
				code = configPromptDict.get('code', '')
				promptDict = {}
				promptDict['enabled'] = True
				promptDict['label'] = configPromptDict.get('label', '')
				promptDict['code'] = code
				promptDict['required'] = configPromptDict.get('required', False)
				promptDict['value'] = self.getPerson().get(code, '')

				if configPromptDict.get('ldapsearch', False):
					promptDict['ldapsearch_url'] = self._getURL(_prefix='/appt/jobaction/identifycandidate/search')

				promptList.append(promptDict)

		return promptList

	def _getCandidateName(self):
		myPersonDict = self.getPerson()
		if not myPersonDict:
			return ''

		firstName = myPersonDict.get('first_name','')
		middleName = myPersonDict.get('middle_name','')
		lastName = myPersonDict.get('last_name','')
		suffix = myPersonDict.get('suffix','')
		fullName = stringUtils.constructFullName(firstName, lastName, middleName, suffix)

		username = myPersonDict.get('username','')
		if username:
			return "%s (%s)" % (fullName, username)
		return fullName

	def _getURL(self, _prefix='/appt/jobaction/identifycandidate'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			prompts = self.getConfigDict().get('prompts',{})
			person = self.getPerson()
			if not person.get('id',None):
				return False
			for prompt in prompts:
				if prompt.get('required',False):
					if not person.get(prompt.get('code','')):
						return False
		return True

	def shouldGrantCandidateAccess(self):
		self.loadInstance()
		if not self.getIsEnabled(): return False

		myPersonDict = self.getPerson()
		if not myPersonDict: return False
		if not myPersonDict.get('username',''): return False

		for configPromptDict in self.getConfigDict().get('prompts', []):
			if (configPromptDict.get('enabled', False)) and \
				(configPromptDict.get('code', '') == 'username') and \
				(configPromptDict.get('ldapsearch', False)):
				return True

		return False
