# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.exceptionUtils as excUtils

kSpecialLookupKeyCache = {
	'CRED_DEPTS': ('Credentialing Departments', 'Credentialing Department'),
	'DEGREES': ('Degrees','Degree'),
	'DEPARTMENT': ('Departments', 'Department'),
	'ETHNICITIES': ('Ethnicities', 'Ethnicity'),
	'FPSC': ('FPSC', 'FPSC'),
	'GRANT_ROLES': ('Grant Roles', 'Grant Role'),
	'GRANT_STATUSES': ('Grant Statuses', 'Grant Status'),
	'LANGUAGES': ('Languages', 'Language'),
	'LICENSES': ('Licenses', 'License'),
	'PATENTS_ROLE': ('Patent Roles', 'Patent Role'),
	'PUBLICATIONSTATUS': ('Publication Statuses', 'Publication Status'),
	'ROLEINCOMMITTEE': ('Role in Committee', 'Role in Committee'),
	'SEMINARTYPES': ('Seminar Types', 'Seminar Type'),
	'TEACHINGROLE': ('Teaching Roles', 'Teaching Role'),
	'WORK_EXPERIENCES': ('Work Experiences', 'Work Experience'),
	'YESNO': ('Yes/No', 'Yes/No'),
}

class AbstractAdminLookupHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _mungeKey(self, _key):
		if _key in kSpecialLookupKeyCache:
			dataTuple = kSpecialLookupKeyCache[_key]
			return dataTuple[0], dataTuple[1]

		entityName = _key.capitalize()
		entityNameSingular = entityName
		if entityNameSingular.endswith('ies'):
			entityNameSingular = entityNameSingular[0:(len(entityNameSingular) - 3)] + 'y'
		elif entityNameSingular.endswith('es'):
			entityNameSingular = entityNameSingular[0:(len(entityNameSingular) - 1)]
		elif entityNameSingular.endswith('s'):
			entityNameSingular = entityNameSingular[0:(len(entityNameSingular) - 1)]
		return entityName, entityNameSingular


#   Render Lookup List

class LookupHandler(AbstractAdminLookupHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptLookupEdit'])

		connection = self.getConnection()
		try:
			staticCache = lookupTableSvc.getStaticCodeDescrCache(connection)
			keyList = self._getKeyList( staticCache)
			key = kwargs.get('key', '')
			if not key:
				if not keyList:
					key = ''
				else:
					key = keyList[0]['code']

			entityName, entityNameSingular = self._mungeKey(key)
			itemList = staticCache.get(key, [])
			count = len(itemList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['entityName'] = entityName
			context['entityNameSingular'] = entityNameSingular
			context['key'] = key
			context['keyList'] = keyList
			context['itemList'] = itemList
			context['count'] = count
			context['countDisplayString'] = "%i %s" % (count, entityName)

			self.render('adminLookupList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def _getKeyList(self, _staticCache):
		keys = _staticCache.keys()
		keys.sort()

		keyList = []
		for key in keys:
			entityName, entityNameSingular = self._mungeKey(key)
			url = "/appt/lookups/%s" % key
			keyList.append({ 'code': key, 'descr': entityName, 'url': url })
		return keyList


#   Render Add/Edit screens

class AbstractAdminLookupAddEditHandler(AbstractAdminLookupHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptLookupEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		key = kwargs.get('key', '')
		itemId = kwargs.get('itemid', '')
		if not key:
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return
		if (isEdit) and (not itemId):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			entityName, entityNameSingular = self._mungeKey(key)

			itemDict = {}
			if isEdit:
				itemDict = self._findItem(connection, key, itemId)
				if not itemDict:
					raise excUtils.MPSValidationException("Record not found")

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['key'] = key
			context['itemId'] = itemId
			context['entityName'] = entityName
			context['entityNameSingular'] = entityNameSingular
			context['itemDetailDict'] = itemDict

			self.render("adminLookupDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def _findItem(self, _connection, _key, _itemId):
		staticCache = lookupTableSvc.getStaticCodeDescrCache(_connection)
		itemList = staticCache.get(_key, [])
		for itemDict in itemList:
			if str(itemDict.get('id', -1)) == _itemId:
				return itemDict
		return None

class LookupAddHandler(AbstractAdminLookupAddEditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class LookupEditHandler(AbstractAdminLookupAddEditHandler):
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

class LookupSaveHandler(AbstractAdminLookupHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptDeptEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		key = kwargs.get('key', '')
		itemId = formData.get('itemId', '')
		if not key:
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return
		if (isEdit) and (not itemId):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			staticCache = lookupTableSvc.getStaticCodeDescrCache(connection)
			self.validateFormData(key, staticCache, formData, isEdit)

			#   Build data structure for persistence.

			itemDict = {}
			itemDict['id'] = itemId
			itemDict['lookup_key'] = key
			itemDict['code'] = formData.get('code', '').strip()
			itemDict['descr'] = formData.get('descr', '').strip()
			itemDict['alt_descr'] = formData.get('alt_descr', '').strip()
			itemDict['seq'] = formData.get('seq', '')
			lookupTableSvc.saveStaticItem(connection, itemDict, not isEdit)

			entityName, entityNameSingular = self._mungeKey(key)
			responseDict = self.getPostResponseDict("%s saved" % entityNameSingular)
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/lookups/' + key
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _key, _staticCache, _formData, _isEdit):
		jErrors = []

		#   Check required fields.
		requiredFields = ['code','descr','seq']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Code must not be a duplicate.
		if not _isEdit:
			code = _formData.get('code', '').strip()
			if code:
				itemList = _staticCache.get(_key, [])
				for itemDict in itemList:
					if itemDict.get('code', '') == code:
						jErrors.append({ 'code': 'code', 'field_value': '', 'message': 'Code already in use' })
						break

		#   Sequence must be an integer.
		try:
			seq = _formData.get('seq', '').strip()
			if seq:
				_formData['seq'] = int(seq)
		except Exception, e:
			jErrors.append({ 'code': 'seq', 'field_value': '', 'message': 'Integer value required' })

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


#   Resequence

class LookupResequenceHandler(AbstractAdminLookupHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptDeptEdit'])

		key = kwargs.get('key', '')
		if not key:
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			staticCache = lookupTableSvc.getStaticCodeDescrCache(connection)
			itemList = staticCache.get(key, [])

			try:
				seq = 1
				for itemDict in itemList:
					itemDict['seq'] = seq
					lookupTableSvc.updateStaticItemSequence(connection, itemDict, doCommit=False)
					seq += 1
				connection.performCommit()
			except Exception, e:
				connection.performRollback()
				raise e

			self.redirect('/' + self.getEnvironment().getAppUriPrefix() + '/lookups/' + key)

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/lookups', LookupHandler),
	(r'/appt/lookups/(?P<key>[^/]*)', LookupHandler),
	(r'/appt/lookups/(?P<key>[^/]*)/add', LookupAddHandler),
	(r'/appt/lookups/(?P<key>[^/]*)/edit/(?P<itemid>[^/]*)', LookupEditHandler),
	(r'/appt/lookups/(?P<key>[^/]*)/save', LookupSaveHandler),
	(r'/appt/lookups/(?P<key>[^/]*)/resequence', LookupResequenceHandler),
]
