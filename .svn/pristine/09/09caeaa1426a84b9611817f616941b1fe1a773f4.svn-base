# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.fieldLevelRevisionsService as revisionsService

class FLRR_Activator(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)

	def prepareNotificationForSubmit(self,jobAction):
		unfreezeContainers = self.getConfigDict().get('freeze',{}).get('unfreezeTasks',[])
		if unfreezeContainers:
			revisions = revisionsService.FieldLevelRevisions(self.getWorkflow().getConnection()).getFieldLevelRevisionsForJobAction(jobAction)
			for revision in revisions:
				if revision.get('task_code','') not in unfreezeContainers:
					unfreezeContainers.append(revision.get('task_code',''))
			self.getConfigDict().get('freeze',{})['unfreezeTasks'] = unfreezeContainers
