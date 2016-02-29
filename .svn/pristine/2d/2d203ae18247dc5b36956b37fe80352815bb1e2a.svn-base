# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import json
import os
import os.path
import tornado.escape
import pprint
import inspect

import MPSAppt.core.constants as constants
import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.core.workflow as wf
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.workflowComponentService as workflowComponentSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.core.sql.lookupTableSQL as lookupSQL
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.exceptionUtils as excUtils

kWfEditModeItem = 'item'
kWfEditModeRaw = 'raw'

kWfViewModeFull = 'full'
kWfViewModeUX = 'ux'

kWfEditRawErrorFieldName = 'data'

class AbstractAdminWorkflowHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	#   Permissions

	def initPermissions(self):
		self.canRaw = self.hasPermission('apptWFEditRaw')
		self.canCreateWorkflow = self.canRaw or self.hasPermission('apptWFEditCreateWorkflow')
		self.canCreateComponent = self.canRaw or self.hasPermission('apptWFEditCreateComponent')
		self.canCreateTitleOverride = self.canRaw or self.hasPermission('apptWFEditCreateTitleOverride')
		self.canDeleteComponent = self.canRaw or self.hasPermission('apptWFEditDeleteComponent')
		self.canDeleteTitleOverride = self.canRaw or self.hasPermission('apptWFEditDeleteTitleOverride')
		self.canEditCode = self.canRaw or self.hasPermission('apptWFEditCode')
		self.canEditComponentType = self.canRaw or self.hasPermission('apptWFEditComponentType')
		self.canEditClassName = self.canRaw or self.hasPermission('apptWFEditClassName')
		self.canEditMetaTrackCode = self.canRaw or self.hasPermission('apptWFEditMetaTrackCode')
		self.canEditJobActionType = self.canRaw or self.hasPermission('apptWFEditJobActionType')
		self.canEditPermissions = self.canRaw or self.hasPermission('apptWFEditPermissions')
		self.canEditBlockers = self.canRaw or self.hasPermission('apptWFEditBlockers')

	def addPermissionsToContext(self, _context):
		_context['canRaw'] = self.canRaw
		_context['canCreateWorkflow'] = self.canCreateWorkflow
		_context['canCreateComponent'] = self.canCreateComponent
		_context['canCreateTitleOverride'] = self.canCreateTitleOverride
		_context['canDeleteComponent'] = self.canDeleteComponent
		_context['canDeleteTitleOverride'] = self.canDeleteTitleOverride
		_context['canEditCode'] = self.canEditCode
		_context['canEditComponentType'] = self.canEditComponentType
		_context['canEditClassName'] = self.canEditClassName
		_context['canEditMetaTrackCode'] = self.canEditMetaTrackCode
		_context['canEditJobActionType'] = self.canEditJobActionType
		_context['canEditPermissions'] = self.canEditPermissions
		_context['canEditBlockers'] = self.canEditBlockers

	def getInitialTemplateContext(self, _environment=None):
		context = super(AbstractAdminWorkflowHandler, self).getInitialTemplateContext(_environment)
		self.addPermissionsToContext(context)
		return context

	#   Kwarging

	def getWfId(self, _isRequired=True, **kwargs):
		wfId = kwargs.get('wfId', 0)
		if (_isRequired) and (not wfId):
			raise excUtils.MPSValidationException("Unknown workflow identifier")
		return wfId

	def getTitleId(self, _isRequired=False, **kwargs):
		titleId = kwargs.get('titleId', 0)
		if (_isRequired) and ((not titleId) or (titleId == '0')):
			raise excUtils.MPSValidationException("Unknown title identifier")
		return titleId

	def getContainerCode(self, _isRequired=True, **kwargs):
		containerCode = kwargs.get('containerCode', '')
		if (_isRequired) and (not containerCode):
			raise excUtils.MPSValidationException("Unknown container identifier")
		return containerCode

	def getEditMode(self, _isRequired=True, **kwargs):
		editMode = kwargs.get('editMode', '')
		if editMode in (kWfEditModeItem, kWfEditModeRaw):
			return editMode
		if _isRequired:
			raise excUtils.MPSValidationException("Unknown edit mode")
		if self.hasAnyPermission(['apptWFEditRaw']):
			return kWfEditModeRaw
		return kWfEditModeItem

	def getViewMode(self, _isRequired=True, **kwargs):
		viewMode = kwargs.get('viewMode', '')
		if viewMode in (kWfViewModeFull, kWfViewModeUX):
			return viewMode
		if _isRequired:
			raise excUtils.MPSValidationException("Unknown view mode")
		return kWfViewModeFull

	#   Lookin' and Searchin'

	def getWorkflow(self, _wfService, _wfId):
		wfDict = _wfService.getWorkflowById(_wfId)
		if not wfDict:
			raise excUtils.MPSValidationException("Workflow not found")
		return wfDict

	def getTitle(self, _connection, _titleId):
		titleService = titleSvc.TitleService(_connection)
		titleDict = titleService.getTitle(_titleId)
		if not titleDict:
			raise excUtils.MPSValidationException("Title not found")
		return titleDict

	def getContainer(self, _wfService, _containerCode):
		containerDict = _wfService.getComponentByCode(_containerCode)
		if not containerDict:
			raise excUtils.MPSValidationException("Container not found")
		return containerDict


	#   Validation and utility methods.

	def validateComponentType(self, _connection, _componentTypeStr, _errorCode):
		componentTypeCache = lookupSvc.getLookupTable(_connection, 'wf_component_type', _key='code')
		componentTypeDict = componentTypeCache.get(_componentTypeStr.upper(), {})
		if not componentTypeDict:
			self.raiseValidationError(_errorCode, "Unknown Component Type '%s'" % _componentTypeStr)
		return componentTypeDict

	def validateJobActionType(self, _connection, _jobActionTypeStr, _errorCode):
		jobActionTypeCache = self.getJobActionTypeCache(_connection)
		jobActionTypeDict = jobActionTypeCache.get(_jobActionTypeStr.upper(), {})
		if not jobActionTypeDict:
			self.raiseValidationError(_errorCode, "Unknown Job Action Type '%s'" % _jobActionTypeStr)
		return jobActionTypeDict

	def listifyCommaSeparatedInput(self, _data, _jErrors=None, _optionalValidationList=None):
		result = []
		for each in _data.split(','):
			value = str(each).strip()
			if value:
				if (_optionalValidationList is not None) and \
					(_jErrors is not None) and \
					(value not in _optionalValidationList):
					_jErrors.append({ 'code': 'metaTrackCodes', 'message': 'Unknown value: %s' % value })
				else:
					if value not in result:
						result.append(value)
		return result

	def isWorkflow(self, _componentTypeDict):
		return _componentTypeDict.get('code', '').upper() == 'WORKFLOW'

	def isContainer(self, _componentTypeDict):
		return _componentTypeDict.get('code', '').upper() == 'CONTAINER'

	def isTask(self, _componentTypeDict):
		return _componentTypeDict.get('code', '').upper() == 'TASK'

	def raiseValidationError(self, _code, _message):
		jErrors = [ { 'code': _code, 'message': _message } ]
		raise excUtils.MPSValidationException(jErrors)

	#   List/Cache utilities

	def getComponentTypeList(self, _includeWorkflow=True):
		task = { 'code':'TASK', 'descr':'Task' }
		container = { 'code':'CONTAINER', 'descr':'Container' }
		workflow = { 'code':'WORKFLOW', 'descr':'Workflow' }
		if _includeWorkflow:
			return [ task, container, workflow ]
		return [ task, container ]

	def getAffordanceTypeList(self):
		blank = { 'code':'', 'descr':'' }
		tab = { 'code':'TAB', 'descr':'Tab' }
		section = { 'code':'SECTION', 'descr':'Section' }
		item = { 'code':'ITEM', 'descr':'Item' }
		return [ blank, tab, section, item ]

	def getAffordanceTypeCache(self):
		cache = {}
		for each in self.getAffordanceTypeList():
			cache[each['code']] = each
		return cache

	def getClassNameList(self):
		nameList = []
		for memberTuple in inspect.getmembers(constants):
			if memberTuple[0].startswith('kContainerClass'):
				nameList.append(memberTuple[1])
		return nameList

	def getMetatrackNameList(self, _connection):
		metatrackCache = lookupSvc.getLookupTable(_connection, 'wf_metatrack', _key='code')
		return metatrackCache.keys()

	def getJobActionTypeList(self, _connection):
		return lookupSQL.getLookupTable(_connection, 'wf_job_action_type', _orderBy='descr')

	def getJobActionTypeCache(self, _connection):
		cache = {}
		for each in self.getJobActionTypeList(_connection):
			cache[each['code']] = each
		return cache


