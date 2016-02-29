# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.services.lookupTableService as lookupTableService
import MPSAppt.services.evaluationsService as evaluationsService
import MPSAppt.modules.academicEvaluators as acadEvals

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		content = None
		try:
			configDict = eval(self.config)
			taskCode = configDict.get('task_code','')
			jobTaskDict = self.workflow.getJobTaskCache().get(taskCode,'')
			if jobTaskDict:
				evalSourceDict = lookupTableService.getLookupTable(self.dbConnection,"wf_evaluator_source")
				evaluatorTypeIds = []
				evaluatorTypeDict = {}
				evaluatorsReceived = []
				evaluatorsDeclined = []

				for evalType in configDict.get('evaluator_types',''):
					evaluatorType = lookupTableService.getEntityByKey(self.dbConnection,"wf_evaluator_type",evalType)
					if evaluatorType:
						evaluatorTypeDict[evaluatorType.get('id',-1)] = evaluatorType
						evaluatorTypeIds.append(evaluatorType.get('id',-1))
				evaluators = evaluationsService.EvaluationsService(self.dbConnection).getEvaluatorsList(jobTaskDict.get('id',-1),_orderBy="UPPER(lastname),UPPER(firstname)")
				for evaluator in evaluators:
					if evaluator.get('declined',False):
						evaluatorsDeclined.append(evaluator)
					else:
						if evaluator.get('uploaded',False):
							evaluatorsReceived.append(evaluator)

				content,pages = acadEvals.getExternalReviewersList(evaluatorsReceived,evaluatorsDeclined,evaluatorTypeDict,evalSourceDict,self.env)

				return {"descr":"External Reviewers List","content":content,"pages":pages}
		except Exception,e:
			pass
