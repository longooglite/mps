# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.containers.submit as submitTask
import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.backgroundCheckService as backgroundCheckSvc

class SubmitBackgroundCheck(submitTask.Submit):
	def __init__(self, containerCode, parameterBlock):
		submitTask.Submit.__init__(self, containerCode, parameterBlock)


	#   Custom pre-commit hook.

	def customPrecommitHook(self, _jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName, _dashboardConfigKeyName, _freezeConfigKeyName, _alertConfigKeyName, _emailConfigKeyName, doCommit=True):
		#   Hook to submit a Background Check Order to an outside vendor.

		#   Must specify the name of the Background Check item.
		#   Background Check item must exist.
		#   Background Check item must be the correct item type.

		cbcTaskName = _container.getConfigDict().get('cbcTaskName', '')
		if not cbcTaskName: return

		cbcTask = _container.getWorkflow().getContainer(cbcTaskName)
		if not cbcTask: return

		if cbcTask.getClassName() != constants.kContainerClassBackgroundCheck:
			return

		#   Find or create the Job Task for the Background Check item.
		#   Create the Background Check item for the Task, if it does not exist.

		jaService = jobActionSvc.JobActionService(self.getWorkflow().getConnection())
		jobTask = jaService.getOrCreateJobTask(_jobActionDict, cbcTask, _now, _username, doCommit=doCommit)

		bcService = backgroundCheckSvc.BackgroundCheckService(self.getWorkflow().getConnection())
		backgroundCheckDict = bcService.getBackgroundCheck(jobTask.get('id',0))
		if not backgroundCheckDict:
			bcDict = {}
			bcDict['job_task_id'] = jobTask.get('id',0)
			bcDict['status'] = constants.kBackgroundCheckStatusNotSubmitted
			bcDict['status_date'] = _now
			bcDict['created'] = _now
			bcDict['updated'] = _now
			bcDict['lastuser'] = _username
			bcService.createBackgroundCheck(bcDict, doCommit)
			backgroundCheckDict = bcService.getBackgroundCheck(jobTask.get('id',0))
		if not backgroundCheckDict:
			return

		#   Submit the request to the 3rd-party vendor.
		#   Once we have a spec on how to do this, there will be a bunch of code to write.
		#   In the meantime, simply mark the Background Check as if we successfully submitted it.

		backgroundCheckDict['submitted_date'] = _now
		backgroundCheckDict['external_key'] = str(backgroundCheckDict['id'])
		bcService.enactSubmittedStatus(backgroundCheckDict, doCommit)