#   Render Workflow page

class WorkflowHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()

		currentTitle = {}
		currentWorkflow = {}
		currentViewMode = {}

		currentWorkflowData = {}
		currentWorkflowUX = {}

		connection = self.getConnection()
		try:
			wfId = self.getWfId(_isRequired=False, **kwargs)
			titleId = self.getTitleId(_isRequired=False, **kwargs)
			editMode = self.getEditMode(_isRequired=False, **kwargs)
			viewMode = self.getViewMode(_isRequired=False, **kwargs)

			if not titleId:
				titleId = 0
			workflowList = self.getWorkflowList(connection, titleId, editMode, viewMode)

			if (not wfId) and (workflowList):
				wfId = workflowList[0].get('id', 0)
			if not wfId:
				wfId = 0
				if workflowList:
					wfId = workflowList[0].get('id', 0)

			titleList = self.getTitleHierarchy(connection, wfId, editMode, viewMode)
			if titleList:
				if (not titleId) or (titleId == '0'):
					currentTitle = titleList[0]
				else:
					for each in titleList:
						for child in each.get('children', []):
							if str(titleId) == str(child.get('id', 0)):
								currentTitle = child
								break

			viewModeList = self.getViewModeList(wfId, titleId, editMode)
			for each in viewModeList:
				if viewMode == each.get('code', ''):
					currentViewMode = each
					break

			parameterBlock = {}
			if wfId:
				for each in workflowList:
					if str(wfId) == str(each.get('id', 0)):
						currentWorkflowData = each
						break

				if currentWorkflowData:
					parameterBlock['userProfile'] = self.getProfile()
					parameterBlock['userPermissions'] = self.getUserProfile().get('userPermissions', [])
					parameterBlock['titleCode'] = currentTitle.get('code', '')
					parameterBlock['ignoreMissingContainers'] = True
					currentWorkflow = wf.Workflow(connection)
					currentWorkflow.buildWorkflow(currentWorkflowData.get('code', ''), parameterBlock)

					if viewMode == kWfViewModeUX:
						currentWorkflowUX = currentWorkflow.getWFAdminUI(wfId, titleId, editMode, viewMode)
					else:
						container = currentWorkflow.getMainContainer()
						if container:
							self.getAdditionalContainerInfo(container, wfId, titleId, editMode, viewMode)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['wfId'] = wfId
			context['workflowList'] = workflowList
			context['currentWorkflow'] = currentWorkflow
			context['currentWorkflowData'] = currentWorkflowData
			context['currentWorkflowUX'] = currentWorkflowUX

			context['titleId'] = titleId
			context['titleList'] = titleList
			context['currentTitle'] = currentTitle

			context['viewMode'] = viewMode
			context['viewModeList'] = viewModeList
			context['currentViewMode'] = currentViewMode

			context['hasMissingContainers'] = parameterBlock.get('hasMissingContainers', False)
			context['missingContainers'] = parameterBlock.get('missingContainers', [])

			if self.canCreateWorkflow:
				context['createWorkflowUrl'] = "/appt/wf/createworkflow/%s/%s/%s/%s" % (str(wfId), str(titleId), editMode, viewMode)
			if self.canCreateComponent:
				context['createComponentUrl'] = "/appt/wf/createcomponent/%s/%s/%s/%s" % (str(wfId), str(titleId), editMode, viewMode)

			self.render('adminWorkflow.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def getWorkflowList(self, _connection, _titleId, _editMode, _viewMode):
		wfService = workflowSvc.WorkflowService(_connection)
		rawWorkflowList = wfService.getWorkflows()
		jaTypeCache = lookupSvc.getLookupTable(_connection, 'wf_job_action_type', _key='id')

		wfList = []
		for wfDict in rawWorkflowList:
			jaTypeId = wfDict.get('job_action_type_id', -1)
			jaTypeDict = jaTypeCache.get(jaTypeId, None)
			if (jaTypeDict) and (jaTypeDict.get('active', False)):
				wfDict['job_action_type_code'] = jaTypeDict.get('code', '')
				wfDict['job_action_type_descr'] = jaTypeDict.get('descr', '')
				wfDict['url'] = "/appt/wf/%s/%s/%s/%s" % (str(wfDict.get('id', 0)), str(_titleId), _editMode, _viewMode)
				wfList.append(wfDict)
		return wfList

	def getTitleHierarchy(self, _connection, _wfId, _editMode, _viewMode):
		titleService = titleSvc.TitleService(_connection)
		titleHierarchy = titleService.getTitleHierarchy(_includeInactive=True)
		for trackDict in titleHierarchy:
			for titleDict in trackDict.get('children', []):
				titleId = titleDict.get('id', 0)
				titleDict['url'] = "/appt/wf/%s/%s/%s/%s" % (str(_wfId), str(titleId), _editMode, _viewMode)

		noneDict = { 'id':0, 'descr':'None' }
		noneDict['url'] = "/appt/wf/%s/0/%s/%s" % (str(_wfId), _editMode, _viewMode)
		titleHierarchy.insert(0, noneDict)
		return titleHierarchy

	def getViewModeList(self, _wfId, _titleId, _editMode):
		fullMode = { 'code':kWfViewModeFull, 'descr':'Full Workflow' }
		fullMode['url'] = "/appt/wf/%s/%s/%s/%s" % (str(_wfId), str(_titleId), _editMode, kWfViewModeFull)
		uxMode = { 'code':kWfViewModeUX, 'descr':'UX View' }
		uxMode['url'] = "/appt/wf/%s/%s/%s/%s" % (str(_wfId), str(_titleId), _editMode, kWfViewModeUX)
		return [ fullMode, uxMode ]

	def getAdditionalContainerInfo(self, _container, _wfId, _titleId, _editMode, _viewMode):
		contDict = _container.getContainerDict()
		contDict['url'] = "/appt/wf/edit/%s/%s/%s/%s/%s" % (str(_wfId), str(_titleId), _container.getCode(), _editMode, _viewMode)

		componentType = contDict.get('componentType', '')
		className = contDict.get('className', '')
		enabled = str(contDict.get('enabled', True))
		optional = str(contDict.get('optional', False))
		contDict['tooltip'] = 'componentType: %s\nclassName: %s\nenabled: %s\noptional: %s' % (componentType, className, enabled, optional)

		for child in _container.getContainers():
			self.getAdditionalContainerInfo(child,  _wfId, _titleId, _editMode, _viewMode)


#   Render Workflow Edit page

class WorkflowComponentEditHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		containerCode = self.getContainerCode(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)
			containerDict = self.getContainer(wfService, containerCode)

			titleDict = { 'descr': 'None' }
			hasTitleOverride = False
			isTitleOverride = True if (titleId) and (titleId != '0') else False
			if isTitleOverride:
				titleDict = self.getTitle(connection, titleId)

			overrideDict = {}
			if isTitleOverride:
				titleCode = titleDict.get('code', '')
				override = wfService.getTitleOverrideForWorkflowComponentTitle(wfDict.get('code', ''), titleCode, containerCode)
				if override:
					overrideDict = override
					hasTitleOverride = True

			rawData = ''
			componentDataDict = {}
			if editMode == kWfEditModeRaw:
				if isTitleOverride:
					if hasTitleOverride:
						value = overrideDict.get('value', '')
						if value:
							rawData = json.dumps(json.loads(value), indent=4)
				else:
					rawData = containerDict.get('src', '')
			else:
				if isTitleOverride:
					pass
				else:
					rawData = containerDict.get('src', '')
					exec(rawData)
					componentDataDict = eval(containerCode)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['wfId'] = wfId
			context['wfDict'] = wfDict
			context['titleId'] = titleId
			context['titleDict'] = titleDict
			context['containerCode'] = containerCode
			context['containerDict'] = containerDict
			context['isTitleOverride'] = isTitleOverride
			context['hasTitleOverride'] = hasTitleOverride
			context['overrideDict'] = overrideDict
			context['viewMode'] = viewMode
			context['editMode'] = editMode
			context['rawData'] = rawData
			context['classNameList'] = self.getClassNameList()
			context['metatrackNameList'] = self.getMetatrackNameList(connection)
			context['jobActionTypeList'] = self.getJobActionTypeList(connection)

			if editMode == kWfEditModeRaw:
				context['canUseItemEditMode'] = True
				context['itemEditModeUrl'] = "/appt/wf/edit/%s/%s/%s/%s/%s" % (str(wfId), str(titleId), containerCode, kWfEditModeItem, viewMode)
			else:
				if self.canRaw:
					context['canUseRawEditMode'] = True
					context['rawEditModeUrl'] = "/appt/wf/edit/%s/%s/%s/%s/%s" % (str(wfId), str(titleId), containerCode, kWfEditModeRaw, viewMode)

				context['componentDataDict'] = componentDataDict
				context['componentTypeList'] = self.getComponentTypeList()
				context['affordanceTypeList'] = self.getAffordanceTypeList()

			if self.canRaw and (not isTitleOverride):
				context['canWriteSingleFileToDisk'] = True

			self.render('adminWorkflowEdit.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Save Workflow Edit page

class AbstractWorkflowComponentSaveHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		containerCode = self.getContainerCode(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)
		isWriteFile = kwargs.get('writeFile', False)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)
			containerDict = self.getContainer(wfService, containerCode)

			titleDict = { 'descr': 'None' }
			isTitleOverride = True if (titleId) and (titleId != '0') else False
			if isTitleOverride:
				titleDict = self.getTitle(connection, titleId)

			if (isTitleOverride) and (isWriteFile):
				raise excUtils.MPSValidationException("Not supported for Title Overrides")

			overrideDict = {}
			if isTitleOverride:
				titleCode = titleDict.get('code', '')
				overrideDict = wfService.getTitleOverrideForWorkflowComponentTitle(wfDict.get('code', ''), titleCode, containerCode)
				if not overrideDict:
					raise excUtils.MPSValidationException("Title Override not found.")

			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)
			if isTitleOverride:
				message = "Title Override saved"
				if editMode == kWfEditModeItem:
					raise excUtils.MPSValidationException("We don't do Item Edit Mode yet.")
				else:
					#   Title Override, raw mode.
					self.processTitleOverrideInRawMode(connection, overrideDict, formData)
			else:
				message = "Component saved"
				if editMode == kWfEditModeItem:
					self.processBaseComponentInItemMode(connection, containerDict, formData)
				else:
					#   Base component, raw mode.
					self.processBaseComponentInRawMode(connection, containerDict, formData)

			#   Write the component source, if requested.

			if isWriteFile:
				message += ", file written to source tree"
				containerDict = wfService.getComponentByCode(containerCode)
				carRelativePath = containerDict.get('car_relative_path', '')
				if not carRelativePath:
					raise excUtils.MPSValidationException("File has no relative path in source tree")

				root = envUtils.getEnvironment().getSrcRootFolderPath()
				dstPath = os.path.join(root, 'data', 'atramData') + carRelativePath

				f = None
				try:
					f = open(dstPath, 'w')
					f.write(containerDict.get('src', ''))
				finally:
					if f:
						try: f.close()
						except Exception, e: pass

			responseDict = self.getPostResponseDict(message)
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + "/wf/%s/%s/%s/%s" % (str(wfId), str(titleId), editMode, viewMode)
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def processBaseComponentInRawMode(self, _connection, _containerDict, _formData):
		data = ''
		dataDict = {}
		value = ''

		#   Base component, raw mode.
		#   Ensure we can parse the data.

		oldContainerCode = _containerDict.get('code', '')
		try:
			data = _formData.get('data', '')
			exec(data)
			dataDict = eval(oldContainerCode)
			value = json.dumps(dataDict)
		except Exception, e:
			self.raiseRawError(e.__repr__())

		#   Extract and validate updated values.

		newContainerCode = dataDict.get('code', '')
		newDescr = dataDict.get('descr', '')
		newComponentTypeStr = dataDict.get('componentType', '')
		newComponentTypeDict = self.validateComponentType(_connection, newComponentTypeStr, kWfEditRawErrorFieldName)
		newComponentTypeId = newComponentTypeDict.get('id', 0)
		relativePath = str(_formData.get('car_relative_path', '')).strip()

		#   Watch for changes to the Container Code.

		if oldContainerCode != newContainerCode:
			old = "%s = {" % oldContainerCode
			new = "%s = {" % newContainerCode
			data = data.replace(old, new, 1)

		#   Persist modifications.

		_containerDict['code'] = newContainerCode
		_containerDict['descr'] = newDescr
		_containerDict['component_type_id'] = newComponentTypeId
		_containerDict['src'] = data
		_containerDict['value'] = value
		if relativePath:
			_containerDict['car_relative_path'] = relativePath
		workflowComponentSvc.WorkflowComponentService(_connection).updateComponent(_containerDict)

	def processTitleOverrideInRawMode(self, _connection, _overrideDict, _formData):
		dataDict = {}

		#   Title override, raw mode.
		#   Ensure we can parse the data.

		try:
			data = _formData.get('data', '')
			dataDict = json.loads(data)
		except Exception, e:
			self.raiseRawError(e.__repr__())

		#   Verify that key field values were not changed:
		#       workflow_code
		#       component_code
		#       title_code

		if _overrideDict.get('workflow_code', '') != dataDict.get('workflowCode', ''):
			raise excUtils.MPSValidationException("Editing workflowCode is not allowed.")
		if _overrideDict.get('component_code', '') != dataDict.get('componentCode', ''):
			raise excUtils.MPSValidationException("Editing componentCode is not allowed.")
		if _overrideDict.get('title_code', '') != dataDict.get('titleCode', ''):
			raise excUtils.MPSValidationException("Editing titleCode is not allowed.")

		#   Persist modifications.

		_overrideDict['value'] = json.dumps(dataDict)
		workflowComponentSvc.WorkflowComponentService(_connection).updateComponentOverride(_overrideDict)

	def processBaseComponentInItemMode(self, _connection, _containerDict, _formData):
		oldContainerCode = _containerDict.get('code', '')
		rawData = _containerDict.get('src', '')
		exec(rawData)
		componentDataDict = eval(oldContainerCode)
		oldJobActionType = componentDataDict.get('jobActionType', '')

		#   Check for errors, Narc'em.

		jErrors = []
		self._processCommonItems(_connection, componentDataDict, _formData, jErrors)
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

		#   Manufacture Container record changes, and persist.

		newContainerCode = componentDataDict.get('code', '')
		_containerDict['code'] = newContainerCode
		_containerDict['descr'] = componentDataDict.get('descr', '')
		if self.canEditComponentType:
			_containerDict['component_type_id'] = componentDataDict.get('componentTypeId', 0)
			if 'componentTypeId' in componentDataDict:
				del componentDataDict['componentTypeId']

		_containerDict['src'] = "%s = %s" % (newContainerCode, pprint.pformat(componentDataDict))
		_containerDict['value'] = json.dumps(componentDataDict)

		if oldContainerCode != newContainerCode:
			carRelativePath = _containerDict.get('car_relative_path', '')
			if carRelativePath:
				oldFilename = oldContainerCode + '.py'
				if carRelativePath.endswith(oldFilename):
					newFilename = newContainerCode + '.py'
					_containerDict['car_relative_path'] = carRelativePath.replace(oldFilename, newFilename)

		componentService = workflowComponentSvc.WorkflowComponentService(_connection)
		componentService.updateComponent(_containerDict)

		#   Update wf_workflow.job_action_type_id if required.

		newJobActionType = componentDataDict.get('jobActionType', '')
		if oldJobActionType != newJobActionType:
			newJobActionTypeDict = self.validateJobActionType(_connection, newJobActionType, '')
			if newJobActionTypeDict:
				newJobActionTypeId = newJobActionTypeDict.get('id', 0)
				if newJobActionTypeId:
					workflowDict = workflowSvc.WorkflowService(_connection).getWorkflow(newContainerCode)
					if workflowDict:
						oldJobActionTypeId = workflowDict.get('job_action_type_id', 0)
						if oldJobActionTypeId != newJobActionTypeId:
							workflowDict['job_action_type_id'] = newJobActionTypeId
							componentService.updateWorkflow(workflowDict)

	def _processCommonItems(self, _connection, _componentDataDict, _formData, jErrors):
		#   Check required fields.
		requiredFields = ['descr']
		if self.canEditCode:
			requiredFields.append('code')
		if self.canEditComponentType:
			requiredFields.append('componentType')
		if self.canEditClassName:
			requiredFields.append('className')
		for fieldCode in requiredFields:
			fieldValue = str(_formData.get(fieldCode, '')).strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		newComponentTypeStr = _componentDataDict.get('componentType', '')
		if self.canEditComponentType:
			newComponentTypeStr = str(_formData.get('componentType', '')).strip()
		newComponentTypeDict = self.validateComponentType(_connection, newComponentTypeStr, 'componentType')

		newAffordanceTypeStr = str(_formData.get('affordanceType', '')).strip()
		newAffordanceTypeDict = self.validateAffordanceType(newAffordanceTypeStr, 'affordanceType')

		#   Poke new values in the component dictionary.
		if self.canEditCode:
			_componentDataDict['code'] = str(_formData.get('code', '')).strip()
		if self.canEditClassName:
			_componentDataDict['className'] = str(_formData.get('className', '')).strip()
		if self.canEditComponentType:
			_componentDataDict['componentType'] = newComponentTypeDict.get('descr', '')
			_componentDataDict['componentTypeId'] = newComponentTypeDict.get('id', 0)
		if self.canEditPermissions:
			_componentDataDict['accessPermissions'] = self.listifyCommaSeparatedInput(_formData.get('accessPermissions', ''))
			_componentDataDict['viewPermissions'] = self.listifyCommaSeparatedInput(_formData.get('viewPermissions', ''))
		if self.canEditBlockers:
			_componentDataDict['blockers'] = self.listifyCommaSeparatedInput(_formData.get('blockers', ''))

		_componentDataDict['descr'] = str(_formData.get('descr', '')).strip()
		_componentDataDict['affordanceType'] = newAffordanceTypeDict.get('descr', '')
		_componentDataDict['optional'] = True if str(_formData.get('optional', '')).strip() == 'true' else False
		_componentDataDict['enabled'] = True if str(_formData.get('enabled', '')).strip() == 'true' else False
		_componentDataDict['statusMsg'] = str(_formData.get('statusMsg', '')).strip()
		_componentDataDict['comment'] = str(_formData.get('comment', '')).strip()

		if self.isTask(newComponentTypeDict):
			_componentDataDict['logEnabled'] = True if str(_formData.get('logEnabled', '')).strip() == 'true' else False
			_componentDataDict['freezable'] = True if str(_formData.get('freezable', '')).strip() == 'true' else False
			_componentDataDict['overviewOnly'] = True if str(_formData.get('overviewOnly', '')).strip() == 'true' else False
			_componentDataDict['isProtectedCandidateItem'] = True if str(_formData.get('isProtectedCandidateItem', '')).strip() == 'true' else False
			_componentDataDict['successMsg'] = str(_formData.get('successMsg', '')).strip()

		if self.isWorkflow(newComponentTypeDict) or self.isContainer(newComponentTypeDict):
			_componentDataDict['containers'] = self.listifyCommaSeparatedInput(_formData.get('containers', ''))

			if self.isWorkflow(newComponentTypeDict):
				if self.canEditMetaTrackCode:
					_componentDataDict['metaTrackCodes'] = self.listifyCommaSeparatedInput(_formData.get('metaTrackCodes', ''), jErrors, _optionalValidationList=self.getMetatrackNameList(_connection))

				if self.canEditJobActionType:
					newJobActionTypeStr = str(_formData.get('jobActionType', '')).strip()
					newJobActionTypeDict = self.validateJobActionType(_connection, newJobActionTypeStr, 'jobActionType')
					if newJobActionTypeDict:
						_componentDataDict['jobActionType'] = newJobActionTypeDict.get('code', '')


	#   Validation and utility methods.

	def validateAffordanceType(self, _affordanceTypeStr, _errorCode):
		affordanceTypeCache = self.getAffordanceTypeCache()
		affordanceTypeDict = affordanceTypeCache.get(_affordanceTypeStr.upper(), {})
		if not affordanceTypeDict:
			self.raiseValidationError(_errorCode, "Unknown Affordance Type '%s'" % _affordanceTypeStr)
		return affordanceTypeDict

	def raiseRawError(self, _message):
		self.raiseValidationError(kWfEditRawErrorFieldName, _message)

