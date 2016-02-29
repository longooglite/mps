# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os
import os.path

import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.stringUtilities as stringUtils
from MPSAppt.core.containers.baseContainer import BaseContainer
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.departmentService as departmentSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.emailService as emailSvc
import MPSAppt.utilities.environmentUtils as envUtils

class Task(BaseContainer):

	#   Tasks are leaf-nodes in the Container hierarchy.

	def __init__(self, containerCode, parameterBlock):
		BaseContainer.__init__(self, containerCode, parameterBlock)

		accessPermissionName = self.getAccessPermissionName()
		accessPermissions = self.getAccessPermissions()
		if accessPermissionName not in accessPermissions:
			accessPermissions.append(accessPermissionName)

		viewPermissionName = self.getViewPermissionName()
		viewPermissions = self.getViewPermissions()
		if viewPermissionName not in viewPermissions:
			viewPermissions.append(viewPermissionName)
		if accessPermissionName not in viewPermissions:
			viewPermissions.append(accessPermissionName)


	#   Permissions.

	def getViewPermissionName(self):
		return self.getCode() + "_view"

	def getAccessPermissionName(self):
		return self.getCode() + "_edit"

	def hasViewPermission(self):
		if self.hasPermission('isalmighty'):
			return True
		return self.hasAnyPermission(self.getViewPermissions())

	def hasEditPermission(self):
		if self.hasPermission('isalmighty'):
			return True
		return self.hasAnyPermission(self.getAccessPermissions())

	#   Field Level Revisions

	def isFieldLevelRevisable(self,revisions):
		if self.workflow.jobActionDict.get('complete',False):
			#   disallow anything to be done on a completed job action
			return False,False
		flrrContainerCode = self.workflow.getMainContainer().getConfigDict().get('FLRR_Container','')
		if flrrContainerCode:
			flrrContainer = self.workflow.getContainer(flrrContainerCode)
			if flrrContainer:
				approvalContainerCode = flrrContainer.getConfigDict().get('approvalTask','')
				if approvalContainerCode:
					approvalContainer = self.workflow.getContainer(approvalContainerCode)
					if approvalContainer:
						if not approvalContainer.isComplete():
							return False,True
		config = self.getConfigDict()
		if config.get('isFieldLevelRevisable',False):
			if self.hasPermission('canrequestfieldrevisions'):
				#   Allow user to to enter revisions required mode
				#   Allow user to see revisions that have already been entered
				return True,True
			else:
				#   The candidate cannot go into revisions required mode
				#   The candidate can see the revisions if they've been submitted
				for revision in revisions:
					if revision.get('when_notified',''):
						return False,True
		#   not applicable for revisions required mode or field level revisions
		return False,False

	#   Rendering.

	def getEditContext(self, _sitePreferences):
		return self.getCommonEditContext(_sitePreferences)

	def getCommonEditContext(self, _sitePreferences):
		context = {}
		context['disabled'] = self.standardTaskDisabledCheck()
		context['optional'] = self.getIsOptional()
		context['blocked'] = self.getIsBlocked()
		context['complete'] = self.isComplete()
		context['activity_log'] = self.getTaskActivityLog(_sitePreferences)
		context['field_level_revisions_url'] = '/appt/jobaction/fieldlevelrevisions/%i/%s' % (self.workflow.jobActionDict.get('id',-1), self.getCode())
		return context

	def dictifyPromptsList(self,promptsList):
		dictifiedPromptsDict = {}
		for prompt in promptsList:
			code = prompt.get('code','')
			newdict = dict(prompt)
			try:
				del newdict['code']
				del newdict['data_type']
			except:
				pass
			dictifiedPromptsDict[code] = newdict
		return dictifiedPromptsDict


	#   Enabled/Disabled.

	def standardTaskDisabledCheck(self):
		if self.hasPermission('isalmighty'):
			return False
		isBlackWhiteListable = True
		#faculty affairs users are immune from blacklist/whiteist
		if self.hasPermission("facultyAffairsUser") or self.hasPermission("apptCandidate"):
			isBlackWhiteListable = False
		#whitelist, blacklist caches are filtered by the department this user is in
		if isBlackWhiteListable:
			isBlackListed = self.getWorkflow().getPermissionOverrideBlackListCache().get(self.getCode(),{}).get('access_allowed',True) == False
			#for the case that a primary department has access to multiple departments, it's possible that they could be black listed AND white listed.
			#If they are whitelisted and blacklisted, fall back to normal departmental permissions
			isWhiteListed = self.getWorkflow().getPermissionOverrideWhiteListCache().get(self.getCode(),{}).get('access_allowed',False)
			if isBlackListed and not isWhiteListed:
				return True

		if (self.getIsBlocked()) or \
					(self.getWorkflow().getJobActionDict().get('complete', False)) or \
					(self.getWorkflow().getJobActionDict().get('frozen', False)) or \
					(self.getWorkflow().getJobTaskCache().get(self.getCode(),{}).get('frozen', False)) or \
					(stringUtils.interpretAsTrueFalse(self.getWorkflow().userProfile.get('sessionProfile',{}).get('isCandidateView','false'))):
			return True

		#find out if person is whitelisted.
		if isBlackWhiteListable:
			isWhiteListed = False
			if self.getWorkflow().getPermissionOverrideWhiteListCache():
				#if there is anything in the whitelist cache for this user, we know the user is whitelisted
				isWhiteListed = True

			if isWhiteListed:
				#if the person is whitelisted, everything is disabled except for the individual tasks they've been granted access to
				whiteListCacheItem = self.getWorkflow().getPermissionOverrideWhiteListCache().get(self.getCode(),{})
				if whiteListCacheItem:
					if whiteListCacheItem.get('access_allowed',False):
						return False
					else:
						return True

		return (not self.hasAnyPermission(self.getAccessPermissions()))


	#   Activity Log.

	def getTaskActivityLog(self, _sitePreferences, _optionalSingleTaskCodeOrListOfTaskCodes=None):
		taskCode = _optionalSingleTaskCodeOrListOfTaskCodes if _optionalSingleTaskCodeOrListOfTaskCodes else self.getCode()
		return self.getWorkflow().getJobActionActivityLog(_sitePreferences, taskCode)


	#   Date and Timstamp localization.

	def convertMDYToDisplayFormat(self, _sitePreferences, _dateInDbFormat):
		#   Convert a YYYY-MM-DD from the database to the Site's display format.
		if not _dateInDbFormat: return ''
		localizedDate = dateUtils.localizeUTCDate(_dateInDbFormat, _tzname=_sitePreferences.get('timezone', 'US/Eastern'))
		return dateUtils.parseDate(localizedDate, _sitePreferences.get('ymdformat', '%m/%d/%Y'))

	def convertTimestampToDisplayFormat(self, _sitePreferences, _dateInDbFormat):
		#   Convert a YYYY-MM-DD HH:MM:SS.nnnnnn from the database to the Site's display format.
		if not _dateInDbFormat: return ''
		localizedDate = dateUtils.localizeUTCDate(_dateInDbFormat, _tzname=_sitePreferences.get('timezone', 'US/Eastern'))
		return dateUtils.parseDate(localizedDate, _sitePreferences.get('ymdhmformat', '%m/%d/%Y %H:%M'))

	def localizeDate(self, _utcDate, timezone, format):
		localDate = dateUtils.localizeUTCDate(_utcDate, timezone)
		return dateUtils.parseDate(localDate, format)


	#   Status calculation.

	def computeStatus(self):
		if self.getIsEnabled():
			if self.isCompleteWithConsiderations():
				return self.getStatusMsg()
		return ''

	#   Directive emails.

	def shouldGrantCandidateAccess(self):
		return False


	#   Custom pre-commit hook.

	def customPrecommitHook(self, _jobActionDict, _jobTaskDict, _container, _profile, _formData, _now, _username, _activityLogConfigKeyName, _dashboardConfigKeyName, _freezeConfigKeyName, _alertConfigKeyName, _emailConfigKeyName, doCommit=True):
		#   Hook for custom Task code.
		pass

	def initializeOnNewJobAction(self, _jobAction, _personDict, _profile, _now, _username, doCommit=True):
		#   Hook for processing on the create of a new job action
		self.initializeItemSharingOnNewJobAction(_jobAction, _profile, _now, _username, doCommit=doCommit)
		return {}

	def initializeItemSharingOnNewJobAction(self, _jobAction, _profile, _now, _username, doCommit=True):

		#   Create Job Task row for Items instances that are 'initialized'.
		#   Setup Item Sharing as specified in the item configuration.

		connection = self.getWorkflow().getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobTask = jaService.getOrCreateJobTask(_jobAction, self, _now, _username, doCommit=False)
			if jobTask:
				#   If this item specifies a 'parentCode', then we are actually sharing our data with an existing
				#   parent Task, IFF we are a child.

				parentCode = self.getConfigDict().get('parentCode', '')
				if parentCode:
					jobActionId = _jobAction.get('id', 0)
					if jobActionId:
						parentJobActionId = jaService.getParentRelatedJobAction(jobActionId)
						if (parentJobActionId) and (jobActionId != parentJobActionId):
							parentJobActionDict = jaService.getJobAction(parentJobActionId)
							parentWorkflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(parentJobActionDict, _profile)
							parentContainer = parentWorkflow.getContainer(parentCode)
							if parentContainer:
								parentTaskDict = jaService.getJobTask(parentJobActionDict, parentContainer)
								if parentTaskDict:
									jobTask['primary_job_task_id'] = parentTaskDict.get('id', 0)
									jobTask['updated'] = _now
									jobTask['lastuser'] = _username
									jaService.updateJobTaskPrimaryJobTaskId(jobTask, doCommit=False)

			if doCommit:
				connection.performCommit()

		except Exception, e:
			try: connection.performRollback()
			except Exception, e1: pass
			raise e


	#   Various.

	def getJobTaskDict(self):
		#   Obtains the current Job Task record, if any, from the Job Task Cache.
		#   The Job Task Cache only contains Job Tasks directly linked to the current Job Action.
		#   This method does not resolve to a different Job Task if a primary_job_task_id is specified.
		#   Use the getPrimaryJobTaskDict() method (below) for that purpose.
		jobTaskCache = self.getWorkflow().getJobTaskCache()
		return jobTaskCache.get(self.getCode(), None)

	def getPrimaryJobTaskDict(self, _jobTaskDict=None):
		#   Obtains the primary Job Task record, if any, for the given _jobTaskDict.
		#   If a primary Job Task is not specified, then _jobTaskDict is returned.
		#   If _jobTaskDict is not provided, it is first obtained using the getJobTaskDict() method (above).
		jobTaskDict = _jobTaskDict if _jobTaskDict else self.getJobTaskDict()
		if not jobTaskDict:
			return None

		primaryJobTaskId = jobTaskDict.get('primary_job_task_id', 0)
		if not primaryJobTaskId:
			return jobTaskDict

		primaryJobTaskDict = lookupTableSvc.getEntityByKey(self.getWorkflow().getConnection(), 'wf_job_task', primaryJobTaskId, _key='id')
		if primaryJobTaskDict:
			return primaryJobTaskDict
		return jobTaskDict

	def getContent(self):
		#   Called during packet generation. For use by non-file upload tasks if needed.
		return None

	def getRevisionsRequiredDescriptors(self,fieldName):
		return {}

	#   Email

	def sendDirectiveEmail(self,emailConfig,personDict,jobAction,container,now,profile):
		username = self.getWorkflow().userProfile.get('userProfile',{}).get('username','')
		emailer = emailSvc.EmailService(self.getWorkflow().getConnection(),jobAction,{"code":""},container,profile,username,now)
		for config in emailConfig:
			fullPathToSite = self.buildFullPathToSiteTemplate(profile.get('siteProfile',{}).get('site',''),config.get('bodyTemplateName',''))
			if config.get('sendToCandidate',False):
				config['sendToAddresses'].append(personDict.get('email',''))
			emailer.prepareAndSendDirectiveEmailFromNonItem(config,fullPathToSite,personDict,True)


	#   Department

	def getDepartment(self,departmentOverride = None):
		if departmentOverride and departmentOverride == "primary":
			return self.getWorkflow().department
		departmentTaskCode = self.getConfigDict().get('departmentContainer','')
		if departmentTaskCode:
			departmentContainer = self.getWorkflow().getContainer(departmentTaskCode)
			if departmentContainer:
				departmentContainer.loadInstance()
				departmentId = departmentContainer.getDepartmentId()
				if departmentId:
					department = lookupTableSvc.getEntityByKey(self.getWorkflow().getConnection(),'wf_department',departmentId,'id')
					if department:
						return department
		departmentIdentifier = self.getConfigDict().get('departmentIdentifier','')
		if departmentIdentifier == 'personsprimary':
			return departmentSvc.DepartmentService(self.getWorkflow().getConnection()).getPrimaryDepartmentForPerson(self.getWorkflow().getJobActionDict().get('person_id',-1))
		return self.getWorkflow().department


	#   Personal Info

	def locateEnabledPersonalInfoContainer(self):
		personalInfoTaskCode = self.getConfigDict().get('personalInfoTaskCode', '')
		if personalInfoTaskCode:
			personalInfoContainer = self.getWorkflow().getContainer(personalInfoTaskCode)
			if personalInfoContainer:
				if personalInfoContainer.getIsEnabled():
					return personalInfoContainer
		return None


	# Deletion - currently only used for injected items

	def deleteYourself(self):
		pass

	#   Images - grab image from another container, write to disk, fill context
	#   Currently used to display image for identity verification. But could come in handy in other cases
	#   Did not try to define placement on form, or deal with multiple images
	def updateContextWithImage(self,displayImage,displayImageScalePixelWidth,imageTaskCode,isForPrint=False):
		context = {"displayImage":False}
		if not imageTaskCode or not displayImage:
			return context
		import MPSAppt.services.fileRepoService as fileRepoSvc
		import MPSCore.utilities.PDFUtils as pdfUtils
		context['displayImage'] = displayImage
		context['displayImageScalePixelWidth'] = displayImageScalePixelWidth
		context['displayImageTaskCode'] = imageTaskCode
		context['displayImage'] = displayImage
		imageTask = self.workflow.jobTaskCache.get(imageTaskCode,None)
		if imageTask:
			imageItem = fileRepoSvc.FileRepoService(self.workflow.getConnection()).getLastFileRepo(imageTask,1)
			if imageItem:
				extension = '.jpg'
				file_name = imageItem.get('file_name','')
				if file_name.find('.') > 0:
					parts = file_name.split('.')
					extension = parts[len(parts)-1]
				image = fileRepoSvc.FileRepoService(self.workflow.getConnection()).getFileRepoContent(imageTask,1)
				env = envUtils.Environment()
				writepath = env.createGeneratedOutputFilePath('pers_img', extension)
				f = None
				try:
					f = open(writepath,'wb')
					f.write(image.get('content'))
					f.flush()
					scaledImagePath = pdfUtils.scaleImage(displayImageScalePixelWidth,writepath)
					uxPath = env.getUxGeneratedOutputFilePath(scaledImagePath)
					if isForPrint:
						context['imagePath'] = scaledImagePath
					else:
						context['imagePath'] = uxPath
				except:
					context['displayImage'] = False
					pass
				finally:
					try:
						if f:
							f.close()
						return context
					except:
						return context
		return context


