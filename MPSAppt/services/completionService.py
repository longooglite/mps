# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.completionSQL as completionSQL
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.dashboardService as dashboardSvc
import MPSAppt.services.secondaryJobActionService as secondaryJobActionSvc

class CompletionService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getCompletion(self, _jobTaskId):
		return completionSQL.getCompletion(self.connection, _jobTaskId)

	def createCompletion(self, _completionDict, doCommit=True):
		completionSQL.createCompletion(self.connection, _completionDict, doCommit)


	#   UI creation/modification handling.

	def updateCompletion(self, _jobTaskDict, _completionDict, doCommit=True):
		existingCompletion = self.getCompletion(_jobTaskDict.get('id',0))

		try:
			if existingCompletion:
				completionSQL.updateCompletion(self.connection, _completionDict, doCommit=False)
			else:
				self.createCompletion(_completionDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _completionDict, _container, _profile, _formData, _now, _username, doCommit=True):

		try:
			jobActionId = _jobActionDict.get('id', None)

			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = jobActionId
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Completion table row.
			self.updateCompletion(_jobTaskDict, _completionDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbScheduleCompletion
				logDict['item'] = _container.getDescr()
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username,_dashboardConfigKeyName="completeDashboardEvents", doCommit=False)

			#   Job Action Completion.
			scheduledDate = _completionDict.get('scheduled_date','')
			if (scheduledDate) and (scheduledDate <= _now):
				self.completeJobAction(jobActionId, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e


	#   Completing a Job Action.

	def completeJobAction(self, _jobActionId, _now, _username, doCommit=True):

		try:
			#   Find the specified Job Action.
			jaService = jobActionSvc.JobActionService(self.connection)
			jobActionDict = jaService.getJobAction(_jobActionId)
			if not jobActionDict:
				return

			jobActionType = jaService.getJobActionType(jobActionDict)
			if not jobActionType:
				return
			jobActionDict['jobActionType'] = jobActionType
			#   Load the associated Workflow.
			wfService = workflowSvc.WorkflowService(self.connection)
			workflow = wfService.getWorkflowForJobAction(jobActionDict, {})

			#   Find the Completion Task in the workflow and in the database.
			#   Normally, there is exactly one of these containers.

			completionContainers = workflow.getContainersForClassName(constants.kContainerClassCompletion)
			if not completionContainers:
				return
			completionContainer = completionContainers[len(completionContainers) - 1]
			completionContainer.loadInstance()
			completionDict = completionContainer.getCompletion()
			effectiveDate = completionDict.get('effective_date', '')

			#   Perform common Job Action Completion tasks,
			#   plus any actions specific to the type of Job Action being completed.
			#
			#   This will need to be updated as we figure out what needs to happen.
			#   Currently, we're just marking this Job Action as done and rolling over
			#   the Job Action's Appointment to be the current Appointment.
			#   All of this is subject to change.

			self._commonCompletionTasks(jobActionDict, workflow, completionContainer, _now, _username)

			secondaryJobActionContainers = completionContainer.containerDict.get('config',{}).get('secondaryActionContainers',{})
			if secondaryJobActionContainers:
				self.createSecondaryJobActions(secondaryJobActionContainers,jobActionDict, workflow, completionContainer, _now, effectiveDate, _username, doCommit = False)

			secondaryJointPromoItem = completionContainer.containerDict.get('config',{}).get('secondaryPromoItem',{})
			if secondaryJointPromoItem:
				self.createSecondaryPromotions(secondaryJointPromoItem,jobActionDict, workflow, completionContainer, _now, effectiveDate, _username, doCommit = False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def createSecondaryJobActions(self,secondaryJobActionContainers,_jobActionDict, _workflow, _completionContainer, _now, _effectiveDate, _username,doCommit = False):
		#joint secondary appointments
		for secondary in secondaryJobActionContainers:
			activeContainer = _workflow.getContainer(secondary.get('determineActiveContainer',''))
			if activeContainer:
				if activeContainer.containerDict.get('enabled',False):
					approvalContainer = _workflow.getContainer(secondary.get('approvalContainer',''))
					if approvalContainer:
						approvalContainer.loadInstance()
						secondaryJobActionSvc.SecondaryJobActionService(self.connection).createSecondaryJobActions(secondary,_jobActionDict, _workflow,_completionContainer, _now, _username,doCommit)

	def createSecondaryPromotions(self,secondaryJointPromoItem,_jobActionDict, _workflow, _completionContainer, _now, _effectiveDate, _username, doCommit = False):
		jointSecondaryPromotionContainer = _workflow.getContainer(secondaryJointPromoItem)
		if jointSecondaryPromotionContainer:
			jointSecondaryPromotionContainer.loadInstance()
			jointSecondaryPromotions = jointSecondaryPromotionContainer.getJointPromotions()
			for jsPromotion in jointSecondaryPromotions:
				newjobActionDict = secondaryJobActionSvc.SecondaryJobActionService(self.connection).createSecondaryJointPromotions(jsPromotion,_jobActionDict,_completionContainer, _now, _username,doCommit)
				self.updateHistoricalAppointment(newjobActionDict,_effectiveDate,_now,_username)
				self.updateCurrentAppointment(newjobActionDict,_effectiveDate,_now,_username)

	def _commonCompletionTasks(self, _jobActionDict, _workflow, _completionContainer, _now, _username):
		completionTaskDict = _completionContainer.getJobTaskDict()
		completionDict = _completionContainer.getCompletion()
		effectiveDate = completionDict.get('effective_date', '')

		#   Logging setup.

		logDict = {}
		logDict['logEnabled'] = False
		logDict['created'] = _now
		logDict['lastuser'] = _username
		if completionTaskDict:
			logDict['logEnabled'] = _completionContainer.getIsLogEnabled()
			logDict['job_action_id'] = _jobActionDict.get('id', None)
			logDict['job_task_id'] = completionTaskDict.get('id', None)
			logDict['class_name'] = _completionContainer.getClassName()


		#   Freeze and Complete the Job Action, and update timestamp.
		jaService = jobActionSvc.JobActionService(self.connection)
		logDict['verb'] = constants.kJobActionLogVerbFreezeJobAction
		logDict['item'] = _completionContainer.getDescr()
		logDict['message'] = _completionContainer.getLogMessage(logDict['verb'], logDict['item'])
		jaService.freezeJobAction(_jobActionDict.get('id',None), logDict, doCommit=False)

		logDict['verb'] = constants.kJobActionLogVerbCompleteJobAction
		logDict['item'] = _completionContainer.getDescr()
		logDict['message'] = _completionContainer.getLogMessage(logDict['verb'], logDict['item'])
		jaService.completeJobAction(_jobActionDict.get('id',None), _workflow.getWorkflowJsonForArchiving(), '', '','', logDict, doCommit=False)

		if _jobActionDict.get('jobActionType',{}).get('code','') not in (constants.kJobActionTypeCredential,constants.kJobActionTypeEnroll):
			self.updateHistoricalAppointment(_jobActionDict, effectiveDate, _now, _username)
		newAppointmentDict = self.updateCurrentAppointment(_jobActionDict, effectiveDate, _now, _username)

		#   Update the Position to have the Title of the Appointment.

		if newAppointmentDict:
			newTitleId = newAppointmentDict.get('title_id', None)
			if newTitleId:
				positionDict = {}
				positionDict['id'] = _jobActionDict.get('position_id',-1)
				positionDict['title_id'] = newTitleId
				positionDict['updated'] = _now
				positionDict['lastuser'] = _username
				positionSvc.updateTitle(self.connection, positionDict, doCommit=False)


		#   Mark the wf_completion row as Complete.

		completionDict['complete'] = True
		completionDict['updated'] = _now
		completionDict['lastuser'] = _username
		self.updateCompletion(completionTaskDict, completionDict, doCommit=False)


		#   Make a log entry for completion.

		if logDict.get('logEnabled', False):
			logDict['verb'] = constants.kJobActionLogVerbComplete
			logDict['message'] = _completionContainer.getLogMessage(logDict['verb'], logDict['item'])
			jaService.createJobActionLog(logDict, doCommit=False)

		if _completionContainer.completionDict.get('termination_type_id',None):
			if newAppointmentDict:
				theDate = effectiveDate if effectiveDate else _now
				dateObj = datetime.datetime.strptime(theDate, dateUtils.kUTCDateOnlyFormat)
				endDate = dateUtils.formatUTCDateOnly(dateObj)
				jaService.updateAppointmentStatus(newAppointmentDict.get('id'), constants.kAppointStatusHistorical, endDate, endDate, _now, _username, doCommit=False)


	def updateHistoricalAppointment(self,_jobActionDict,_effectiveDate,_now,_username):
		#   Find and update any existing Filled Appointment for this Position:
		#       - mark as Historical
		#       - set end_date, if not already set
		#       - timestamp, lastuser
		jaService = jobActionSvc.JobActionService(self.connection)
		positionId = _jobActionDict.get('position_id', None)
		existingAppointmentDict = jaService.getFilledAppointmentForPosition(positionId)
		if existingAppointmentDict:
			appointmentId = existingAppointmentDict.get('id',None)
			startDate = existingAppointmentDict.get('start_date','')
			endDate = existingAppointmentDict.get('end_date','')
			if not endDate:
				theDate = _effectiveDate if _effectiveDate else _now
				dateObj = datetime.datetime.strptime(theDate, dateUtils.kUTCDateOnlyFormat)
				dateObj = dateObj - datetime.timedelta(days=1)
				endDate = dateUtils.formatUTCDateOnly(dateObj)
			jaService.updateAppointmentStatus(appointmentId, constants.kAppointStatusHistorical, startDate, endDate, _now, _username, doCommit=False)
		return positionId

	def updateCurrentAppointment(self,_jobActionDict, _startDate, _now, _username):
		#   Update the Appointment for this Job Action:
		#       - mark as Filled
		#       - set start_date, if not already set
		#       - timestamp, lastuser
		status = constants.kAppointStatusFilled
		if _jobActionDict.get('jobActionType',{}).get('code','') in (constants.kJobActionTypeCredential,constants.kJobActionTypeEnroll):
			status = constants.kAppointStatusHistorical
		
		jaService = jobActionSvc.JobActionService(self.connection)
		appointmentId = _jobActionDict.get('appointment_id', None)
		newAppointmentDict = jaService.getAppointment(appointmentId)
		if newAppointmentDict:
			startDate = newAppointmentDict.get('start_date','')
			endDate = newAppointmentDict.get('end_date','')
			if not startDate:
				startDate = _startDate[0:10]
			jaService.updateAppointmentStatus(appointmentId, status, startDate, endDate, _now, _username, doCommit=False)
		return newAppointmentDict

	#   Cancel a Job Action.
	#   Returnd True if the Job Action was canceled.
	#   Returns False if anything goes wrong.

	def cancelJobAction(self, _jobActionId, _comment, _now, _username, doCommit=True):

		try:
			#   Find the specified Job Action.
			jaService = jobActionSvc.JobActionService(self.connection)
			jobActionDict = jaService.getJobAction(_jobActionId)
			if not jobActionDict:
				return False
			appointment = jaService.getAppointment(jobActionDict.get('appointment_id'))

			#   Load the associated Workflow.
			wfService = workflowSvc.WorkflowService(self.connection)
			workflow = wfService.getWorkflowForJobAction(jobActionDict, {})

			#   Find the Completion Task in the workflow and in the database.
			#   Normally, there is exactly one of these containers.

			jaService.removeRelatedJobActionsforJobAction(_jobActionId,doCommit)
			completionContainers = workflow.getContainersForClassName(constants.kContainerClassCompletion)
			if not completionContainers:
				return False
			completionContainer = completionContainers[len(completionContainers) - 1]


			#   Logging setup.

			jaService.getOrCreateJobTask(jobActionDict, completionContainer, _now, _username, doCommit=False)
			completionContainer.loadInstance()
			completionTaskDict = completionContainer.getJobTaskDict()

			logDict = {}
			logDict['logEnabled'] = False
			logDict['created'] = _now
			logDict['lastuser'] = _username
			if completionTaskDict:
				logDict['logEnabled'] = completionContainer.getIsLogEnabled()
				logDict['job_action_id'] = _jobActionId
				logDict['job_task_id'] = completionTaskDict.get('id', None)
				logDict['class_name'] = completionContainer.getClassName()

			#   Freeze and Complete the Job Action, and update timestamp.
			jaService = jobActionSvc.JobActionService(self.connection)
			logDict['verb'] = constants.kJobActionLogVerbFreezeJobAction
			logDict['item'] = completionContainer.getDescr()
			logDict['message'] = completionContainer.getLogMessage(logDict['verb'], logDict['item'])
			jaService.freezeJobAction(_jobActionId, logDict, doCommit=False)

			logDict['verb'] = constants.kJobActionLogVerbCompleteJobAction
			logDict['item'] = completionContainer.getDescr()
			logDict['message'] = completionContainer.getLogMessage(logDict['verb'], logDict['item'])
			jaService.completeJobAction(_jobActionId, workflow.getWorkflowJsonForArchiving(), _comment, _username, _now, logDict, doCommit=False)

			#   Fix the Appointment Status a abandoned.
			jaService.updateAppointmentStatus(jobActionDict.get('appointment_id',-1), constants.kAppointStatusAbandoned, appointment.get('start_date'), '', _now,  _username, doCommit=False)

			#   Remove Dashboard events.
			dashboardSvc.DashboardService(self.connection).removeEventsForJobActionId(_jobActionId, doCommit=False)

			if doCommit:
				self.connection.performCommit()

			return True

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
