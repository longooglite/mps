# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.handlers.coreApplicationHandler as coreAppHandler
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.reportingService as reportingSvc
import MPSAppt.utilities.environmentUtils as envUtils
from MPSAppt.core.apptMenues import MENUES
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.handlers.adminUserHelper as userHelper
from PIL import Image
import json
import os

kKeyName = 'MPSAppt_SessionParms'

class AbstractHandler(coreAppHandler.CoreApplicationHandler):

	def getEnvironment(self):
		return envUtils.getEnvironment()

	def getMenues(self):
		menuList = self.buildMenuList(MENUES)
		try:
			jobActionId = getattr(self,"jobActionId",None)
			if stringUtils.interpretAsTrueFalse(self.getSitePreferences().get('reporting','')):
				if not self.hasPermission('apptCandidate'):
					self.extendMenuWithReporting(menuList)
			if jobActionId:
				if stringUtils.interpretAsTrueFalse(self.getSitePreferences().get('autofill','')):
					if getattr(self,"jobActionId",None):
						self.extendMenuWithAutofill(menuList)

				isInCandidateView = stringUtils.interpretAsTrueFalse(self.getProfile().get('sessionProfile',{}).get('isCandidateView','false'))
				if self.hasPermission("apptViewAsCandidate") or isInCandidateView:
					if getattr(self,"jobActionId",None):
						if self.dbConnection:
							jaSVC = jobActionSvc.JobActionService(self.dbConnection)
							jobAction = jaSVC.getJobAction(jobActionId)
							if jobAction:
								candidate = jaSVC.getCandidateDict(jobAction)
								if candidate and candidate.get('username'):
									self.extendMenuWithViewAsCandidate(menuList, isInCandidateView)
		except Exception,e:
			#if anything blows up building autofill or candidate view, eat the error and proceed
			pass
		return menuList

	def extendMenuWithViewAsCandidate(self, _menuList, _isInCandidateView):
		baseurl = "/appt/viewascandidate/" + str(getattr(self,"jobActionId",0)) + '/'
		if _isInCandidateView:
			descr = 'Exit View as Candidate'
			urlSuffix = 'off'
		else:
			descr = 'View as Candidate'
			urlSuffix = 'on'

		menuDict = {}
		menuDict['rootid'] = 'viewascandidate'
		menuDict['enabled'] = True
		menuDict['descr'] = descr
		menuDict['glyph'] = 'glyphicon-eye-open'
		menuDict['url'] = baseurl + urlSuffix
		_menuList.append(menuDict)

	def extendMenuWithAutofill(self,menuList):
		menuDict = {"descr":"Autofill","enabled":"true","rootid":"autofill","glyph":"glyphicon-import"}
		configFile = None
		try:
			coreEnvUtilities = coreEnvUtils.CoreEnvironment()
			corePath = coreEnvUtilities.getSrcCoreFolderPath()
			configPath = corePath.split('MPSCore')[0] + "%s%s%s%s%s%s" % ('config',os.sep,'dev',os.sep,'MPSAppt',os.sep)
			configFilePath = configPath + 'autofill.json'
			if os.path.exists(configFilePath):
				configFile = open(configFilePath,'rU')
				configList = json.loads(configFile.read())
				menuDict['itemList'] = []
				for item in configList:
					item = {"descr":item.get('descr',''),"enabled":"true","url":"/appt/autofill/" + str(getattr(self,"jobActionId",0)) + '/' + str(item.get('source_jaId','')) + '/' + str(item.get('taskcodes',[]))}
					menuDict['itemList'].append(item)
				menuList.append(menuDict)
		except Exception,e:
			pass
		finally:
			if configFile:
				configFile.close()

	def extendMenuWithReporting(self,menuList):
		community = self.getUserProfileCommunity()
		username = self.getUserProfileUsername()
		unreadReports = reportingSvc.ReportingService(self.dbConnection).getNbrUnreadReportsForUser(community, username)
		menuDict = {"descr":"Reporting","enabled":"true","rootid":"reporting","glyph":"glyphicon-print","itemListHasGlyphs": True,"nbrUnread":unreadReports}
		configFile = None
		try:
			coreEnvUtilities = coreEnvUtils.CoreEnvironment()
			corePath = coreEnvUtilities.getSrcCoreFolderPath()
			configPath = corePath.split('MPSCore')[0] + "%s%s%s%s%s%s%s%s%s%s" % ('data',os.sep,'atramData',os.sep,'sites',os.sep,self.getProfile().get('siteProfile',{}).get('site',''),os.sep,"reports",os.sep)
			configFilePath = configPath + 'reportingmenuconfig.json'
			if os.path.exists(configFilePath):
				configFile = open(configFilePath,'rU')
				configList = json.loads(configFile.read())
				menuDict['itemList'] = []
				archiveItem = {"descr":"<b>View Reports Archive</b>","enabled":"true","url":"/appt/reporting/viewarchive","glyph": "glyphicon-print"}
				menuDict['itemList'].append(archiveItem)
				for entry in configList:
					hasPermission = False
					for perm in entry.get('permission',[]):
						if self.hasPermission(perm):
							hasPermission = True
					if hasPermission:
						item = {"descr":entry.get('descr',''),"enabled":"true","url":"/appt/reporting/" + entry.get('reportConfig','')}
						menuDict['itemList'].append(item)
				if menuDict['itemList']	:
					menuList.append(menuDict)
		except Exception,e:
			pass
		finally:
			if configFile:
				configFile.close()


	def getAppMenues(self):
		return [self.buildApplicationMenu(self.getUserProfile().get('userApplications',[]))]

	def getPostResponseDict(self, _message=None):
		responseDict = {}
		if _message:
			try:
				msgDict = self.postToAuthSvc("/putMessage", { 'message': _message })
				responseDict['msgid'] = msgDict.get('msgid', '')
			except Exception as e:
					pass
		return responseDict

	def getInitialTemplateContext(self, _environment=None):
		context = super(AbstractHandler, self).getInitialTemplateContext(_environment)
		context['windowTitle'] = 'Appointments'
		context['pageHeaderTitle'] = 'Appointments'
		return context

	def handleGetException(self, _exception, _logger, _optionalOverrideRedirect=None):
		super(AbstractHandler, self).handleGetException(_exception, _logger, _optionalOverrideRedirect)
		if not _optionalOverrideRedirect:
			self.redirect(envUtils.getEnvironment().getToastUri())


	def _getSessionParms(self):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		response = self.postToAuthSvc("/getRandomSessionData", payload, "Unable to obtain %s" % kKeyName)
		cvSessionDict = response.get('value', None)
		if cvSessionDict:
			return cvSessionDict
		return self._getInitialSessionParms()

	def _getInitialSessionParms(self):
		cvSessionDict = {}
		cvSessionDict['a'] = False
		cvSessionDict['b'] = False
		cvSessionDict['c'] = False
		return cvSessionDict

	def _putSessionParms(self, _cvSessionDict):
		payload = self.getInitialPayload()
		payload['key'] = kKeyName
		payload['value'] = _cvSessionDict
		response = self.postToAuthSvc("/putRandomSessionData", payload, "Unable to save %s" % kKeyName)

	def setSessionParms(self,key):
		sessionParms = self._getSessionParms()
		sessionParms[key] = not sessionParms[key]
		self._putSessionParms(sessionParms)


	#   Various routines to redirect when errors occur.

	def doRedirect(self, _message, _url="/appt"):
		try:
			msgDict = self.postToAuthSvc("/putMessage", { 'message': _message})
			msgid = msgDict.get('msgid', '')
			if msgid:
				self.set_cookie('msgid', msgid)
		except Exception as e:
			pass

		self.redirect(_url)


	#   Various common validation routines used by many handlers.

	def validateJobAction(self, _jobActionService, _jobActionId):
		jobActionDict = _jobActionService.getJobAction(_jobActionId)
		if not jobActionDict:
			raise excUtils.MPSValidationException("Unable to retrieve job action")
		return jobActionDict

	def validateTaskCode(self, _workFlow, _taskCode, _optionalClassName=None):
		container = _workFlow.getContainer(_taskCode)
		if not container:
			raise excUtils.MPSValidationException("Unable to retrieve container for code '%s'" % _taskCode)
		if _optionalClassName:
			if type(_optionalClassName) == type([]):
				if container.getClassName() not in _optionalClassName:
					raise excUtils.MPSValidationException("Container is not a allowed container")
			else:
				if container.getClassName() != _optionalClassName:
					raise excUtils.MPSValidationException("Container is not a '%s' container" % _optionalClassName)
		return container

	def validateUserHasAccessToJobAction(self, _dbConnection, _community, _username, _jobActionDict):
		#   Skip this check for Candidates.
		if self.hasPermission('apptCandidate'):
			theCandidate = personSvc.PersonService(_dbConnection).getPerson(_jobActionDict.get('person_id',-1))
			if theCandidate is None or \
				theCandidate.get('community','').strip() <> _community.strip() or \
				theCandidate.get('username','').strip() <> _username.strip():
				raise excUtils.MPSValidationException("Permission Denied")
		else:
			positionId = _jobActionDict.get('position_id', 0)
			positionDict = positionSvc.getPostionById(_dbConnection, positionId)
			if not positionDict:
				raise excUtils.MPSValidationException("Unable to retrieve position for id '%i'" % positionId)

			departmentId = positionDict.get('department_id', 0)
			departmentList = deptSvc.DepartmentService(self.dbConnection).getDepartmentsForUser(_community, _username)
			for departmentDict in departmentList:
				if departmentDict.get('id',0) == departmentId:
					return False
			if jobActionSvc.JobActionService(self.dbConnection).departmentHasOverrideAccessToJobAction(_jobActionDict.get('id',-1),departmentList,False):
				return True
			raise excUtils.MPSValidationException("User not permitted to access Department")

	def validatePDFOrImageContent(self,fileObject,container):
		pages = 0
		version = ''
		message = ''
		fileType = container.getConfigDict().get('fileType','PDF')
		extension = '.pdf' if fileType == 'PDF' else '.img'
		f = None
		fp = None
		try:
			filePath = self.getEnvironment().createGeneratedOutputFilePath('file_', extension)
			f = open(filePath,'wb')
			f.write(bytearray(fileObject.body))
			f.flush()
			if fileType == 'PDF':
				version = pdfUtils.getPDFVersion(fileObject.body)
				pages = pdfUtils.getPageCountAndNormalizePDFContent(filePath)
				fp = open(filePath,'rb')
				content = bytearray(fp.read())
				fileObject.body = content
			elif fileType == 'image':
				version = 'image'
				pages = 1
				fp = open(filePath, "rb")
				im = Image.open(fp)
				im.load()
		except Exception, e:
			errorText = ''
			if fileType == 'PDF':
				errorText = 'PDFs'
			elif fileType == 'image':
				errorText = 'images'
			message = "Invalid file format: only %s are accepted" % (errorText)
			pass
		finally:
			if f:
				f.close()
			if fp:
				fp.close()
		return message,pages,version


	#   Common Job Action tasks.

	def updateRosterStatusForJobAction(self, _dbConnection, _jobActionDict):
		jobActionId = _jobActionDict.get('id', 0)
		workflow = self.loadWorkflowForJobAction(_dbConnection, jobActionId)
		status = workflow.computeStatus()

		now = self.getEnvironment().formatUTCDate()
		username = self.getUserProfileUsername()
		jaService = jobActionSvc.JobActionService(_dbConnection)
		jaService.updateJobActionRosterStatus(jobActionId, status, now, username)
		return workflow

	def loadWorkflowForJobAction(self, _dbConnection, _jobActionId):
		jobActionDict = jobActionSvc.JobActionService(_dbConnection).getJobAction(_jobActionId)
		return workflowSvc.WorkflowService(_dbConnection).getWorkflowForJobAction(jobActionDict, self.getProfile())

	def writeJobActionLog(self, _dbConnection, _jobActionDict, _jobTaskDict, _container, _verb, _item, _now=None, _username=None):
		if not _container.getIsLogEnabled():
			return

		now = _now
		if not now:
			now = self.getEnvironment().formatUTCDate()

		username = _username
		if not username:
			username = self.getUserProfileUsername()

		logDict = {}
		logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
		logDict['job_task_id'] = _jobTaskDict.get('id', None)
		logDict['class_name'] = _container.getClassName()
		logDict['verb'] = _verb
		logDict['item'] = _item
		logDict['message'] = _container.getLogMessage(_verb, _item)
		logDict['created'] = now
		logDict['lastuser'] = username

		jobActionService = jobActionSvc.JobActionService(_dbConnection)
		jobActionService.createJobActionLog(logDict)

	def grantCandidateAccess(self, _personDict):
		helper = userHelper.AdminUserHelper(self)
		helper.handleGrantCandidateAccessRequest(_personDict)


	#   Date conversions.

	def convertMDYToDisplayFormat(self, _dateInDbFormat):

		#   Convert a YYYY-MM-DD from the database to the Site's display format.

		if not _dateInDbFormat: return ''
		return dateUtils.parseDate(_dateInDbFormat, self.getSiteYearMonthDayFormat())

	def convertTimestampToDisplayFormat(self, _timestampInDbFormat):

		#   Convert a full timestamp from the database to the Site's display format.

		if not _timestampInDbFormat: return ''
		return dateUtils.parseDate(_timestampInDbFormat, self.getSiteYearMonthDayHourMinuteFormat())

	#   url

	def getJobActionUrl(self,jobActionDict):
		return "%s/jobaction/%s" % (self.getBaseUrl(), str(jobActionDict.get('id',"")))

	def getBaseUrl(self, appCode='APPT'):
		siteAppList = self.profile.get('siteProfile',{}).get('siteApplications',{})
		for app in siteAppList:
			if app.get('code','') == appCode:
				return app.get('url','')
		return ''


	#   Path utilities.

	def buildFullPathToSiteTemplate(self, _templateName, _site=None):
		lastPath = ''
		site = _site if _site else self.getProfile().get('siteProfile',{}).get('site','')
		site = site.replace('-','_')
		pathList = envUtils.getEnvironment().buildFullPathToSiteTemplatesList(site)
		for path in pathList:
			lastPath = os.path.join(path, _templateName)
			if os.path.exists(lastPath):
				return lastPath
		return lastPath
