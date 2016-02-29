# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractUberAdminHandler as absHandler
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.exceptionUtils as excUtils


#   Render Uber Group List

class UberGroupHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		connection = self.getConnection()
		try:
			groupList = uberSvc.UberService(connection).getUberGroups()
			count = len(groupList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['groupList'] = groupList
			context['count'] = count
			context['countDisplayString'] = "%i Groups" % count

			self.render('adminUberGroupList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Render Add/Edit screens

class AbstractUberGroupAddEditHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		groupid = kwargs.get('groupid', '')
		if (isEdit) and (not groupid):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			group = {}
			if isEdit:
				group = lookupTableSvc.getEntityByKey(connection, 'wf_uber_group', groupid, _key='id')
				if not group:
					raise excUtils.MPSValidationException("Group not found")

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['group'] = group

			maxGroupChildren = self.getMaxGroupChildren()
			self.breakoutGroupChildren(group, maxGroupChildren)
			context['maxGroupChildren'] = maxGroupChildren

			self.render("adminUberGroupDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def breakoutGroupChildren(self, _group, _maxGroupChildren):
		children = _group.get('children', '').split(',')
		for i in range(1, 1 + _maxGroupChildren):
			if len(children) < i:
				children.append('')
		_group['childrenBreakout'] = children


class UberGroupAddHandler(AbstractUberGroupAddEditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class UberGroupEditHandler(AbstractUberGroupAddEditHandler):
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

class UberGroupSaveHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		groupId = formData.get('groupId', '')
		if (isEdit) and (not groupId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Find existing Group.
			group = {}
			if isEdit:
				group = lookupTableSvc.getEntityByKey(connection, 'wf_uber_group', groupId, _key='id')
				if not group:
					raise excUtils.MPSValidationException("Group not found")

			#   Validate form data.
			self.validateFormData(connection, group, formData, isEdit)

			#   Build data structures for persistence.

			groupDict = {}
			groupDict['id'] = groupId
			groupDict['code'] = formData.get('code', '').strip()
			groupDict['descr'] = formData.get('descr', '').strip()
			groupDict['display_text'] = formData.get('display_text', '').strip()
			groupDict['cols_offset'] = formData.get('cols_offset', 0)
			groupDict['cols_label'] = formData.get('cols_label', 0)
			groupDict['repeating'] = True if formData.get('repeating', '') == 'true' else False
			groupDict['repeating_table'] = True if formData.get('repeating_table', '') == 'true' else False
			groupDict['required'] = True if formData.get('required', '') == 'true' else False
			groupDict['wrap'] = True if formData.get('wrap', '') == 'true' else False
			groupDict['filler'] = True if formData.get('filler', '') == 'true' else False
			groupDict['children'] = self.resequenceChildren(formData)
			uberSvc.UberService(connection).saveGroup(groupDict, isEdit)

			responseDict = self.getPostResponseDict("Group saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/uber/groups'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _question, _formData, _isEdit):
		jErrors = []

		#   Check required fields.
		requiredFields = ['code','descr','repeating','repeating_table','required','wrap','filler']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Size and Placement fields must be integers if specified, otherwise fill in default values.
		intErrors = []
		self._validateInteger(_formData, 'cols_offset', 0, intErrors)
		self._validateInteger(_formData, 'cols_label', 12, intErrors)
		if intErrors:
			jErrors.extend(intErrors)
		else:
			total = _formData.get('cols_offset', 0) + _formData.get('cols_label', 0)
			if total > 12:
				jErrors.append({ 'code': 'cols_offset', 'field_value': '', 'message': 'Cannot specify more than 12 total columns' })

		#   Code must be unique across Question, Option, and Group.
		groupCode = _formData.get('code', '').strip()
		if groupCode:
			if groupCode != _formData.get('original_code', ''):
				self._duplicateCodeCheck(_connection, groupCode, 'code', jErrors)

		#   Narc if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def resequenceChildren(self, _formData):
		childList = []
		childSequence = _formData.get('child_sequence', [])
		for seqNbr in childSequence:
			key = 'child_%s' % seqNbr
			value = _formData.get(key, '')
			if value:
				childList.append(value)
		return ','.join(childList)


#   Try It!

class UberGroupTryItHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		groupid = kwargs.get('groupid', '')
		if not groupid:
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			group = lookupTableSvc.getEntityByKey(connection, 'wf_uber_group', groupid, _key='id')
			if not group:
				raise excUtils.MPSValidationException("Group not found")

			container = self._createContainer(connection, group.get('code',''))
			container.loadInstanceByForce()

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['group'] = group
			context.update(container.getEditContext(self.getSitePreferences()))
			context['disabled'] = False
			context['optional'] = True
			context['blocked'] = False
			context['complete'] = False
			self.render('adminUberTryIt.html', context=context, skin=context['skin'])

		finally:
			if connection:
				try: connection.performRollback()
				except Exception, e1: pass
			self.closeConnection()

	def _createContainer(self, _connection, _groupCode):
		parameterBlock = {}
		parameterBlock['userProfile'] = self.getProfile()
		parameterBlock['userPermissions'] = self.getUserProfile().get('userPermissions', [])
		parameterBlock['titleCode'] = ''
		parameterBlock['containerDict'] = self._createContainerDict(_groupCode)

		import MPSAppt.core.workflow as wf
		parameterBlock['workflow'] = wf.Workflow(_connection, {}, {})

		className = 'UberForm'
		importString = "from MPSAppt.core.containers.%s import %s" % (className.lower(), className)
		exec importString

		container = eval(className + "('%s', parameterBlock)" % _groupCode)
		return container

	def _createContainerDict(self, _groupCode):
		tryit = {
			"code": "tryit",
			"descr": "Preview",
			"componentType": "Task",
			"affordanceType":"Item",
			"optional": False,
			"enabled": True,
			"logEnabled": False,
			"freezable": False,
			"className": "UberForm",
			"config": {
				"questionGroupCode": _groupCode,
				"submitEnabled": False,
				"draftEnabled": False,
				"savedSetsEnabled": False,
			},
		}
		return tryit




#   All URL mappings for this module.

urlMappings = [
	(r'/appt/uber/groups', UberGroupHandler),
	(r'/appt/uber/groups/add', UberGroupAddHandler),
	(r'/appt/uber/groups/edit/(?P<groupid>[^/]*)', UberGroupEditHandler),
	(r'/appt/uber/groups/save', UberGroupSaveHandler),
	(r'/appt/uber/groups/tryit/(?P<groupid>[^/]*)', UberGroupTryItHandler),
]
