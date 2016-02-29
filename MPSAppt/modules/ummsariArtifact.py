# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.PDFUtils as pdfUtils

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		f = None
		try:
			containerDict = self.workflow.workflowCache.get('ari',{})
			packethandler = self.context.get('handler',None)

			if containerDict and packethandler:
				candidate_name = self.context.get('candidate_name','').upper()
				jobActionDict = self.workflow.jobActionDict
				site = self.context.get('profile',{}).get('siteProfile',{}).get('site','')
				templateName = containerDict.get('config',{}).get('form','')
				form = self.buildFullPathToSiteTemplate(site, templateName)
				context = packethandler.getInitialTemplateContext(envUtils.getEnvironment())
				context['jobactionid'] = jobActionDict.get('job_action_id',-1)
				context['taskcode'] = 'ari'
				context['submitText'] = containerDict.get('config',{}).get('submitText','') % (candidate_name.upper())
				context['form'] = form
				context['prompts'] = containerDict.get('config',{}).get('prompts',[])
				loader = packethandler.getEnvironment().getTemplateLoader()
				template = loader.load(form)
				variableContent = template.generate(context=context)
				header = '<html><form><b>Authorization, Release and Immunity (ARI)</b>'
				submitText = containerDict.get('config',{}).get('submitText','') % (candidate_name)
				footer = '''<input type="checkbox" name="attest" checked="checked" value="True"> <b>%s</b></form></html>''' % (submitText)
				html = ''.join([header, variableContent, footer])
				pdffilename,pdffullPath = pdfUtils.createPDFFromHTML(html, self.env,"",False,'ari_')
				f = open(pdffullPath,'rb')
				content = bytearray(f.read())
				f.close()
				return {"descr":"ARI","content":content,"pages":1}
		except Exception,e:
			pass

