# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import json
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.departmentResolverService as deptResolverSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractAdminDeptHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def breakoutAddressLines(self, _department, _maxAddressLines):
		addressLinesJson = _department.get('address_lines','[]')
		addressLines = json.loads(addressLinesJson)
		for i in range(1, 1 + _maxAddressLines):
			if len(addressLines) < i:
				addressLines.append('')
		_department['address_lines_breakout'] = addressLines

	def breakoutSuffixLines(self, _department, _maxSuffixLines):
		addressSuffixJson = _department.get('address_suffix','[]')
		addressSuffix = json.loads(addressSuffixJson)
		for i in range(1, 1 + _maxSuffixLines):
			if len(addressSuffix) < i:
				addressSuffix.append('')
		_department['address_suffix_breakout'] = addressSuffix

	def breakoutDepartmentChairs(self, _department, _maxChairs):
		chairs = _department.get('department_chair', [])
		for i in range(1, 1 + _maxChairs):
			if len(chairs) < i:
				chairs.append({})
		_department['department_chair_breakout'] = chairs

	def breakoutDepartmentChairTitles(self, _department, _maxChairTitles):
		chairs = _department.get('department_chair_breakout', [])
		for each in chairs:
			titles = each.get('chair_titles_list', [])
			for i in range(1, 1 + _maxChairTitles):
				if len(titles) < i:
					titles.append('')
			each['chair_titles_breakout'] = titles
		_department['department_chair_breakout'] = chairs


#   Render Department List

