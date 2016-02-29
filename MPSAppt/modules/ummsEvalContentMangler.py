# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.jobActionResolverService as jaResolver
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.lookupTableService as lookupTableSvc

class UberContentMangler:
	def mangleContent(self,_dbConnection,_context,_container,_evaluatorId):
		_container.loadInstance()
		workflow = _container.workflow

		siteProfile = {}
		jobAction = jaResolver.JobActionResolverService(_dbConnection,siteProfile).resolve(workflow.jobActionDict)
		person = jobAction.get('person',{})

		personalInfoDict = {}
		personalInfo = workflow.getContainer('cred_personalinfo')
		if personalInfo:
			personalInfoDict = personalInfo.getResponseCacheByIdentifierCode()

		lastNameFirst = stringUtils.constructLastCommaFirstName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
		firstNameLast = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
		aliases = personalInfoDict.get('aliases','')
		ssn = personalInfoDict.get('ssn','')
		genderPossessive = 'his/her'
		gender = personalInfoDict.get('gender','')
		if gender == 'Male':
			genderPossessive = 'his'
		elif gender == 'Female':
			genderPossessive = 'her'
		genderPossessive = genderPossessive
		if ssn:
			parts = ssn.split('*')
			lastFour = parts[len(parts)-1]
			ssn = 'XXX-XX-%s' % (lastFour)
		bdate = personalInfoDict.get('birth_date')
		if bdate:
			bdate = datetime.datetime.strptime(bdate,'%m/%d/%Y').strftime('%b %d, %Y')
		birth_date = bdate

		liabilityReleaseContainer = workflow.getContainer('cred_release_statement')
		liabilityReleaseContainer.loadInstance()
		releasedOnStr = liabilityReleaseContainer.getAttestation().get('updated','')
		if releasedOnStr:
			releasedOnStr = datetime.datetime.strptime(releasedOnStr,dateUtils.kUTCDateFormat).strftime('%b %d, %Y')
		releaseDate = releasedOnStr

		evaluatorDict = self.getEvaluatorDict(_evaluatorId,_container)

		addressList = []
		addressList.append(evaluatorDict.get('institution',''))
		for address in evaluatorDict.get('address_lines',[]):
			if address:
				addressList.append(address)
		cityStateZip = "%s, %s  %s" % (evaluatorDict.get('city',''),evaluatorDict.get('state',''),evaluatorDict.get('postal',''))
		addressList.append(cityStateZip)
		country = lookupTableSvc.getStaticLookupDiscreteValue(_dbConnection, 'COUNTRIES', evaluatorDict.get('country',''))
		if country:
			addressList.append(country.get('descr',''))

		institutionAddressTable = "<table>"
		for each in addressList:
			institutionAddressTable += '''<tr><td>%s</td></tr>''' % (each)
		institutionAddressTable += '</table>'

		admissionDate = ''
		if evaluatorDict.get('admission_date',''):
			admissionDate = datetime.datetime.strptime(evaluatorDict.get('admission_date',''),'%Y-%m-%d').strftime('%b %d, %Y')

		applicantInfoTable = '<table>'
		applicantInfoTable += '''<tr><td><b>Applicant's Name:</b> %s</td></tr>'''% (lastNameFirst)
		applicantInfoTable += '''<tr><td><b>Other Name:</b> %s</td></tr>'''% (aliases)
		applicantInfoTable += '''<tr><td><b>Social Security Number:</b> %s</td></tr>'''% (ssn)
		applicantInfoTable += '''<tr><td><b><b>Birth Date:</b> %s</td></tr>'''% (birth_date)
		applicantInfoTable += '''<tr><td><b>Date of Admission:</b> %s</td></tr>'''% (admissionDate)
		applicantInfoTable += '</table>'

		certificationHeader = '<b><u><center>CERTIFICATION OF MEDICAL EDUCATION FOR MEDICAL SCHOOL GRADUATES</center></b></u>'
		deanRegistrarHeader = '<b><u><center>THIS SECTION TO BE COMPLETED BY THE DEAN OR REGISTRAR OF MEDICAL SCHOOL</center></b></u>'
		schoolCert = '''I certify that %s attended the medical school named above from''' % (lastNameFirst)

		guidoGood = '''On %s, %s released from liability all individuals and organizations that provide information concerning %s qualifications for staff appointments and clinical priveleges.''' % (releaseDate,lastNameFirst,genderPossessive)
		if evaluatorDict.get('program','') == 'OptometrySchool':
			certificationHeader = '<b><u><center>CERTIFICATION OF EDUCATION COMPLETION OF DOCTORATE DEGREE FOR OPTOMETRISTS</center></b></u>'
			deanRegistrarHeader = '<b><u><center>THIS SECTION TO BE COMPLETED BY THE DEAN OR REGISTRAR OF SCHOOL WHERE EDUCATION WAS COMPLETED</center></b></u>'
			schoolCert = '''I certify that %s attended the school named above from''' % (lastNameFirst)
		elif evaluatorDict.get('program','') == 'DentalSchool':
			certificationHeader = '<b><u><center>CERTIFICATION OF DENTAL EDUCATION FOR DENTAL SCHOOL GRADUATES</center></b></u>'
			deanRegistrarHeader = '<b><u><center>THIS SECTION TO BE COMPLETED BY THE DEAN OR REGISTRAR OF DENTAL SCHOOL</center></b></u>'
			schoolCert = '''I certify that %s attended the dental school named above from''' % (lastNameFirst)
		elif evaluatorDict.get('program','') == 'DoctoralProgramPhDPsyD':
			certificationHeader = '<b><u><center>CERTIFICATION OF EDUCATION COMPLETION OF DOCTORATE DEGREE FOR PSYCHOLOGISTS</center></b></u>'
			deanRegistrarHeader = '<b><u><center>THIS SECTION TO BE COMPLETED BY THE DEAN OR REGISTRAR OF SCHOOL WHERE EDUCATION WAS COMPLETED</center></b></u>'
			schoolCert = '''I certify that %s attended the school named above from''' % (lastNameFirst)

		uber = _context.get('uber_instance',{})
		if uber:
			questions = uber.get('questions',{})
			for element in questions.get('elements',{}):
				elementCode = element.get('code','')
				if elementCode == 'edPostGradOpeningBlurb':
					element['display_text'] = '</br>'+certificationHeader
				elif elementCode == 'edPostGuidoGood':
					element['display_text'] = guidoGood
				elif elementCode == 'edPostApplicantInfo':
					element['display_text'] = applicantInfoTable
				elif elementCode == 'edPostDeanComplete':
					element['display_text'] = deanRegistrarHeader
				elif elementCode == 'edPostEvaluatorWrapper':
					for wrappedElement in element.get('elements',{}):
						subElementCode = wrappedElement.get('code','')
						if subElementCode == 'edPostInstAddress':
							wrappedElement['display_text'] = institutionAddressTable
						elif subElementCode == 'EDPOSTCERTIFY':
							wrappedElement['display_text'] = schoolCert

		uberContent = _context.get('uberContent',{})
		if uberContent:
			for element in uberContent:
				elementCode = element.get('code','')
				if elementCode == 'edPostGradOpeningBlurb':
					element['groupdescr'] = '</br>'+certificationHeader
				elif elementCode == 'edPostGuidoGood':
					element['groupdescr'] = '</br>'+guidoGood
				elif elementCode == 'edPostApplicantInfo':
					element['groupdescr'] = '</br>'+applicantInfoTable
				elif elementCode == 'edPostDeanComplete':
					element['groupdescr'] = '</br>'+deanRegistrarHeader
				elif elementCode == 'edPostEvaluatorWrapper':
					element['groupdescr'] = '</br>'+institutionAddressTable+'</br>'
					for wrappedElement in element.get('items',{}):
						subElementCode = wrappedElement.get('code','')
						if subElementCode == 'edPostInstAddress':
							wrappedElement['groupdescr'] = institutionAddressTable
						elif subElementCode == 'EDPOSTCERTIFY':
							wrappedElement['groupdescr'] = schoolCert



	def getEvaluatorDict(self,id,container):
		for evaluator in container.evaluatorsList:
			if evaluator.get('id',-1) == int(id):
				return evaluator
		return {}