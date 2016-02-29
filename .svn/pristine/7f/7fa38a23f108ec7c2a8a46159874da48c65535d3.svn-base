# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.placeholderService as placeholderSvc
import MPSAppt.services.qaService as qaSVC
import MPSAppt.services.personService as personSvc
import MPSAppt.services.fileRepoService as fRepoSvc
import MPSAppt.services.approvalService as approvalSvc
import MPSAppt.services.evaluationsService as evalSvc
import MPSAppt.services.jobPostingService as jobPostingSvc
import MPSAppt.services.confirmTitleService as confirmTitleSvc
import MPSAppt.services.attestService as attestSvc
import MPSAppt.services.npiService as npiSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.disclosureService as disclosureSvc
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.backgroundCheckService as backgroundCheckSvc
import MPSCore.utilities.dateUtilities as dateUtils

kBackgroundCheckMap = {
	constants.kBackgroundCheckStatusSubmitted: 'handleSubmit',
	constants.kBackgroundCheckStatusSubmittedError: 'handleSubmissionError',
	constants.kBackgroundCheckStatusAccepted: 'handleAccept',
	constants.kBackgroundCheckStatusAcceptedWithFindings: 'handleAcceptWithFindings',
	constants.kBackgroundCheckStatusRejected: 'handleReject',
	constants.kBackgroundCheckStatusInProgress: 'handleInProgress',
	constants.kBackgroundCheckStatusComplete: 'handleComplete',
	constants.kBackgroundCheckStatusWaived: 'handleWaive',
}


