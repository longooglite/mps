# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.evaluationsService as evaluationsService
import MPSAppt.services.fileRepoService as fileRepoService
import MPSAppt.services.lookupTableService as lookupTableService
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSAppt.modules.academicEvaluators as acadEvals


def getEvaluatorLetters(_dbConnection,_configDict,_workflow,_descr,_env):
	content = None
	try:
		taskCode = _configDict.get('task_code','')
		jobTaskDict = _workflow.getJobTaskCache().get(taskCode,'')
		if jobTaskDict:
			evalSourceDict = lookupTableService.getLookupTable(_dbConnection,"wf_evaluator_source")
			evaluatorTypeIds = []
			evaluatorTypeDict = {}
			for evalType in _configDict.get('evaluator_types',''):
				evaluatorType = lookupTableService.getEntityByKey(_dbConnection,"wf_evaluator_type",evalType)
				if evaluatorType:
					evaluatorTypeDict[evaluatorType.get('id',-1)] = evaluatorType
					evaluatorTypeIds.append(evaluatorType.get('id',-1))
			evaluators = evaluationsService.EvaluationsService(_dbConnection).getEvaluatorsList(jobTaskDict.get('id',-1),_orderBy="UPPER(lastname),UPPER(firstname)")
			documents = []
			fileRepoSvc = fileRepoService.FileRepoService(_dbConnection)
			for evaluator in evaluators:
				if evaluator.get('evaluator_type_id',-1) in evaluatorTypeIds:
					uploadFile = fileRepoSvc.getFileRepoContent(jobTaskDict,evaluator.get('uploaded_file_repo_seq_nbr',-1))
					if uploadFile and uploadFile.get('content',''):
						if _configDict.get('includeBio',False):
							bio = acadEvals.getBio(evaluator,evaluatorTypeDict,evalSourceDict,_env)
							documents.append(bio)
						documents.append(uploadFile)
			if documents:
				mergedContent,pages = pdfUtils.mergePDFsToOne(documents)
				return {"descr":_descr,"content":mergedContent,"pages":pages}
		return {"descr":_descr,"content":None,"pages":0}
	except Exception,e:
		pass

