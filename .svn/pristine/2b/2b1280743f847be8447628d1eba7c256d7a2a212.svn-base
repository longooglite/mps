# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.constants as constants
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.stringUtilities as stringUtils

#   Super-class for task-related service classes.

class AbstractTaskService:
	def __init__(self, _connection):
		self.connection = _connection


	#   Timestamp a Job Task.

	def touchJobTask(self, _jobTaskDict, _updated, _username, doCommit=True):
		import MPSAppt.services.jobActionService as jobActionSvc
		jobActionSvc.JobActionService(self.connection).touchJobTaskImpl(_jobTaskDict, _updated, _username, doCommit)


	#   Email settings.

	def getEmailOn(self, _profile):

		#   Returns a boolean indicating whether or not sending of emails is 'on'.
		#
		#   This parameter can be specified at one of two levels: Site, or Environment.
		#   Site is used as an override to explicitly turn email on/off for specific Sites.
		#   Emailing based on Environment is the default. Think of 'Environment' as a server-wide setting.
		#
		#   Normally, the Environment specifies the Email settings. That is to say, all sites running on a
		#   particular server usually adhere to the policy set forth for the Environment. However, for a Site
		#   that requires different behavior, Site-level override can be provided.
		#
		#   Look first for a Site-level setting. If the setting exists in the given _profile, we use it.
		#   Thus, the Site-level setting can be used to explicitly turn emailing on or off for a specific Site.
		#
		#   If no Site-level setting is specified, simply return the Environment setting.

		if _profile:
			sitePreferences = _profile.get('siteProfile', {}).get('sitePreferences', {})
			if 'emailon' in sitePreferences:
				return stringUtils.interpretAsTrueFalse(sitePreferences['emailon'])

		return envUtils.getEnvironment().getEmailOn()


	#   Common event handler pre-commit activities.

	def commmonHandlerPrecommitTasks(self,
			_jobActionDict,
			_jobTaskDict,
			_container,
			_profile,
			_formData,
			_now,
			_username,
			_activityLogConfigKeyName='activityLog',
			_dashboardConfigKeyName='dashboardEvents',
			_freezeConfigKeyName='freeze',
			_alertConfigKeyName='alert',
			_emailConfigKeyName='emails',
			doCommit=True):
		_container.clearJobTaskCache()
		_container.setIsLoaded(False)
		_container.loadInstance()

		#   Timestamp the Job Task.
		self.touchJobTask(_jobTaskDict, _now, _username, doCommit)

		#   Freeze/Thaw.
		if _freezeConfigKeyName:
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username
			self.freezeThaw(_jobActionDict, _container, _freezeConfigKeyName, logDict)

		#   Black/White Listing
		self.blackListWhiteList(_container,_jobActionDict)

		#   Activity Log.
		import MPSAppt.services.activityService as activitySvc
		fullUserName = _profile.get('userProfile',{}).get('userPreferences',{}).get('description',_username)
		activitySvc.ActivityService(self.connection).writeActivityLog(_jobTaskDict, _container, _formData, _activityLogConfigKeyName, _now, fullUserName, doCommit)

		#   Dashboard Events.
		import MPSAppt.services.dashboardService as dashboardSvc
		dashboardSvc.DashboardService(self.connection).processDashboardEvents(_jobActionDict, _jobTaskDict, _container, _dashboardConfigKeyName, _now, _username, doCommit)

		#   Field Level Revisions
		self.clearFieldLevelRevisions(_container,_jobActionDict,_now,_username,doCommit)

		#   Emails.
		if self.getEmailOn(_profile):
			import MPSAppt.services.emailService as emailSvc
			emailer = emailSvc.EmailService(self.connection, _jobActionDict, _jobTaskDict, _container, _profile, _username, _now, _alertConfigKeyName=_alertConfigKeyName, _emailConfigKeyName=_emailConfigKeyName)

			#   Alert emails.
			emailer.prepareAndSendAlertEmail(doCommit)

			#   Directive emails.
			emailer.prepareAndSendDirectiveEmails(doCommit)

		#   Custom handler pre-commit activities.
		_container.customPrecommitHook(_jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName, _dashboardConfigKeyName, _freezeConfigKeyName, _alertConfigKeyName, _emailConfigKeyName, doCommit)


	#   Field Level Revisions

	def clearFieldLevelRevisions(self,_container,_jobActionDict,_now,_username,doCommit):
		import MPSAppt.services.fieldLevelRevisionsService as FLRService
		config = _container.getConfigDict()
		if config.get('clearFieldLevelRevisions',False):
			flrService = FLRService.FieldLevelRevisions(self.connection)
			fieldRevisionsList = config.get('clearFieldLevelContainers',[])
			for revision in fieldRevisionsList:
				flrService.setRevisionsComplete(_jobActionDict.get('id',-1),revision,_now,_username,doCommit)

	#   Freeze/Thaw.

	def freezeThaw(self, _jobActionDict, _container, _freezeConfigKey, _logDict):
		if not _freezeConfigKey:
			return
		freezeThawConfigDict = _container.getConfigDict().get(_freezeConfigKey, {})
		if not freezeThawConfigDict:
			return

		import MPSAppt.services.jobActionService as jobActionSvc
		jaSvc = jobActionSvc.JobActionService(self.connection)
		jobActionId = _jobActionDict.get('id', None)

		#   Set Job Action Revisions Required.

		if freezeThawConfigDict.get('setJobActionRevisionsRequired', False):
			_logDict['verb'] = constants.kJobActionLogVerbSetJobActionRevisionsRequired
			_logDict['item'] = ''
			_logDict['message'] = _container.getLogMessage(_logDict['verb'], _logDict['item'])
			jaSvc.setJobActionRevisionsRequired(jobActionId, _logDict, doCommit=False)

		#   Clear Job Action Revisions Required.

		if freezeThawConfigDict.get('clearJobActionRevisionsRequired', False):
			_logDict['verb'] = constants.kJobActionLogVerbClearJobActionRevisionsRequired
			_logDict['item'] = ''
			_logDict['message'] = _container.getLogMessage(_logDict['verb'], _logDict['item'])
			jaSvc.clearJobActionRevisionsRequired(jobActionId, _logDict, doCommit=False)

		#   Freeze Job Action.

		if freezeThawConfigDict.get('freezeJobAction', False):
			_logDict['verb'] = constants.kJobActionLogVerbFreezeJobAction
			_logDict['item'] = ''
			_logDict['message'] = _container.getLogMessage(_logDict['verb'], _logDict['item'])
			jaSvc.freezeJobAction(jobActionId, _logDict, doCommit=False)

		#   Unfreeze Job Action.

		if freezeThawConfigDict.get('unfreezeJobAction', False):
			_logDict['verb'] = constants.kJobActionLogVerbUnfreezeJobAction
			_logDict['item'] = ''
			_logDict['message'] = _container.getLogMessage(_logDict['verb'], _logDict['item'])
			jaSvc.unfreezeJobAction(jobActionId, _logDict, doCommit=False)

		#   Freeze Tasks.

		containerList = []
		if freezeThawConfigDict.get('freezeAllPredecessors', False):
			containerList = _container.getWorkflow().getFreezablePredecessorTasks(_container.getCode())
		if _container.getIsFreezable() and freezeThawConfigDict.get('freezeSelf', False):
			containerList.append(_container)
		for taskCode in freezeThawConfigDict.get('freezeTasks', []):
			thisContainer = _container.getWorkflow().getContainer(taskCode)
			if thisContainer and \
				thisContainer.getIsFreezable() and \
				thisContainer not in containerList:
				containerList.append(thisContainer)

		_logDict['verb'] = constants.kJobActionLogVerbFreeze
		for container in containerList:
			_logDict['item'] = container.getCode()
			_logDict['message'] = _container.getLogMessage(_logDict['verb'], _logDict['item'])
			jaSvc.getOrCreatePrimaryJobTask(_jobActionDict, container, _logDict.get('created',''), _logDict.get('lastuser',''), doCommit=False)
			jaSvc.freezeJobTask(_logDict['job_action_id'], container.getCode(), _logDict, doCommit=False)

		#   Unfreeze Tasks.

		containerList = []
		if freezeThawConfigDict.get('unfreezeAllPredecessors', False):
			containerList = _container.getWorkflow().getFreezablePredecessorTasks(_container.getCode())
		if _container.getIsFreezable() and freezeThawConfigDict.get('unfreezeSelf', False):
			containerList.append(_container)
		for taskCode in freezeThawConfigDict.get('unfreezeTasks', []):
			thisContainer = _container.getWorkflow().getContainer(taskCode)
			if thisContainer and \
				thisContainer.getIsFreezable() and \
				thisContainer not in containerList:
				containerList.append(thisContainer)

		_logDict['verb'] = constants.kJobActionLogVerbUnfreeze
		for container in containerList:
			_logDict['item'] = container.getCode()
			_logDict['message'] = _container.getLogMessage(_logDict['verb'], _logDict['item'])
			revisionsRequiredApprovalTask = ''
			if freezeThawConfigDict.get('setJobActionRevisionsRequired', False):
				if container.getCode() in freezeThawConfigDict.get('unfreezeOptions',[]):
					revisionsRequiredApprovalTask = _container.getCode()
			jaSvc.getOrCreatePrimaryJobTask(_jobActionDict, container, _logDict.get('created',''), _logDict.get('lastuser',''), doCommit=False)
			jaSvc.unfreezeJobTask(_logDict['job_action_id'], container.getCode(),revisionsRequiredApprovalTask, _logDict, doCommit=False)

		#   Clear Submit status.

		submitContainerCode = freezeThawConfigDict.get('clearSubmitStatus','')
		if submitContainerCode:
			if not type(submitContainerCode) is list:
				submitContainerCode = [submitContainerCode]
			for code in submitContainerCode:
				submitContainer = _container.getWorkflow().getContainer(code)
				if submitContainer:
					submitJobTask = jaSvc.getJobTask(_jobActionDict, submitContainer)
					if submitJobTask:
						className = submitContainer.getContainerDict().get('className','')
						if className == constants.kContainerClassAttest:
							import MPSAppt.services.attestService as attestSvc
							attestDict = {}
							attestDict['updated'] = _logDict.get('created', '')
							attestDict['lastuser'] = _logDict.get('lastuser', '')
							attestDict['job_task_id'] = submitJobTask.get('id',None)
							attestDict['complete'] = False
							attestSvc.AttestService(self.connection).updateAttestation(submitJobTask,attestDict,doCommit=False)
						else:
							myApprovalDict = {}
							myApprovalDict['job_task_id'] = submitJobTask.get('id',None)
							myApprovalDict['approval'] = ''
							myApprovalDict['updated'] = _logDict.get('created', '')
							myApprovalDict['lastuser'] = _logDict.get('lastuser', '')

							import MPSAppt.services.approvalService as approvalSvc
							approvalSvc.ApprovalService(self.connection).updateApprovalStatus(submitJobTask, myApprovalDict, doCommit=False)

	#   Black List/White List

	def blackListWhiteList(self,_container,_jobActionDict):
		import MPSAppt.services.departmentService as deptSvc
		import MPSAppt.services.jobActionService as jobActionSvc
		configDict = _container.getConfigDict()
		whitelist = configDict.get('whitelist',None)
		blacklist = configDict.get('blacklist',None)
		if blacklist or whitelist:
			_container.loadInstance()
			#confusing - When doing a standalone secondary appointment, the primary appointment is an appointment off in some other department. The primary department on the workflow'
			#is the secondary department.
			if _container.getConfigDict().get('departmentIdentifier') == 'personsprimary':
				secondaryDepartment = _container.getDepartment()
				primaryDepartment = _container.getDepartment('primary')
			else:
				#In the case of a joint secondary, since the workflow is being driven by the primary department, the primary department is on the workflow and the secondaries
				#are gotten by talking to configured confirmtitledept objects
				primaryDepartment = deptSvc.DepartmentService(self.connection).getDepartmentForJobAction(_jobActionDict)
				secondaryDepartment = _container.getDepartment()
			blacklistDepartment,whitelistDepartment = None,None
			blacklistDepartmentType,whiteListDepartmentType = blacklist.get('departmentType',''),whitelist.get('departmentType','')
			if blacklistDepartmentType  == 'primary':
				blacklistDepartment = primaryDepartment
			elif blacklistDepartmentType == 'secondary':
				blacklistDepartment = secondaryDepartment
			if whiteListDepartmentType  == 'primary':
				whitelistDepartment = primaryDepartment
			elif whiteListDepartmentType == 'secondary':
				whitelistDepartment = secondaryDepartment
			if blacklistDepartment:
				if secondaryDepartment.get('id',-1) == primaryDepartment.get('id',-1):
					return  #administrative appointments take place in the same departments. Don't black/whitelist
				taskCodes = blacklist.get('containers',[])
				for taskCode in taskCodes:
					jobActionSvc.JobActionService(self.connection).overrideJobActionDepartmentalAccess(_jobActionDict.get('id',-1),taskCode,blacklistDepartment.get('id',-1),False,doCommit=False)
			if whitelistDepartment:
				if secondaryDepartment.get('id',-1) == primaryDepartment.get('id',-1):
					return  #administrative appointments take place in the same departments. Don't black/whitelist
				taskCodes = whitelist.get('containers',[])
				for taskCode in taskCodes:
					jobActionSvc.JobActionService(self.connection).overrideJobActionDepartmentalAccess(_jobActionDict.get('id',-1),taskCode,whitelistDepartment.get('id',-1),True,doCommit=False)
