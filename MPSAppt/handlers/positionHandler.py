# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jaService
import MPSAppt.core.constants as constants

class PositionViewHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)


	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptPositionView'])

		connection = self.getConnection()
		try:
			allowNewAppoint = False
			allowSecondaryAppoint = False
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			pcn_id = kwargs.get('pcn_id', '')
			position = positionSvc.getPostionById(connection,pcn_id)
			if position.get('is_primary',True):
				allowNewAppoint = True
			else:
				allowSecondaryAppoint = True
			department = positionSvc.getDepartment(connection,position.get('id',0))
			titleDict = lookupTableSvc.getEntityByKey(connection, 'wf_title', position.get('title_id',0), _key='id')
			sitePreferences = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			jaSvc = jaService.JobActionService(connection)
			appointments = jaSvc.getResolvedAppointmentsForPosition(position,sitePreferences)
			for each in appointments:
				if each.get('jobAction',{}):
					try:
						self.validateUserHasAccessToJobAction(connection,community,username,each.get('jobAction',{}))
						each.get('appointment',{})['url'] = self.getJobActionUrl(each.get('jobAction',{}))
					except:
						each.get('appointment',{})['url'] = ''

			if not appointments:
				allowNewAppoint,allowSecondaryAppoint = True,True
			positionId = position.get('id',0)
			titleId = titleDict.get('id',0)
			jobActionMenuList = self.getJobActionMenuList(connection,allowNewAppoint,allowSecondaryAppoint)
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['position_id'] = positionId
			context['appointments'] = appointments
			context['allowNewAppoint'] = allowNewAppoint
			context['allowSecondaryAppoint'] = allowSecondaryAppoint
			context['pcn'] = position.get('pcn','')
			context['department_id'] = department.get('id',0)
			context['department_descr'] = department.get('full_descr','')
			context['title_id'] = titleId
			context['title_descr'] = titleDict.get('descr','')
			context['canCreateAppointment'] = self.hasPermission('apptCreateJobAction')
			context['workflowlist'] = jobActionMenuList
			titleSVC = titleSvc.TitleService(connection)
			titlesList,metatrackId = titleSVC.getTitlesOnEquivalentMetaTrack(titleDict)
			context['track_title_selection'] = titlesList

			self.render("pcn.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

	def getJobActionMenuList(self,connection,allowNewAppoint,allowSecondaryAppoint):
		if self.getSitePreferenceAsBoolean('anyworkflow', 'false'):
			return workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes(constants.kAllJobActionTypesList)

		menuList = []
		if allowNewAppoint:
			appointmentworkflows = workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes([constants.kJobActionTypeNewAppoint])
			if appointmentworkflows:
				menuList.extend(appointmentworkflows)
		if allowSecondaryAppoint:
			insideSecondaryworkflows = workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes([constants.kJobActionTypeSecondaryApptInside])
			if insideSecondaryworkflows:
				menuList.extend(insideSecondaryworkflows)
			outsideSecondaryworkflows = workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes([constants.kJobActionTypeSecondaryApptOutside])
			if outsideSecondaryworkflows:
				menuList.extend(outsideSecondaryworkflows)
		return menuList


class CreatePositionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreatePosition')

		#   Department Code is required.

		deptId = kwargs.get('dept_id', '')
		if not deptId:
			self.redirect("/appt")
			return

		titleId = kwargs.get('title_id', '')
		if not titleId:
			self.redirect("/appt")
			return

		#   Find the Department.
		#   The user must have access to the Department.

		connection = self.getConnection()
		try:
			departmentDict = deptSvc.DepartmentService(self.dbConnection).getDepartment(deptId)
			if not departmentDict:
				raise excUtils.MPSValidationException("Department not found")

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			departmentList = deptSvc.DepartmentService(self.dbConnection).getDepartmentsForUser(community, username)
			if not self.isDepartmentInDepartmentList(departmentDict.get('code',''), departmentList):
				raise excUtils.MPSValidationException("Operation not permitted")

			titleDict = lookupTableSvc.getEntityByKey(connection, 'wf_title', titleId, 'id')
			if not titleDict:
				raise excUtils.MPSValidationException("Title not found")

			#   Create the Position.

			formData = tornado.escape.json_decode(self.request.body)
			manualpcn = ''
			if formData.has_key('manualpcn'):
				manualpcn = formData.get('manualpcn','')
				if not manualpcn:
					raise excUtils.MPSValidationException("PCN is required")
				if positionSvc.getPostionFromPCN(self.dbConnection,manualpcn):
					raise excUtils.MPSValidationException("This PCN already exists")

			positionDict = {}
			positionDict['manualpcn'] = manualpcn
			positionDict['department_id'] = departmentDict.get('id', None)
			positionDict['title_id'] = titleDict.get('id', None)
			positionDict['is_primary'] = True
			positionDict['created'] = self.getEnvironment().formatUTCDate()
			positionDict['updated'] = positionDict['created']
			positionDict['lastuser'] = username
			positionId = positionSvc.createPosition(connection, positionDict, departmentDict)
			position = positionSvc.getPostionById(connection,positionId)
			pcnNumber = '' if not position else position.get('pcn','')
			if formData.get('manualpcn',''):
				pcnNumber = manualpcn

			responseDict = self.getPostResponseDict("Position created")
			# New: Re-Use page after Position Create to show link Created Position VS. allow user to create another
			responseDict['custom_page_response'] = {
				'positionId': positionId,
				'pcn': pcnNumber,
				'showRosterLink': self.hasPermission('apptRosterView')
			}

			if self.hasPermission('apptRosterView'):
				responseDict['redirect'] = '/appt/page/roster'
			else:
				responseDict['redirect'] = '/appt'

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def isDepartmentInDepartmentList(self, _deptCode, _departmentList):
		for departmentDict in _departmentList:
			thisDeptCode = departmentDict.get('code', '')
			if thisDeptCode == _deptCode:
				return True
		return False

class CreatePositionViewHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)


	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreatePosition'])

		connection = self.getConnection()
		try:
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			titleSVC = titleSvc.TitleService(connection)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			deptService = deptSvc.DepartmentService(connection)
			userdepartmentList = deptService.getDepartmentsForUser(community, username)

			departmentList = deptService.getDepartmentHierarchy(userdepartmentList, _excludeInactive=True)
			titlesList = titleSVC.getTitlesByTrack()
			# if this preference is set to 'manual', user will need to enter a pcn manually vs. having it generated.
			pcnpref = self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('pcncreationmethod','')
			context['pcn_creation'] = pcnpref.lower()
			context['track_title_selection'] = titlesList
			context['department_selection'] = departmentList

			self.render("pcncreate.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

class DeletePositionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreatePosition')

		#   PCN ID is required.

		pcnID = kwargs.get('pcn_id', '')
		if not pcnID:
			self.redirect("/appt")
			return

		#   Find the Department.
		#   The user must have access to the Department.

		connection = self.getConnection()
		try:

			positionIsInUse = jaService.JobActionService(connection).positionIsInUse(pcnID)
			if positionIsInUse:
				raise excUtils.MPSValidationException("Position is in use. Operation not permitted")

			positionSvc.deletePosition(connection,pcnID)

			responseDict = self.getPostResponseDict("Position deleted")
			if self.hasPermission('apptRosterView'):
				responseDict['redirect'] = '/appt/page/roster'
			else:
				responseDict['redirect'] = '/appt'
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


#   All URL mappings for this module.
urlMappings = [
	(r"/appt/pcn/(?P<pcn_id>[^/]*)", PositionViewHandler),
	(r"/appt/pcncreate", CreatePositionViewHandler),
	(r"/appt/pcncreate/(?P<dept_id>[^/]*)/(?P<title_id>[^/]*)", CreatePositionHandler),
	(r"/appt/pcndelete/(?P<pcn_id>[^/]*)", DeletePositionHandler),
]