class WorkflowComponentSaveHandler(AbstractWorkflowComponentSaveHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form save requests.

	def post(self, **kwargs):
		try:
			kwargs['writeFile'] = False
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

class WorkflowComponentWriteHandler(AbstractWorkflowComponentSaveHandler):
	logger = logging.getLogger(__name__)

	#   POST handles form save requests, followed by component write request.

	def post(self, **kwargs):
		try:
			kwargs['writeFile'] = True
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)


#   Create Workflow

class WorkflowCreateHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	#   GET renders the create workflow page.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()
		if not self.canCreateWorkflow:
			raise excUtils.MPSValidationException("Operation not permitted")

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['wfId'] = wfId
			context['wfDict'] = wfDict
			context['titleId'] = titleId
			context['viewMode'] = viewMode
			context['editMode'] = editMode
			context['jobActionTypeList'] = self.getJobActionTypeList(connection)

			self.render('adminWorkflowCreateWorkflow.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


	#   POST creates new workflows.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()
		if not self.canCreateWorkflow:
			raise excUtils.MPSValidationException("Operation not permitted")

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)
			formData = tornado.escape.json_decode(self.request.body)

			#   Check for errors, Narc'em.
			jErrors = []
			workflowDict, componentDict = self.validateFormData(connection, wfDict, formData, jErrors)
			if jErrors:
				raise excUtils.MPSValidationException(jErrors)

			#   Persist.
			workflowComponentSvc.WorkflowComponentService(connection).createWorkflow(workflowDict, doCommit=False)
			workflowComponentSvc.WorkflowComponentService(connection).createComponent(componentDict)

			newWfId = 0
			newWfDict = wfService.getWorkflow(workflowDict.get('code', ''))
			if newWfDict:
				newWfId = newWfDict.get('id', 0)
			responseDict = self.getPostResponseDict("Workflow created")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + "/wf/%s/%s/%s/%s" % (str(newWfId), str(titleId), editMode, viewMode)
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _wfDict, _formData, jErrors):
		#   Check required fields.
		requiredFields = ['code','descr','jobActionType']
		for fieldCode in requiredFields:
			fieldValue = str(_formData.get(fieldCode, '')).strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		jobActionTypeStr = str(_formData.get('jobActionType', '')).strip()
		jobActionTypeDict = self.validateJobActionType(_connection, jobActionTypeStr, 'jobActionType')
		metaTrackCodes = self.listifyCommaSeparatedInput(_formData.get('metaTrackCodes', ''), jErrors, _optionalValidationList=self.getMetatrackNameList(_connection))
		componentTypeDict = self.validateComponentType(_connection, 'Workflow', '')

		#   Build a workflow.
		#   Build a component.
		#   Build a component data dictionary.

		componentDataDict = {}
		componentDataDict['code'] = str(_formData.get('code', '')).strip()
		componentDataDict['descr'] = str(_formData.get('descr', '')).strip()
		componentDataDict['componentType'] = 'Workflow'
		componentDataDict['className'] = constants.kContainerClassContainer
		componentDataDict['affordanceType'] = ''
		componentDataDict['optional'] = False
		componentDataDict['enabled'] = False
		componentDataDict['accessPermissions'] = []
		componentDataDict['viewPermissions'] = []
		componentDataDict['blockers'] = []
		componentDataDict['statusMsg'] = ''
		componentDataDict['comment'] = ''
		componentDataDict['logEnabled'] = False
		componentDataDict['containers'] = []
		componentDataDict['metaTrackCodes'] = metaTrackCodes
		componentDataDict['jobActionType'] = jobActionTypeDict.get('code', '')

		componentDict = {}
		componentDict['code'] = componentDataDict['code']
		componentDict['descr'] = componentDataDict['descr']
		componentDict['component_type_id'] = componentTypeDict.get('id', 0)
		componentDict['is_site_override'] = True
		componentDict['value'] = json.dumps(componentDataDict)
		componentDict['src'] = "%s = %s" % (componentDataDict['code'], pprint.pformat(componentDataDict))
		componentDict['car_relative_path'] = '/sites/%s/components/%s/%s.py' % (self.getProfile().get('siteProfile', {}).get('site', ''), componentDataDict['code'], componentDataDict['code'])

		workflowDict = {}
		workflowDict['code'] = componentDataDict['code']
		workflowDict['descr'] = componentDataDict['descr']
		workflowDict['job_action_type_id'] =  jobActionTypeDict.get('id', 0)

		return workflowDict, componentDict


