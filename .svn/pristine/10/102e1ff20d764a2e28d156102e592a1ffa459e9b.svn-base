# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractHandler as absHandler
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.core.packetMaster as packetMeister
import MPSAppt.services.titleService as titleSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.uberResolverService as uberResolverSvc

class AbstractPacketHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


class PacketDownloadHandler(AbstractPacketHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskCode = kwargs.get('taskcode', '')
		if not jobactionid or not taskCode:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = jaService.getJobAction(jobactionid)
			if not jobAction:
				raise excUtils.MPSValidationException("Unable to retrieve job action")

			wfService = workflowSvc.WorkflowService(connection)
			workflow = wfService.getWorkflowForJobAction(jobAction, self.getProfile())
			container = workflow.getContainer(taskCode)
			if not container:
				raise excUtils.MPSValidationException("Unable to retrieve container for code '%s'" % taskCode)
			if container.getClassName() not in [constants.kContainerClassPacketDownload, constants.kContainerClassEvaluations]:
				raise excUtils.MPSValidationException("Container is not a '%s' container" % constants.kContainerClassPacketDownload)
			if not container.hasViewPermission():
				raise excUtils.MPSValidationException("Operation not permitted")
			candidate = jaService.getCandidateDict(jobAction)
			title = jaService.getTitle(jobAction)
			department = positionSvc.getDepartment(connection,jobAction.get('position_id',0))
			departmentdescr = department.get('full_descr','')
			sitePreferences = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			altDeptContainerCode = container.getConfigDict().get('altDepartmentContainerCode','')
			if altDeptContainerCode:
				altDepartmentContainer = workflow.getContainer(altDeptContainerCode)
				if altDepartmentContainer:
					altDepartmentItemKey = container.getConfigDict().get('altDepartmentContainerKey','')
					if altDepartmentItemKey:
						altDepartmentContainer.loadInstance()
						altDepartmentContainer.applyResponses()
						questionsByIdentifierCodeCache = altDepartmentContainer.organizeQuestionsByIdentifierCode()
						primaryDepartmentQuestion = questionsByIdentifierCodeCache.get(altDepartmentItemKey,'')
						departmentdescr = ''
						if primaryDepartmentQuestion:
							departmentdescr = uberResolverSvc.UberResolverService(self.dbConnection,{}).resolve(primaryDepartmentQuestion)

			templateLoader = self.getEnvironment().getTemplateLoader()
			templatePref = self.getProfile().get('siteProfile', {}).get('sitePreferences', {}).get('packettoc', 'packetTOC.html')
			templatePath = self.buildFullPathToSiteTemplate(templatePref)
			packetCode = container.getConfigDict().get('packet_code',taskCode)
			titles = self.getTitleArray(connection,title.get('descr',''),departmentdescr,container,workflow)

			header_image_url = ''
			headerImageFilename = container.getConfigDict().get('header_image','')
			if headerImageFilename:
				appCode = envUtils.getEnvironment().getAppCode()
				skin = sitePreferences.get('skin', 'default')
				header_image_url = self._resolveImageURL(appCode, skin, headerImageFilename, workflow, True)

			context={"packet_title":container.getConfigDict().get('title',''),
					"candidate_name":candidate.get('full_name',''),
					"header_image_url":header_image_url,
					"titles":titles,
					"department":departmentdescr,
					"profile":self.getProfile(),
					"handler":self}
			packetGenerator = packetMeister.PacketMaster(connection,packetCode,container.getDescr(),workflow,templateLoader,templatePath,context,container.getConfigDict())
			packetGenerator.generatePacket()
			self.redirect(packetGenerator.getUxPath())
		finally:
			self.closeConnection()

	def _resolveImageURL(self, _appCode, _skin, _imageFilename, _workflow,_isPDF=False):
		if _isPDF:
			skinFolderPath = envUtils.getEnvironment().getSkinFolderPath()
			args = ("file://%s" % skinFolderPath, _skin, _imageFilename)
		else:
			args = (self._getApplicationURLPrefix(_appCode, _workflow), _skin, _imageFilename)
		return '''%s/%s/images/%s''' % args

	def _getApplicationURLPrefix(self, _appCode,_workflow):
		appURL = self._getApplicationURL(_appCode, _workflow)
		return appURL[:appURL.rfind('/')]

	def _getApplicationURL(self, _appCode, _workflow):
		appList = _workflow.getUserProfile().get('siteProfile',{}).get('siteApplications',[])
		for appDict in appList:
			if appDict.get('code','') == _appCode:
				return appDict.get('url','')
		return ''


	def getTitleArray(self,connection,primaryTitle,primaryDepartment,container,workflow):
		titleArray = []
		titleArray.append(primaryTitle + ' - ' + primaryDepartment)
		secondaryItems = container.containerDict.get('config',{}).get('secondaryApptItems',[])
		for itemCode in secondaryItems:
			itemContainer = workflow.getContainer(itemCode)
			if itemContainer:
				if itemContainer.containerDict.get('enabled',False):
					itemContainer.loadInstance()
					confirmedTitleDict = itemContainer.confirmedTitleDict
					if confirmedTitleDict.get('descr',''):
						department = deptSvc.DepartmentService(connection).getDepartment(confirmedTitleDict.get('department_id',-1))
						if department:
							departmentDescr = ' - ' + department.get('full_descr')
							titleArray.append(confirmedTitleDict.get('descr','') + departmentDescr)
		jointSecondariesCode = container.containerDict.get('config',{}).get('secondaryPromoItem','')
		if jointSecondariesCode:
			itemContainer = workflow.getContainer(jointSecondariesCode)
			if itemContainer:
				if itemContainer.containerDict.get('enabled',False):
					itemContainer.loadInstance()
					jointSecondaryPromotions = itemContainer.getJointPromotions()
					if jointSecondaryPromotions:
						for jsp in jointSecondaryPromotions:
							title = titleSvc.TitleService(connection).getTitle(jsp.get('title_id',{}))
							position = positionSvc.getPostionById(connection,jsp.get('position_id',0))
							if title and position:
								department = deptSvc.DepartmentService(self.dbConnection).getDepartment(position.get('department_id',-1))
								if department:
									departmentDescr = ' - ' + department.get('full_descr')
									titleArray.append(title.get('descr','') + departmentDescr)

		return titleArray


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/packet/download/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", PacketDownloadHandler),
]
