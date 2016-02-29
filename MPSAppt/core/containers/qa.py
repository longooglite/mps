# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
from MPSAppt.services import qaService as qaSvc

class QA(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setQA({})


	#   Getters/Setters.

	def getQA(self): return self.qaDict
	def setQA(self, _qaDict): self.qaDict = _qaDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		qasvc = qaSvc.QAService(self.getWorkflow().getConnection())
		qas = qasvc.getQuestionsAndOptionsForTask(self.getCode())

		responses = {}
		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			responses = qaSvc.QAService(self.getWorkflow().getConnection()).getResponsesToQuestions(jobTask.get('id',0),self.getCode())

		resultDict = {"questionsAndAnswers":qas, "responses":responses}
		if resultDict:
			self.setQA(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			prefix = '/appt/jobaction/qa'
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
			argTuple = (prefix, jobActionIdStr, self.getCode())

			dataDict = {}
			dataDict['url'] = '%s/%s/%s' % argTuple
			prefix = '/appt/jobaction/qadraft'
			argTuple = (prefix, jobActionIdStr, self.getCode())
			dataDict['save_as_draft_url'] = '%s/%s/%s' % argTuple
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getPrompts(self):
		return self.dictifyPromptsList(self.getConfigDict().get('prompts',[]))

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			return self.determineComplete()
		return True

	def determineComplete(self):
		qas = self.getQA().get('questionsAndAnswers',[])
		responses = self.getQA().get('responses',{})
		for q in qas:
			response = responses.get(q.get('id',-1))
			if not response and not q.get('options',[]) == [] and q.get('required',True):
				return False
			if not response and q.get('options',[]) == [] and not q.get('required',True):
				break
			if not response.get('complete',False):
				return False
			if q.get('options',[]):
				foundResponse = False
				for option in q.get('options',[]):
					if option.get('id',-1) == response.get('question_option_id',-1):
						if option.get('text_required',True):
							if response.get('text_response','').strip():
								foundResponse = True
								break
						else:
							foundResponse = True
							break
				if not foundResponse:
					return False
			else:
				if response:
					if q.get('required',True) and not response.get('text_response','').strip():
						return False
		return True
