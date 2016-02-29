# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.jobActionResolverService as jaResolver
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.uberDisplayService as uberDisplaySvc

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		content = None
		try:
			siteProfile = self.params.get('context',{}).get('profile',{}).get('siteProfile',{})
			resolvedJobAction = jaResolver.JobActionResolverService(self.dbConnection,siteProfile).resolve(self.workflow.getJobActionDict())
			context = {}
			siteProfile = self.context.get('profile',{}).get('siteProfile',{})
			templateName = 'umms_provider_enrollment_info.html'
			loader = self.templateLoader
			templatePath = self.buildFullPathToSiteTemplate(siteProfile.get('site',''),templateName)
			template = loader.load(templatePath)

			socialSecurityPerm = None
			if self.context.get('handler').hasPermission('canViewSocialSecurity'):
				socialSecurityPerm = ['PI_SSN']

			personalInfoContainer = self.workflow.getContainer('enroll_personalinfo')
			pInfoAnswers = personalInfoContainer.getResponseCacheByIdentifierCode(_doNotMaskUberCodes = socialSecurityPerm)

			npiContainer = self.workflow.getContainer('npi')
			npiContainer.loadInstance()
			npiData = npiContainer.getNPI()

			candidateInfoContainer = self.workflow.getContainer('enroll_cand_info')
			candidateInfoAnswers = candidateInfoContainer.getResponseCacheByIdentifierCode()

			context['today'] = datetime.datetime.now().strftime("%m/%d/%Y")
			lastNameFirst = stringUtils.constructLastCommaFirstName(pInfoAnswers.get('first_name',''),pInfoAnswers.get('last_name',''))
			context['candidate_name'] = lastNameFirst
			legalName = stringUtils.constructLastCommaFirstName(pInfoAnswers.get('first_name',''),pInfoAnswers.get('last_name',''),pInfoAnswers.get('middle_name',''))
			context['legal_name'] = legalName
			context['position_type'] = 'Faculty'  # We don't have this information
			context['department'] = resolvedJobAction.get('department',{}).get('full_descr','')
			context['position'] = resolvedJobAction.get('title',{}).get('descr','')
			contact = ''
			contact_email = ''
			department = resolvedJobAction.get('department',{})
			rawEmails = department.get('email_address','')
			emailSplit = rawEmails.split(',')
			if emailSplit:
				emailParts = emailSplit[0].split('@')
				if emailParts:
					contact = emailParts[0]
					contact_email = emailSplit[0]
			context['contact_email'] = contact_email
			context['imagePath'] = self.buildFullPathToSiteTemplate(siteProfile.get('site',''),'blockM.jpg')
			context['department_contact'] = contact
			context['birth_date'] = pInfoAnswers.get('birth_date','')
			context['proposed_start_date'] = resolvedJobAction.get('job_action',{}).get('proposed_start_date','')
			context['uniqname'] = resolvedJobAction.get('person',{}).get('username','')
			context['email_address'] = resolvedJobAction.get('person',{}).get('email','')
			context['phone_number'] = pInfoAnswers.get('address_hom_phone','')
			context['correct_name'] = pInfoAnswers.get('name_match','')
			context['ssn'] = pInfoAnswers.get('ssn','')
			context['currently_credentialed'] = candidateInfoAnswers.get('ENROLL_CURRENTLY_CREDENTIALED','')
			context['need_credentialing'] = candidateInfoAnswers.get('ENROLL_NEED_CREDENTIALING','')
			context['on_billing_track'] = candidateInfoAnswers.get('ON_BILLING_TRACK','')
			npi_password = npiData.get('npi_password','')
			context['npi_number'] = npiData.get('npi_nbr','')
			context['npi_user_name'] = npiData.get('npi_username','')
			context['npi_password'] = npi_password
			npi_form_sent_date = ''
			raw_sent_str = npiData.get('updated','')
			if raw_sent_str:
				ts = dateUtils.localizeUTCDate(raw_sent_str)
				npi_form_sent_date = dateUtils.parseDate(ts,"%m/%d/%Y")
			context['npi_form_sent_date'] = npi_form_sent_date
			fpscDict = lookupTableSvc.getStaticLookupDiscreteValue(self.dbConnection,'FPSC',candidateInfoAnswers.get('FPSC',''),"descr")
			if fpscDict:
				context['fpsc_code'] = "%s (%s)" % (fpscDict.get('descr'),fpscDict.get('code'))
			else:
				context['fpsc_code'] = candidateInfoAnswers.get('FPSC','')

			html = template.generate(context=context, skin={})
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.env, setFooter=False, prefix = 'pei_',portrait = True, includeFooterTime=False)
			pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
			f = open(fullPath,'rb')
			content = bytearray(f.read())
			f.close()

		except Exception,e:
			pass
		#artifacts responsible for returning these 3 values
		return {"descr":"provider_enrollment_info","content":content,"pages":1}
