# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.services.uberGapService as uberGapSvc
import MPSAppt.services.personService as personSvc
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.stringUtilities as stringUtils

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		descr = ''
		content = None
		pages = 0
		try:
			config = eval(self.config)
			task_code = config.get('task_code','')
			container = self.workflow.getContainer(task_code)
			if container:
				configKeyName = config.get('configKeyName','uberGapsConfig')
				uberGapsConfig = container.getConfigDict().get(configKeyName, [])

				if uberGapsConfig:
					gapSoivice = uberGapSvc.UberGapService(self.workflow.getConnection())
					sitePreferences = self.params.get('context', {}).get('profile', {}).get('siteProfile', {}).get('sitePreferences', {})
					gaps = gapSoivice.processContainer(container, sitePreferences, _configKeyName=configKeyName, _returnLocalizedDates=True)
					if gaps:
						context = {}
						context['gapsList'] = gaps
						context['header'] = config.get('header', '')
						context['introText'] = container.getConfigDict().get('uberGapsPrintIntroText', '')

						jobAction = self.workflow.getJobActionDict()
						person = personSvc.PersonService(self.dbConnection).getPerson(jobAction.get('person_id',None))
						if person:
							context['candidateName'] = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))

						loader = self.templateLoader
						templatePath = self.buildFullPathToSiteTemplate(config.get("site",""), config.get("template",""))
						template = loader.load(templatePath)
						html = template.generate(context=context, skin={})

						pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.env, setFooter=False, prefix = 'gaps_')
						if fullPath:
							pages = pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
							descr = 'foo'
							f = open(fullPath,'rb')
							content = bytearray(f.read())
							f.close()

		except Exception, e:
			pass

		#   Artifacts are responsible for returning these 3 values
		return { "descr":descr, "content":content, "pages":pages }
