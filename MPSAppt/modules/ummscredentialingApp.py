# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.services.uberDisplayService as uberDisplaySvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.personService as personSvc
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.uberResolverService as uberReolverSvc

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		descr = ''
		content = None
		pages = 0
		try:
			config = eval(self.config)
			cred_personalinfo = self.workflow.getContainer('cred_personalinfo')
			cred_edu_training = self.workflow.getContainer('cred_edu_training')
			cred_work_experience = self.workflow.getContainer('cred_work_experience')
			cred_board_cert = self.workflow.getContainer('cred_board_cert')
			cred_licensure = self.workflow.getContainer('cred_licensure')
			cred_prof_liability = self.workflow.getContainer('cred_prof_liability')
			cred_suppl_questions = self.workflow.getContainer('cred_suppl_questions')
			candidate_info_container = self.workflow.getContainer('cred_cand_info')
			candidate_info_container.loadInstance()
			candidate_info_container.applyResponses()
			questionsByIdentifierCodeCache = candidate_info_container.organizeQuestionsByIdentifierCode()
			primaryDepartmentQuestion = questionsByIdentifierCodeCache.get('PRIMARY_PRIV_DEPT','')
			department = ''
			if primaryDepartmentQuestion:
				department = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(primaryDepartmentQuestion)


			socialSecurityPerm = None
			if self.context.get('handler').hasPermission('canViewSocialSecurity'):
				socialSecurityPerm = ['PI_SSN']
			uberDisplay = uberDisplaySvc.UberDisplayService(self.dbConnection,socialSecurityPerm)
			personalInfo = uberDisplay.getContent(cred_personalinfo,{})
			edu_training = uberDisplay.getContent(cred_edu_training,{})
			self.removeTable(edu_training,'credEduTrainingTable')
			work_experience = uberDisplay.getContent(cred_work_experience,{})
			self.removeTable(work_experience,'credWorkExpTable')
			board_cert = uberDisplay.getContent(cred_board_cert,{})
			self.removeTable(board_cert,'credBoardCertTable')
			licensure = uberDisplay.getContent(cred_licensure,{})
			self.removeTable(licensure,'credLicensureTable')
			prof_liability = uberDisplay.getContent(cred_prof_liability,{})
			self.removeTable(prof_liability,'credLiabilityInsuranceTable')
			suppl_questions = uberDisplay.getContent(cred_suppl_questions,{})
			removeQuestions = ['PI_LIVING_IN_US',
		           'PI_HAS_SSN',
		           'PI_SCHOLARLY_FOCUS',
		           'PI_ETHNICITY',
		           'PI_NAME_MATCH']
			self.removeQuestions(personalInfo,removeQuestions)
			self.removeSection(personalInfo,'piHighDegreeSection')

			personalInfoContainer = self.workflow.getContainer('cred_personalinfo')
			personalInfoContainer.loadInstance()
			personalInfoContainer.applyResponses()
			questionsByIdentifierCodeCache = personalInfoContainer.organizeQuestionsByIdentifierCode()
			degreeCode = ''
			degreeDescr = ''
			degreeQuestion = questionsByIdentifierCodeCache.get('hd_degree','')
			if degreeQuestion:
				if degreeQuestion.get('responseList',[]):
					degreeRow = degreeQuestion.get('responseList',[])[0]
					if degreeRow:
						degreeData = degreeRow.get('response','')
						splits = degreeData.split('|')
						if len(splits) == 2:
							degreeCode = splits[1]
				degree = lookupTableSvc.getStaticLookupDiscreteValue(self.dbConnection,'DEGREES',degreeCode)
				if degree:
					degreeDescr = degree.get('descr','')
			context = {}
			jobAction = self.workflow.getJobActionDict()
			person = personSvc.PersonService(self.dbConnection).getPerson(jobAction.get('person_id',None))
			candidateName = ''
			if person:
				candidateName = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			if degreeDescr and candidateName:
				context['candidateName'] = '%s, %s' % (candidateName,degreeDescr)

			self.addUserNameToPersonalInfo(person.get('username',''),personalInfo)
			npiContainer = self.workflow.getContainer('npi')
			if npiContainer:
				npiContainer.loadInstance()
				self.addNPIToPersonalInfo(npiContainer.npiDict.get('npi_nbr',''),personalInfo)

			headeImageURL = ''
			headerImage = config.get('header_image','')
			if headerImage:
				sitePreferences = self.params.get('context',{}).get('profile',{}).get('siteProfile',{})
				appCode = envUtils.getEnvironment().getAppCode()
				skin = sitePreferences.get('skin', 'default')
				headeImageURL = self._resolveImageURL(appCode, skin, headerImage, self.params.get('workflow'), True)

			forms = []
			forms.append({"header":cred_personalinfo.getDescr(),"uberContent":personalInfo})
			forms.append({"header":cred_edu_training.getDescr(),"uberContent":edu_training})
			forms.append({"header":cred_work_experience.getDescr(),"uberContent":work_experience})
			forms.append({"header":cred_board_cert.getDescr(),"uberContent":board_cert})
			forms.append({"header":cred_licensure.getDescr(),"uberContent":licensure})
			forms.append({"header":cred_prof_liability.getDescr(),"uberContent":prof_liability})
			forms.append({"header":cred_suppl_questions.getDescr(),"uberContent":suppl_questions})
			context['forms'] = forms
			context['header_image_url'] = headeImageURL
			context['department'] = department
			loader = self.templateLoader
			templatePath = self.buildFullPathToSiteTemplate(config.get("site",""), config.get("template",""))
			template = loader.load(templatePath)
			html = template.generate(context=context, skin={})
			footer = candidateName
			if degreeDescr:
				footer = '%s, %s' % (candidateName,degreeDescr)
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.env, setFooter=True, prefix = 'credapp_',includeFooterTime=True, name = footer)
			if fullPath:
				pages = pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
				descr = 'Credentialing Application'
				f = open(fullPath,'rb')
				content = bytearray(f.read())
				f.close()

		except Exception,e:
			pass
		#   Artifacts are responsible for returning these 3 values
		return { "descr":descr, "content":content, "pages":pages }

	def removeTable(self,uber,key):
		index = 0
		removalIndex = None
		for each in uber:
			if each.get('code','') == key:
				removalIndex = index
			index += 1
		if removalIndex <> None:
			del uber[removalIndex]

	def removeQuestions(self,personalInfo,prompts):
		removalIndexes = []
		for section in personalInfo:
			counter = 0
			for item in section.get('items',[]):
				if item.get('code','') in prompts:
					removalIndexes.append(counter)
				counter += 1
			sortedList = sorted(removalIndexes, reverse=True)
			for index in sortedList:
				del section.get('items',[])[index]
			removalIndexes = []

	def removeSection(self,personalInfo,sectionCode):
		removalIndex = -1
		counter = 0
		for section in personalInfo:
			if section.get('code','') == sectionCode:
				removalIndex = counter
				break
			counter += 1
		if removalIndex > 0:
			del personalInfo[removalIndex]

	def addUserNameToPersonalInfo(self,uniqname,personalInfo):
		if personalInfo > 0:
			personalInfo[1].get('items',[]).append({'value':uniqname,'label':'UM Uniqname'})

	def addNPIToPersonalInfo(self,npiNumber,personalInfo):
		if personalInfo > 0:
			personalInfo[0].get('items',[]).append({'value':npiNumber,'label':'NPI Number'})
