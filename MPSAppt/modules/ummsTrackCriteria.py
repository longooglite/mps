# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.services.jobActionService as jaSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.lookupTableService as lookupSvc
import os

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		f = None
		try:
			apptId = self.workflow.jobActionDict.get('appointment_id',-1)
			jaService = jaSvc.JobActionService(self.params.get('dbConnection',None))
			appointment = jaService.getAppointment(apptId)
			title = lookupSvc.getEntityByKey(self.dbConnection,"wf_title",appointment.get('title_id',-1),"id")
			f = open(self.params.get('env').buildFullPathToSiteTemplatesList('umms')[0] + os.sep + "CriteriaDocuments" + os.sep + title.get('position_criteria',''),'rb')
			return {"descr":"criteria","content":bytearray(f.read()),"pages":3}
		except Exception,e:
			pass
		finally:
			if f:
				f.close()