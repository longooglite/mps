# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import json
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.buildingService as buildingSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractAdminBuildingHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


#   Render Building List

class BuildingHandler(AbstractAdminBuildingHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyAnyPermission(['apptBuildingEdit'])

		connection = self.getConnection()
		try:
			buildingList = buildingSvc.BuildingService(connection).getAllBuildings(_includeInactive=True)
			count = len(buildingList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['buildingList'] = buildingList
			context['count'] = count
			context['countDisplayString'] = "%i Buildings" % count

			self.render('adminBuildingList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Render Add/Edit screens

class AbstractAdminBuildingAddeditHandler(AbstractAdminBuildingHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptBuildingEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		buildingid = kwargs.get('buildingid', '')
		if (isEdit) and (not buildingid):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			building = {}
			if isEdit:
				building = buildingSvc.BuildingService(connection).getBuilding(buildingid)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['building'] = building

			staticCache = lookupTableSvc.getStaticCodeDescrCache(connection)
			context['states'] = staticCache.get('STATES', [])
			context['countries'] = staticCache.get('COUNTRIES', [])

			context['maxAddressLines'] = self.getSitePreferenceAsInt('apptmaxbuildingaddresslines', 5)
			self.breakoutAddressLines(building, context['maxAddressLines'])
			self.render("adminBuildingDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def breakoutAddressLines(self, _building, _maxAddressLines):
		addressLinesJson = _building.get('address_lines','[]')
		addressLines = json.loads(addressLinesJson)
		for i in range(1, 1 + _maxAddressLines):
			if len(addressLines) < i:
				addressLines.append('')
		_building['address_lines_breakout'] = addressLines

class BuildingAddHandler(AbstractAdminBuildingAddeditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class BuildingEditHandler(AbstractAdminBuildingAddeditHandler):
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

class BuildingSaveHandler(AbstractAdminBuildingHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptBuildingEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		buildingId = formData.get('buildingId', 0)
		if (isEdit) and (not buildingId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			self.validateFormData(connection, formData)

			#   Build data structure for persistence.

			buildingDict = {}
			buildingDict['id'] = buildingId
			buildingDict['code'] = formData.get('code', '').strip()
			buildingDict['descr'] = formData.get('descr', '').strip()
			buildingDict['active'] = True if formData.get('active', '') == 'true' else False
			buildingDict['address_lines'] = self.assembleAddressLines(formData)
			buildingDict['city'] = formData.get('city', '').strip()
			buildingDict['state'] = formData.get('state', '').strip()
			buildingDict['country'] = formData.get('country', '').strip()
			buildingDict['postal'] = formData.get('postal', '').strip()
			buildingSvc.BuildingService(connection).saveBuilding(buildingDict, isEdit)

			responseDict = self.getPostResponseDict("Building saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/buildings'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['code','descr']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

	def assembleAddressLines(self, _formData):
		return self.assembleLines(_formData, 'apptmaxbuildingaddresslines', 5, 'address_line_')

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
	(r'/appt/buildings', BuildingHandler),
	(r'/appt/buildings/add', BuildingAddHandler),
	(r'/appt/buildings/edit/(?P<buildingid>[^/]*)', BuildingEditHandler),
	(r'/appt/buildings/save', BuildingSaveHandler),
]
