# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSAppt.services.uberResolverService as uberReolverSvc
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.departmentService as departmentSvc
import json

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		content = None
		try:
			context = {}
			siteProfile = self.context.get('profile',{}).get('siteProfile',{})
			personalInfoContainer = self.workflow.getContainer('cred_personalinfo')
			personalInfoContainer.loadInstance()
			personalInfoContainer.applyResponses()
			questionsByIdentifierCodeCache = personalInfoContainer.organizeQuestionsByIdentifierCode()
			degreeQuestion = questionsByIdentifierCodeCache.get('hd_degree','')
			degree = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(degreeQuestion)
			firstNameQuestion = questionsByIdentifierCodeCache.get('first_name','')
			firstName = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(firstNameQuestion)
			lastNameQuestion = questionsByIdentifierCodeCache.get('last_name','')
			lastName = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(lastNameQuestion)
			middleNameQuestion = questionsByIdentifierCodeCache.get('middle_name','')
			middleName = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(middleNameQuestion)
			suffixQuestion = questionsByIdentifierCodeCache.get('suffix','')
			suffix = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(suffixQuestion)
			candidate_info_container = self.workflow.getContainer('cred_cand_info')
			candidate_info_container.loadInstance()
			candidate_info_container.applyResponses()
			questionsByIdentifierCodeCache = candidate_info_container.organizeQuestionsByIdentifierCode()
			primaryDepartmentQuestion = questionsByIdentifierCodeCache.get('PRIMARY_PRIV_DEPT','')
			department = ''
			if primaryDepartmentQuestion:
				department = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(primaryDepartmentQuestion)
			context['department'] = department
			fullName = stringUtils.constructFullName(firstName,lastName,middleName,suffix)
			context['nameAndDegree'] = fullName + ', ' + degree
			context['hasJointDepartments'] = False
			context['jointDepartment'] = ''
			secondaryDepartment = ''
			secondaryDepartmentQuestion = questionsByIdentifierCodeCache.get('SECONDARY_PRIV_DEPT','')
			if secondaryDepartmentQuestion:
				secondaryDepartment = uberReolverSvc.UberResolverService(self.dbConnection,{}).resolve(secondaryDepartmentQuestion)
			if secondaryDepartment:
				context['hasJointDepartments'] = True
				context['jointDepartment'] = secondaryDepartment
			servrankcontainer = self.workflow.getContainer('enter_serv_rank')
			servrankcontainer.loadInstance()
			imageName = servrankcontainer.getConfigDict().get('image','')
			context['imagePath'] = self.buildFullPathToSiteTemplate(siteProfile.get('site',''),imageName)
			templateName = servrankcontainer.getConfigDict().get('template','')
			loader = self.templateLoader
			templatePath = self.buildFullPathToSiteTemplate(siteProfile.get('site',''),templateName)
			template = loader.load(templatePath)
			serviceAndRankDict = servrankcontainer.serviceAndRankDict
			formatted_address = self.formatAddress(serviceAndRankDict)
			context['formatted_address_lines'] = formatted_address
			context['phone'] = serviceAndRankDict.get('phone','')
			titles = self.context.get('titles',[])
			context['title'] = ''
			if titles:
				context['title'] = titles[0]

			rawStartDate = self.workflow.jobActionDict.get('proposed_start_date', '')
			context['clinical_start'] = rawStartDate
			if rawStartDate:
				format = siteProfile.get('sitePreferences', {}).get('ymdformat', '%m/%d/%Y')
				context['clinical_start'] = dateUtils.parseUTCDateOnly(rawStartDate).strftime(format)
			context['email'] = serviceAndRankDict.get('email','')
			context['fax'] = serviceAndRankDict.get('fax','')
			context['membership_category'] = self.getMembershipCategory(serviceAndRankDict.get('membership_category'),servrankcontainer.getConfigDict().get('membershipCategories',[]))
			departmentid = self.workflow.department.get('id',-1)
			chair = departmentSvc.DepartmentService(self.dbConnection).getDepartmentChair(departmentid)
			context['department_contact'] = ''
			if chair:
				context['department_contact'] = chair.get('chair_with_degree','')

			context['today'] = datetime.datetime.now().strftime("%m/%d/%Y")

			html = template.generate(context=context, skin={})
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.env, setFooter=True, prefix = 'servrank',portrait = True, includeFooterTime=True)
			path = pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
			f = open(fullPath,'rb')
			content = bytearray(f.read())
			f.close()

		except Exception,e:
			pass
		#artifacts responsible for returning these 3 values
		return {"descr":"serv_rank","content":content,"pages":1}

	def getMembershipCategory(self,catCode,membershipCategories):
		for aDict in membershipCategories:
			if aDict.get('code','') == catCode:
				return aDict.get('descr','')
			for subDict in aDict.get('subcategories',[]):
				if subDict.get('code',None) == catCode:
					return subDict.get('descr','')
		return ''

	def formatAddress(self, srDict):
		address = []
		if srDict.get('address_lines',''):
			srDict['address_lines'] = json.loads(srDict['address_lines'])
		else:
			srDict['address_lines'] = ['']
		lineNbr = 1
		for addressLine in srDict.get('address_lines',''):
			if lineNbr == 2:
				if srDict.get('floor',''):
					addressLine += ' Floor %s' % (srDict.get('floor',''))
				if srDict.get('reception',''):
					addressLine += ' Reception %s' % (srDict.get('reception',''))
				if srDict.get('room',''):
					addressLine += ' Rm %s' % (srDict.get('room',''))
			elif lineNbr == 3:
				if srDict.get('spc',''):
					addressLine += ' SPC %s' % (srDict.get('spc',''))

			address.append(addressLine)
			lineNbr += 1
		address.append(srDict.get('city','') + ', ' + srDict.get('state','') + '  ' + srDict.get('postal',''))
		return address
