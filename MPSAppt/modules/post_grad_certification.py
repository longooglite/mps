# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSAppt.services.evaluationsService as evalSvc
import MPSAppt.services.jobActionResolverService as jaResolver
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.dateUtilities as dateUtils

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		packethandler = self.context.get('handler',None)
		content = None
		try:
			config = eval(self.config)
			templateName = config.get('template','')
			site = self.context.get('profile',{}).get('siteProfile',{}).get('site','')
			templatePath = self.buildFullPathToSiteTemplate(site, templateName)
			loader = packethandler.getEnvironment().getTemplateLoader()
			context = {}

			evaluatorKey = self.params['context']['handler'].path_kwargs.get('key','')
			evaluatorService = evalSvc.EvaluationsService(self.dbConnection)
			evaluatorDict = {}
			if evaluatorKey:
				evaluatorDict = evaluatorService.getEvaluatorByEmailKey(evaluatorKey)
			else:
				evalContainer = self.workflow.getContainer('postgrad_eval')
				if evalContainer:
					evalContainer.loadInstance()
					if evalContainer.evaluatorsList:
						evaluatorDict = evalContainer.evaluatorsList[0]

			jobAction = jaResolver.JobActionResolverService(self.dbConnection,self.context.get('profile',{}).get('siteProfile',{})).resolve(self.workflow.jobActionDict)
			person = jobAction.get('person',{})

			personalInfoDict = {}
			personalInfo = self.workflow.getContainer('cred_personalinfo')
			if personalInfo:
				personalInfoDict = personalInfo.getResponseCacheByIdentifierCode()

			context['lastNameFirst'] = stringUtils.constructLastCommaFirstName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''))
			context['firstNameLast'] = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''))
			context['aliases'] = personalInfoDict.get('aliases','')
			context['ssn'] = personalInfoDict.get('ssn','')
			genderPossessive = 'his/her'
			gender = personalInfoDict.get('gender','')
			if gender == 'Male':
				genderPossessive = 'his'
			elif gender == 'Female':
				genderPossessive = 'her'
			context['genderPossessive'] = genderPossessive
			if context['ssn']:
				parts = context['ssn'].split('*')
				lastFour = parts[len(parts)-1]
				context['ssn'] = 'XXX-XX-%s' % (lastFour)
			bdate = personalInfoDict.get('birth_date')
			if bdate:
				bdate = datetime.datetime.strptime(bdate,'%m/%d/%Y').strftime('%b %d, %Y')
			context['birth_date'] = bdate

			context['certificationHeader'] = 'CERTIFICATION OF POSTGRADUATE TRAINING FOR MEDICAL PRACTITIONERS'
			context['deanRegistrarHeader'] = 'TO BE COMPLETED BY THE DIRECTOR OF MEDICAL EDUCATION OR PROGRAM DIRECTOR'
			context['schoolType'] = 'medical school'

			context['address1'] = evaluatorDict.get('institution','')
			keyNum = 2
			for address in evaluatorDict.get('address_lines',[]):
				keyName = 'address%i' % (keyNum)
				context[keyName] = address
				keyNum += 1
			keyName = 'address%i' % (keyNum)
			context[keyName] = "%s, %s  %s" % (evaluatorDict.get('city',''),evaluatorDict.get('state',''),evaluatorDict.get('postal',''))

			keyNum += 1
			keyName = 'address%i' % (keyNum)
			country = lookupTableSvc.getStaticLookupDiscreteValue(self.dbConnection, 'COUNTRIES', evaluatorDict.get('country',''))
			context[keyName] = ''
			if country:
				context[keyName] = country.get('descr','')

			context['department'] = ''
			candidate_info = self.workflow.getContainer('cred_cand_info')
			if candidate_info:
				candidateInfoDict = candidate_info.getResponseCacheByIdentifierCode()
				context['department'] = candidateInfoDict.get('PRIMARY_PRIV_DEPT','')

			siteProfile = self.context.get('profile',{}).get('siteProfile',{})
			context['imagePath'] = self.buildFullPathToSiteTemplate(siteProfile.get('site',''),'logoUMHS.png')

			liabilityReleaseDict = {}
			liabilityReleaseContainer = self.workflow.getContainer('cred_release_statement')
			liabilityReleaseContainer.loadInstance()
			releasedOnStr = liabilityReleaseContainer.getAttestation().get('updated','')
			if releasedOnStr:
				releasedOnStr = datetime.datetime.strptime(releasedOnStr,dateUtils.kUTCDateFormat).strftime('%b %d, %Y')
			context['releaseDate'] = releasedOnStr
			template = loader.load(templatePath)
			html = template.generate(context=context, skin={})
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.env, setFooter=False, prefix = 'servrank',portrait = True, includeFooterTime=False)
			path = pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
			f = open(fullPath,'rb')
			content = bytearray(f.read())
			f.close()
			return {"descr":"CERT","content":content,"pages":1}


		except Exception,e:
			pass
		#artifacts responsible for returning these 3 values