#   Create Workflow Component

class WorkflowComponentCreateHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	#   GET renders the create component page.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()
		if not self.canCreateComponent:
			raise excUtils.MPSValidationException("Operation not permitted")

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['wfId'] = wfId
			context['wfDict'] = wfDict
			context['titleId'] = titleId
			context['viewMode'] = viewMode
			context['editMode'] = editMode
			context['componentTypeList'] = self.getComponentTypeList(_includeWorkflow=False)
			context['classNameList'] = self.getClassNameList()
			if self.canRaw:
				context['canWriteSingleFileToDisk'] = True
				context['car_relative_path'] = self.getDefaultRelativePath(wfDict)

			self.render('adminWorkflowCreateComponent.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def getDefaultRelativePath(self, _wfDict):
		return '/sites/%s/components/%s/' % (self.getProfile().get('siteProfile', {}).get('site', ''), _wfDict.get('code', ''))


	#   POST creates new workflow components.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()
		if not self.canCreateComponent:
			raise excUtils.MPSValidationException("Operation not permitted")

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)
			formData = tornado.escape.json_decode(self.request.body)

			#   Check for errors, Narc'em.
			jErrors = []
			componentDict = self.validateFormData(connection, wfDict, formData, jErrors)
			if jErrors:
				raise excUtils.MPSValidationException(jErrors)

			#   Persist.
			workflowComponentSvc.WorkflowComponentService(connection).createComponent(componentDict)

			responseDict = self.getPostResponseDict("Component created")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + "/wf/%s/%s/%s/%s" % (str(wfId), str(titleId), editMode, viewMode)
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _wfDict, _formData, jErrors):
		#   Check required fields.
		requiredFields = ['code','descr','componentType','className']
		for fieldCode in requiredFields:
			fieldValue = str(_formData.get(fieldCode, '')).strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		componentTypeStr = str(_formData.get('componentType', '')).strip()
		componentTypeDict = self.validateComponentType(_connection, componentTypeStr, 'componentType')

		#   Build a component.
		#   Build a component data dictionary.

		componentDataDict = {}
		componentDataDict['code'] = str(_formData.get('code', '')).strip()
		componentDataDict['descr'] = str(_formData.get('descr', '')).strip()
		componentDataDict['componentType'] = componentTypeDict.get('descr', '')
		componentDataDict['className'] = str(_formData.get('className', '')).strip()
		componentDataDict['affordanceType'] = ''
		componentDataDict['optional'] = False
		componentDataDict['enabled'] = False
		componentDataDict['accessPermissions'] = []
		componentDataDict['viewPermissions'] = []
		componentDataDict['blockers'] = []
		componentDataDict['statusMsg'] = ''
		componentDataDict['comment'] = ''
		componentDataDict['logEnabled'] = True

		if self.isTask(componentTypeDict):
			componentDataDict['freezable'] = False
			componentDataDict['overviewOnly'] = False
			componentDataDict['isProtectedCandidateItem'] = False
			componentDataDict['successMsg'] = ''

		if self.isContainer(componentTypeDict):
			componentDataDict['containers'] = []

		componentDict = {}
		componentDict['code'] = componentDataDict['code']
		componentDict['descr'] = componentDataDict['descr']
		componentDict['component_type_id'] = componentTypeDict.get('id', 0)
		componentDict['is_site_override'] = True
		componentDict['value'] = json.dumps(componentDataDict)
		componentDict['src'] = "%s = %s" % (componentDataDict['code'], pprint.pformat(componentDataDict))

		defaultRelativePath = self.getDefaultRelativePath(_wfDict)
		relativePath = str(_formData.get('car_relative_path', '')).strip()
		if relativePath == defaultRelativePath:
			relativePath = '%s%s.py' % (defaultRelativePath, componentDataDict['code'])
		componentDict['car_relative_path'] = relativePath

		return componentDict