class AutofillService:
	def __init__(self,_dbconnection,_autofillConnection,_profile):
		self.profile = _profile
		self.connection = _dbconnection
		self.autofillConnection = _autofillConnection
		self.autofillJASvc = jobActionSvc.JobActionService(self.autofillConnection)
		self.jaSvc = jobActionSvc.JobActionService(self.connection)
		self.now = dateUtils.formatUTCDate()
		self.username = 'autofilled'

	def autofill(self,fromJobActionId,toJobActionId,taskcodeList):
		try:
			fromJobAction = self.autofillJASvc.getJobAction(fromJobActionId)
			if not fromJobAction:
				return

			toJobAction = self.jaSvc.getJobAction(toJobActionId)
			if not toJobAction:
				return

			for taskcode in taskcodeList:
				fromJobAction = self.autofillJASvc.getJobAction(fromJobActionId)
				fromWorkflow = workflowSvc.WorkflowService(self.autofillConnection).getWorkflowForJobAction(fromJobAction, self.profile.get('userProfile',{}))
				fromContainer = fromWorkflow.getContainer(taskcode)

				toJobAction = self.jaSvc.getJobAction(toJobActionId)
				toWorkflow = workflowSvc.WorkflowService(self.connection).getWorkflowForJobAction(toJobAction, self.profile.get('userProfile',{}))
				toContainer = toWorkflow.getContainer(taskcode)

				if (fromContainer) and (toContainer):
					fromClassName = fromContainer.getContainerDict().get('className','')
					toClassName = toContainer.getContainerDict().get('className','')
					if fromClassName == toClassName:
						if fromClassName == 'FileUpload':
							self.autofillFileUpload(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'QA':
								self.autofillQA(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'Submit':
							self.autofillSubmit(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'SubmitBackgroundCheck':
							self.autofillSubmit(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'Approval':
							self.autofillApproval(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'Placeholder':
							self.autofillPlaceHolder(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'Attest':
							self.autofillAttest(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'Evaluations':
							self.autofillEvaluations(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'Disclosure':
							self.autofillDisclosure(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'PersonalInfoSummary':
							self.autofillPersonalInfoSummary(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'NPI':
							self.autofillNPI(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'JobPosting':
							self.autofillJobPosting(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'IdentifyCandidate':
							self.autofillIdentifyCandidate(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'ConfirmTitle':
							self.autofillConfirmTitle(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'UberForm':
							self.autofillUberForm(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)
						elif fromClassName == 'BackgroundCheck':
							self.autofillBackgroundCheck(fromJobAction,toJobAction,taskcode,fromContainer,toContainer)

		except Exception,e:
			pass

	def autofillFileUpload(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		fAutoRepo = fRepoSvc.FileRepoService(self.autofillConnection)
		fRepo = fRepoSvc.FileRepoService(self.connection)
		fuploads = fAutoRepo.getFileRepoForJobAction(fromJobAction.get('id',-1))
		if fuploads:
			toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
			for fupload in fuploads:
				if fupload.get('task_code','') == taskcode:
					content = fAutoRepo.getFileRepoContentForVersion(jobTaskDict,fupload.get('seq_nbr',-1),fupload.get('version_nbr',-1))
					if content:
						fupload['content'] = content.get('content','')
						fupload['pdf_version_nbr'] = ''
						fupload['job_task_id'] = toJobTask.get('id',-1)
						fRepo.handleUpload(toJobAction, toJobTask, fupload, toContainer, self.profile, self.now, self.username,True)

	def autofillQA(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		qaService = qaSVC.QAService(self.connection)
		qaAutoService = qaSVC.QAService(self.autofillConnection)
		questions = qaAutoService.getQuestionsAndOptionsForTask(taskcode)
		qas = qaAutoService.getResponsesToQuestions(jobTaskDict.get('id',-1),taskcode)
		if qas:
			qaList = []
			for qp in questions:
				response = qas.get(qp.get('id',-1))
				if response:
					options = qp.get('options',[])
					if options:
						for opt in options:
							if opt.get('id',-1) == response.get('question_option_id',-1):
								qaItem = self.getNewQAItem(taskcode,qp.get('code',''),self.now,self.username)
								qaItem['optioncode'] = opt.get('code','')
								qaItem['textresponse'] = response.get('text_response','')
								qaList.append(qaItem)
								break
					else:
						qaItem = self.getNewQAItem(taskcode,qp.get('code',''),self.now,self.username)
						qaItem['textresponse'] = response.get('text_response','')
						qaList.append(qaItem)

			newJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
			qaService.handleSubmit(toJobAction, newJobTask, qaList, toContainer, self.profile, self.now, self.username, True)


	def getNewQAItem(self,taskCode,questioncode,now,username):
		return {"taskcode":taskCode,"questioncode":questioncode,"optioncode":"","textresponse":"","created":now,"updated":now,"lastuser":username}

	def autofillSubmit(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		approvalAuto_svc = approvalSvc.ApprovalService(self.autofillConnection)
		approval_svc = approvalSvc.ApprovalService(self.connection)
		submittal = approvalAuto_svc.getApproval(jobTaskDict.get('id',-1))
		if submittal:
			newJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
			submittal['job_task_id'] = newJobTask.get('id',0)
			approval_svc.handleSubmit(toJobAction,newJobTask,submittal,toContainer,self.profile,submittal,self.now,self.username)

	def autofillApproval(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		approvalAuto_svc = approvalSvc.ApprovalService(self.autofillConnection)
		approval_svc = approvalSvc.ApprovalService(self.connection)
		approval = approvalAuto_svc.getApproval(jobTaskDict.get('id',None))
		if approval:
			newJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
			approval['job_task_id'] = newJobTask.get('id',0)
			approval_svc.handleApprove(toJobAction,newJobTask,approval,toContainer,self.profile,approval,self.now,self.username)

	def autofillPlaceHolder(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		placeholderAuto_svc = placeholderSvc.PlaceholderService(self.autofillConnection)
		pholder = placeholderAuto_svc.getPlaceholder(jobTaskDict.get('id',None))
		placeholder_svc = placeholderSvc.PlaceholderService(self.connection)
		if pholder:
			newJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
			pholder['job_task_id'] = newJobTask.get('id',0)
			placeholder_svc.handleSubmit(toJobAction,newJobTask,pholder,toContainer,self.profile,self.now,self.username)

	def autofillAttest(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		attestAuto_svc = attestSvc.AttestService(self.autofillConnection)
		attest = attestAuto_svc.getAttestation(jobTaskDict.get('id',-1))
		attest_svc = attestSvc.AttestService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		attest['id'] = None
		attest['job_task_id'] = toJobTask.get('id',-1)
		attest_svc.handleSubmit(toJobAction,toJobTask,attest,toContainer,self.profile,self.now,self.username)

	def autofillEvaluations(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		fromjobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		evalAuto_svc = evalSvc.EvaluationsService(self.autofillConnection)
		fAutoRepo = fRepoSvc.FileRepoService(self.autofillConnection)
		fRepo = fRepoSvc.FileRepoService(self.connection)

		evals = evalAuto_svc.getEvaluatorsList(fromjobTaskDict.get('id',-1))
		eval_svc = evalSvc.EvaluationsService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		for each in evals:
			each['id'] = None
			each['job_task_id'] = toJobTask.get('id',-1)
			eval_svc.handleAddEditEvaluator(toJobAction,toJobTask,each,toContainer,self.profile,each,self.now,self.username)
			each['id'] = self.getEvalId(each,toJobTask)
			fupload = fAutoRepo.getFileRepo(fromjobTaskDict,each.get('uploaded_file_repo_seq_nbr',-1))
			if fupload:
				fupload['id'] = None
				fupload['pdf_version_nbr'] = ''
				fupload['job_task_id'] = toJobTask.get('id',-1)
				fRepo.handleUpload(toJobAction,toJobTask,fupload,toContainer,self.profile,self.now,self.username)
				eval_svc.handleFileUpload(toJobAction,toJobTask,each,toContainer,self.profile,each,self.now,self.username)
			eval_svc.handleApproveDenyEvaluator(toJobAction,toJobTask,each,toContainer,self.profile,each,self.now,self.username)

	def getEvalId(self,evaluator,toJobTask):
		sql = "select * from wf_evaluator where first_name = %s and last_name = %s and job_task_id = %s"
		args = (evaluator.get('first_name',''),evaluator.get('last_name',''),toJobTask.get('id',-1))
		qry = self.connection.executeSQLQuery(sql,args)
		if qry:
			return qry[0]['id']
		return None

	def autofillDisclosure(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		disclosurerAuto_svc = disclosureSvc.DisclosureService(self.autofillConnection)
		disclosure = disclosurerAuto_svc.getDisclosure(jobTaskDict.get('id',-1))
		disclosure_svc = disclosureSvc.DisclosureService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		disclosure['job_task_id'] = toJobTask.get('id',-1)
		disclosure_svc.handleSubmit(toJobAction,toJobTask,disclosure,toContainer,self.profile,self.now,self.username)

	def autofillPersonalInfoSummary(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		self.autofillAttest(fromJobAction, toJobAction, taskcode, fromContainer, toContainer)

	def autofillNPI(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		npiAuto_svc = npiSvc.NPIService(self.autofillConnection)
		npi = npiAuto_svc.getNPI(jobTaskDict.get('id',-1))
		npi_svc = npiSvc.NPIService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		npi['jobTaskId'] = toJobTask.get('id',-1)
		npi['id'] = None
		npi_svc.handleSubmit(toJobAction,toJobTask,npi,toContainer,self.profile,self.now,self.username)

	def autofillJobPosting(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		jobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		jpAuto_svc = jobPostingSvc.JobPostingService(self.autofillConnection)
		posting = jpAuto_svc.getJobPosting(jobTaskDict.get('id',-1))
		jp_svc = jobPostingSvc.JobPostingService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		posting['job_task_id'] = toJobTask.get('id',-1)
		jp_svc.handleSubmit(toJobAction,toJobTask,posting,toContainer,self.profile)


	def autofillIdentifyCandidate(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		personAuto_svc = personSvc.PersonService(self.autofillConnection)
		person = personAuto_svc.getPerson(fromJobAction.get('person_id',-1))
		community = person.get('community', 'default')
		uniqname = person.get('username','')
		prompts = toContainer.containerDict.get('config',{}).get('prompts',[])
		saveUsername = False
		for p in prompts:
			if p.get('code','') == 'username' and p.get('enabled',True):
				saveUsername = True
		person_svc = personSvc.PersonService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		addedperson = person_svc.getPerson(toJobAction.get('person_id',-1))
		if addedperson:
			person = addedperson
		else:
			person['id'] = None
		if not saveUsername:
			person['username'] = ''
		else:
			person['community'] = community
			person['username'] = uniqname
			person_svc.createOrUpdatePerson(toJobTask,person,True)

		reloadedToJobAction = self.jaSvc.getJobAction(toJobAction.get('id', 0))
		reloadedPersonId = reloadedToJobAction.get('person_id', 0)
		if reloadedPersonId:
			reloadedPerson = person_svc.getPerson(reloadedPersonId)
		else:
			reloadedPerson = person
		person_svc.handleIdentifyCandidate(reloadedToJobAction,toJobTask,reloadedPerson,toContainer,self.profile,self.now,self.username)

	def autofillConfirmTitle(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		fromjobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		ctAuto_svc = confirmTitleSvc.ConfirmedTitleService(self.autofillConnection)
		confirmedtitle = ctAuto_svc.getConfirmedTitle(fromjobTaskDict.get('id',-1))
		ct_svc = confirmTitleSvc.ConfirmedTitleService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		confirmedtitle['id'] = None
		confirmedtitle['job_task_id'] = toJobTask.get('id',-1)
		ct_svc.handleSubmit(toJobAction,toJobTask,confirmedtitle,toContainer,self.profile,self.now,self.username)

	def autofillUberForm(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		import json
		fromContainer.loadInstance()

		toContainer.setIsLoaded(False)
		toContainer.getWorkflow().clearJobTaskCache()
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction, toContainer, self.now,self.username)
		toContainer.loadInstance()

		insertList = []
		toJobTaskId = toJobTask.get('id', 0)
		fromResponses = fromContainer.getUberInstance().get('responses', {})
		for questionCode in fromResponses.keys():
			fromResponseList = fromResponses[questionCode]
			for fromResponseDict in fromResponseList:
				if type(fromResponseDict.get('response','')) == list:
					fromResponseDict['response'] = json.dumps(fromResponseDict.get('response',''))
				toResponseDict = fromResponseDict.copy()
				toResponseDict['job_task_id'] = toJobTaskId
				toResponseDict['created'] = self.now
				toResponseDict['updated'] = self.now
				toResponseDict['lastuser'] = self.username
				insertList.append(toResponseDict)

		uberSoivice = uberSvc.UberService(self.connection)
		uberSoivice.deleteUberResponsesForTask(toJobTask)
		uberSoivice.handleSubmit(toJobAction, toJobTask, insertList, [], [], toContainer, False, self.profile, self.now, self.username)

	def autofillBackgroundCheck(self, fromJobAction, toJobAction, taskcode, fromContainer, toContainer):
		fromJobTaskDict = self.autofillJASvc.getJobTask(fromJobAction,fromContainer)
		bcAuto_svc = backgroundCheckSvc.BackgroundCheckService(self.autofillConnection)
		backgroundcheck = bcAuto_svc.getBackgroundCheck(fromJobTaskDict.get('id',-1))

		bc_svc = backgroundCheckSvc.BackgroundCheckService(self.connection)
		toJobTask = self.jaSvc.getOrCreatePrimaryJobTask(toJobAction,toContainer,self.now,self.username)
		backgroundcheck['job_task_id'] = toJobTask.get('id',-1)
		qry = self.connection.executeSQLQuery("select max(id) as id from wf_background_check",())
		if qry:
			backgroundcheck['id'] = qry[0].get('id',-1)
		methodName = kBackgroundCheckMap.get(backgroundcheck.get('status', ''), None)
		if methodName:
			actionString = '''bc_svc.%s(toJobAction, toJobTask, backgroundcheck, toContainer, {}, {}, self.now, self.username)''' % methodName
			exec actionString