class DepartmentHandler(AbstractAdminDeptHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		pass
		self.verifyRequest()
		self.verifyAnyPermission(['apptDeptEdit'])

		connection = self.getConnection()
		try:
			departmentHierarchy = deptSvc.DepartmentService(connection).getDepartmentHierarchy(None, _includeChairs=True)
			departmentList = self.flattenDepartmentHierarchy(departmentHierarchy)
			count = len(departmentList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['departmentList'] = departmentList
			context['count'] = count
			context['countDisplayString'] = "%i Departments" % count

			self.render('adminDeptList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def flattenDepartmentHierarchy(self, _hierarchy):
		flatList = []
		for departmentDict in _hierarchy:
			children = departmentDict.get('children',[])
			if children:
				for childDict in children:
					childDict['parent'] = departmentDict
					flatList.append(childDict)
			else:
				flatList.append(departmentDict)
		return flatList


#   Render Add/Edit screens

class AbstractAdminDeptAddeditHandler(AbstractAdminDeptHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptDeptEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		deptid = kwargs.get('deptid', '')
		if (isEdit) and (not deptid):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			department = {}
			if isEdit:
				departmentDict = lookupTableSvc.getEntityByKey(connection, 'wf_department', deptid, _key='id')
				if not departmentDict:
					raise excUtils.MPSValidationException("Department not found")

				resolver = deptResolverSvc.DepartmentResolverService(connection, self.getSitePreferences())
				department = resolver.resolve(departmentDict.get('id', 0))
				if not department:
					raise excUtils.MPSValidationException("Department not found")

			departmentHierarchy = deptSvc.DepartmentService(connection).getDepartmentHierarchy(None, _includeChairs=False)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['department'] = department
			context['parentalUnits'] = departmentHierarchy
			context['userEditEnabled'] = self.hasPermission('apptUserEdit')

			context['maxAddressLines'] = self.getSitePreferenceAsInt('apptmaxaddresslines', 5)
			context['maxAddressSuffixLines'] = self.getSitePreferenceAsInt('apptmaxaddresssuffixlines', 3)
			context['maxChairs'] = self.getSitePreferenceAsInt('apptmaxchairs', 2)
			context['maxChairTitles'] = self.getSitePreferenceAsInt('apptmaxchairtitles', 5)

			self.breakoutAddressLines(department, context['maxAddressLines'])
			self.breakoutSuffixLines(department, context['maxAddressSuffixLines'])
			self.breakoutDepartmentChairs(department, context['maxChairs'])
			self.breakoutDepartmentChairTitles(department, context['maxChairTitles'])

			self.render("adminDeptDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

class DepartmentAddHandler(AbstractAdminDeptAddeditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class DepartmentEditHandler(AbstractAdminDeptAddeditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'edit'
		self._getImpl(**kwargs)


#   Add/Edit save

class DepartmentSaveHandler(AbstractAdminDeptHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptDeptEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		deptId = formData.get('deptId', 0)
		if (isEdit) and (not deptId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			self.validateFormData(connection, formData)

			#   Build data structure for persistence.

			deptDict = {}
			deptDict['id'] = deptId
			deptDict['code'] = formData.get('code', '').strip()
			deptDict['descr'] = formData.get('descr', '').strip()
			deptDict['active'] = True if formData.get('active', '') == 'true' else False
			deptDict['parent_id'] = formData.get('parent_id', None)
			deptDict['pcn'] = formData.get('pcn', '').strip()
			deptDict['cc_acct_cd'] = formData.get('cc_acct_cd', '').strip()
			deptDict['email_address'] = formData.get('email_address', '').strip()
			deptDict['header_image'] = formData.get('header_image', '').strip()
			deptDict['address_lines'] = self.assembleAddressLines(formData)
			deptDict['city'] = formData.get('city', '').strip()
			deptDict['state'] = formData.get('state', '').strip()
			deptDict['postal'] = formData.get('postal', '').strip()
			deptDict['address_suffix'] = self.assembleSuffixLines(formData)
			deptDict['chairs'] = self.assembleChairs(formData)
			deptSvc.DepartmentService(connection).saveDepartment(deptDict, isEdit)

			responseDict = self.getPostResponseDict("Department saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/depts'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['code','descr','pcn']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Parent, if specified, must be valid.
		parentId = _formData.get('parent_id', 0)
		deptService = deptSvc.DepartmentService(_connection)
		if parentId:
			parentDict = deptService.getDepartment(parentId)
			if not parentDict:
				jErrors.append({ 'code': 'parent_id', 'field_value': '', 'message': 'Invalid parent department' })
			_formData['parent_id'] = int(parentId)
		else:
			rootDepartmentDict = deptService.getRootDepartment()
			if rootDepartmentDict:
				_formData['parent_id'] = rootDepartmentDict.get('id', 0)
			else:
				_formData['parent_id'] = None

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def assembleChairs(self, _formData):
		chairList = []
		maxChairs = self.getSitePreferenceAsInt('apptmaxchairs', 2)

		for idx in range(1, 1 + maxChairs):
			chairWithDegree = _formData.get('degree_' + str(idx), '').strip()
			chairSignature = _formData.get('signature_' + str(idx), '').strip()
			chairTitles = self.assembleLines(_formData, 'apptmaxchairtitles', 5, 'title_%s_' % str(idx), _pipeDelimited=True)
			if (chairWithDegree) or (chairSignature) or (chairTitles):
				chairDict = {}
				chairDict['chair_with_degree'] = chairWithDegree
				chairDict['chair_signature'] = chairSignature
				chairDict['chair_titles'] = chairTitles
				chairDict['seq'] = idx
				chairList.append(chairDict)
		return chairList

	def assembleAddressLines(self, _formData):
		return self.assembleLines(_formData, 'apptmaxaddresslines', 5, 'address_line_')

	def assembleSuffixLines(self, _formData):
		return self.assembleLines(_formData, 'maxAddressSuffixLines', 3, 'address_suffix_')

	def assembleLines(self, _formData, _maxKeyName, _maxDefaultValue, _keyPrefix, _pipeDelimited=False):
		lines = []
		maxLines = self.getSitePreferenceAsInt(_maxKeyName, _maxDefaultValue)
		for idx in range(1, 1 + maxLines):
			keyName = _keyPrefix + str(idx)
			thisLine = _formData.get(keyName, '').strip()
			if thisLine:
				lines.append(thisLine)
		if _pipeDelimited:
			return '|'.join(lines)
		return json.dumps(lines)


#   All URL mappings for this module.
urlMappings = [
	(r'/appt/depts', DepartmentHandler),
	(r'/appt/depts/add', DepartmentAddHandler),
	(r'/appt/depts/edit/(?P<deptid>[^/]*)', DepartmentEditHandler),
	(r'/appt/depts/save', DepartmentSaveHandler),
]