#   Create Workflow Title Override

class WorkflowComponentCreateOverrideHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	#   Get handles component override create requests.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()
		if not self.canCreateTitleOverride:
			raise excUtils.MPSValidationException("Operation not permitted")

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(_isRequired=True, **kwargs)
		containerCode = self.getContainerCode(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)
			titleDict = self.getTitle(connection, titleId)
			containerDict = self.getContainer(wfService, containerCode)

			override = wfService.getTitleOverrideForWorkflowComponentTitle(wfDict.get('code', ''), titleDict.get('code', ''), containerCode)
			if override:
				raise excUtils.MPSValidationException("Title already has an override")

			#   Create the title override.

			overrideDict = {}
			overrideDict['workflow_code'] = wfDict.get('code', '')
			overrideDict['component_code'] = containerDict.get('code', '')
			overrideDict['title_code'] = titleDict.get('code', '')

			valueDict = {}
			valueDict['workflowCode'] = overrideDict['workflow_code']
			valueDict['componentCode'] = overrideDict['component_code']
			valueDict['titleCode'] = overrideDict['title_code']
			overrideDict['value'] = json.dumps(valueDict)

			workflowComponentSvc.WorkflowComponentService(connection).createComponentOverride(overrideDict)
			self.redirect("/appt/wf/edit/%s/%s/%s/%s/%s" % (str(wfId), str(titleId), containerCode, editMode, viewMode))

		finally:
			self.closeConnection()


