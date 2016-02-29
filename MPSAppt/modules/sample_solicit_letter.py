# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.services.evaluationsService as evaluationsSvc
import MPSCore.utilities.PDFUtils as pdfUtils

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		content = None
		pages = 0
		try:
			config = eval(self.config)
			task_code = config.get('task_code','')
			jobTask = self.workflow.jobTaskCache.get(task_code,{})
			if jobTask:
				someEvaluator = self._findFirstEvaluator(jobTask.get('id',-1))
				if someEvaluator:
					evaluatorid = someEvaluator.get('id',-1)
					container = self.workflow.getContainer(task_code)
					if container:
						context = {}
						context['taskcode'] = task_code
						context['jobactionid'] = self.workflow.jobActionDict.get('id',-1)
						context['evaluatorid'] = someEvaluator.get('id',-1)
						context.update(container.getEditContextSend(int(evaluatorid), {}, _isPDF=True))
						loader = self.templateLoader
						templatePath = self.buildFullPathToSiteTemplate(config.get("site",""),config.get("email_template",""))
						template = loader.load(templatePath)
						html = template.generate(context=context, skin={})
						pdf, fullPath = pdfUtils.createPDFFromHTML(html, self.env, setFooter=False, prefix = 'sampleSolicitationLetter_')
						if fullPath:
							f = open(fullPath,'rb')
							content = bytearray(f.read())
							f.close()
							pages = pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
		except Exception,e:
			pass
		#artifacts responsible for returning these 3 values
		return {"descr":"Sample Solicitation Letter","content":content,"pages":pages}

	def _findFirstEvaluator(self,jobTaskId):
		resultList = evaluationsSvc.EvaluationsService(self.dbConnection).getEvaluatorsList(jobTaskId)
		for evaluatorDict in resultList:
			if not evaluatorDict.get('declined', False):
				return evaluatorDict
		return None

