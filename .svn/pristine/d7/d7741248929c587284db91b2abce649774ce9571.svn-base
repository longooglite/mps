# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.qaSQL as sql

class QAService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getQuestionsAndOptionsForTask(self,taskCode,optionalIdentifierCode=''):
		questionsList = []
		if optionalIdentifierCode:
			rawQuestions = sql.getQuestionsAndOptionsForTaskAndIdentifierCode(self.connection,taskCode,optionalIdentifierCode)
		else:
			rawQuestions = sql.getQuestionsAndOptionsForTask(self.connection,taskCode)
		current_options_list = []
		current_id = -1
		for rawquestion in rawQuestions:
			if rawquestion.get('quest_active',True):
				if current_id <> rawquestion.get('quest_id',0):
					question = self.createQuestion(rawquestion)
					questionsList.append(question)
					current_id = rawquestion.get('quest_id',0)
					current_options_list =  question['options']
				if rawquestion.get('opt_id',None) and rawquestion.get('opt_active',True):
					prompt = self.createPrompt(rawquestion)
					current_options_list.append(prompt)
		return questionsList

	def getResponsesToQuestions(self, job_task_id, task_code):
		responseDict = {}
		rawResponses =  sql.getResponsesToQuestions(self.connection,job_task_id,task_code)
		for response in rawResponses:
			responseDict[response.get('question_id',0)] = {"question_option_id":response.get('question_option_id',0),"text_response":response.get('text_response',''),"complete":response.get('complete','')}
		return responseDict

	def createQuestion(self,rawQuestion):
		questionDict = {}
		questionDict['id'] = rawQuestion.get('quest_id',0)
		questionDict['code'] = rawQuestion.get('quest_code')
		questionDict['identifier_code'] = rawQuestion.get('quest_identifier_code','')
		questionDict['nbr_rows'] = rawQuestion.get('quest_nbr_rows','')
		questionDict['prompt'] = rawQuestion.get('quest_prompt','')
		questionDict['required'] = rawQuestion.get('quest_required','')
		questionDict['options'] = []
		return questionDict

	def createPrompt(self,rawPrompt):
		promptDict = {}
		promptDict['id'] = rawPrompt.get('opt_id',0)
		promptDict['code'] = rawPrompt.get('opt_code','')
		promptDict['has_text'] = rawPrompt.get('opt_has_text',True)
		promptDict['id'] = rawPrompt.get('opt_id',0)
		promptDict['nbr_rows'] = rawPrompt.get('opt_nbr_rows',5)
		promptDict['option_text'] = rawPrompt.get('opt_text','')
		promptDict['text_required'] = rawPrompt.get('opt_text_required',False)
		promptDict['text_title'] = rawPrompt.get('opt_text_title','')
		return promptDict

	def saveResponsesToOptions(self,questionsAndAnswers,_jobTaskDict,isComplete,doCommit = True):
		try:
			sql.deleteResponsesToQuestions(self.connection,_jobTaskDict.get('id',0),doCommit = True)
			for question in questionsAndAnswers:
				jaId = _jobTaskDict.get('id',0)
				qCode = question.get('questioncode','')
				optcode = question.get('optioncode','')
				textResponse = question.get('textresponse','')
				created = question.get('created','')
				updated = question.get('updated','')
				lastuser = question.get('lastuser','')
				self.saveResponseToOption(jaId,qCode,optcode,textResponse,created,updated,lastuser,isComplete,doCommit = True)
			if doCommit:
				self.connection.performCommit()
		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def saveResponseToOption(self,jobTaskId,questioncode,optioncode,textresponse,created,updated,lastuser,isComplete,doCommit = True):
		question = sql.getQuestion(self.connection,questioncode)
		option = None if not optioncode else sql.getOption(self.connection,optioncode)
		optionid = option.get('id',0) if option else None
		sql.insertResponseToOption(self.connection,jobTaskId,question.get('id',0),optionid,textresponse,created,updated,lastuser,isComplete,doCommit)

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _qaList, _container, _profile, _now, _username, isComplete, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			self.saveResponsesToOptions(_qaList,_jobTaskDict,isComplete,doCommit=True)

			#Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				complete = True
				logDict['item'] = 'incomplete' if complete else 'complete'
				#logDict['item'] = 'incomplete' if _personalInfoDict.get('complete',False) else 'complete'
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def getIsWaived(self, _jobTask, _taskCode, _waiverCode,_waiverAffirmativeResponse):
		question = self.getQuestionsAndOptionsForTask(_taskCode,_waiverCode)
		if question:
			response = sql.getResponseToSingleQuestion(self.connection,_jobTask.get('id',-1),question[0].get('id',-1))
			if response:
				optionId = response[0].get('question_option_id',-1)
				for answer in question[0].get('options',{}):
					if answer.get('id',0) == optionId:
						if answer.get('option_text','') == _waiverAffirmativeResponse:
							return True
		return False