#   Delete Workflow Component

class WorkflowComponentDeleteHandler(AbstractAdminWorkflowHandler):
	logger = logging.getLogger(__name__)

	#   POST handles component delete requests.

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptWFEdit','apptWFEditRaw'])
		self.initPermissions()

		wfId = self.getWfId(**kwargs)
		titleId = self.getTitleId(**kwargs)
		containerCode = self.getContainerCode(**kwargs)
		editMode = self.getEditMode(**kwargs)
		viewMode = self.getViewMode(**kwargs)

		connection = self.getConnection()
		try:
			wfService = workflowSvc.WorkflowService(connection)
			wfDict = self.getWorkflow(wfService, wfId)
			containerDict = self.getContainer(wfService, containerCode)

			titleDict = {}
			isTitleOverride = True if (titleId) and (titleId != '0') else False
			if isTitleOverride:
				titleDict = self.getTitle(connection, titleId)

			#   Delete the component.

			if isTitleOverride:
				titleCode = titleDict.get('code', '')
				overrideDict = wfService.getTitleOverrideForWorkflowComponentTitle(wfDict.get('code', ''), titleCode, containerCode)
				if not overrideDict:
					raise excUtils.MPSValidationException("Title Override not found")
				if not self.canDeleteTitleOverride:
					raise excUtils.MPSValidationException("Operation not permitted")
				workflowComponentSvc.WorkflowComponentService(connection).deleteComponentOverride(overrideDict.get('id', 0))
				responseDict = self.getPostResponseDict("Component Override deleted")
				responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + "/wf/edit/%s/%s/%s/%s/%s" % (str(wfId), str(titleId), containerCode, editMode, viewMode)
			else:
				if not self.canDeleteComponent:
					raise excUtils.MPSValidationException("Operation not permitted")
				workflowComponentSvc.WorkflowComponentService(connection).deleteComponent(containerDict.get('id', 0))
				responseDict = self.getPostResponseDict("Component deleted")
				responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + "/wf/%s/%s/%s/%s" % (str(wfId), str(titleId), editMode, viewMode)

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/wf', WorkflowHandler),
	(r'/appt/wf/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowHandler),
	(r'/appt/wf/edit/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<containerCode>[^/]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowComponentEditHandler),
	(r'/appt/wf/save/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<containerCode>[^/]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowComponentSaveHandler),
	(r'/appt/wf/write/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<containerCode>[^/]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowComponentWriteHandler),
	(r'/appt/wf/createworkflow/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowCreateHandler),
	(r'/appt/wf/createcomponent/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowComponentCreateHandler),
	(r'/appt/wf/createoverride/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<containerCode>[^/]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowComponentCreateOverrideHandler),
	(r'/appt/wf/deletecomponent/(?P<wfId>[0-9]*)/(?P<titleId>[0-9]*)/(?P<containerCode>[^/]*)/(?P<editMode>[^/]*)/(?P<viewMode>[^/]*)', WorkflowComponentDeleteHandler),
]
