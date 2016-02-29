# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.core.sql.lookupTableSQL as lookupSQL
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractAdminTitleHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


#   Render Track List

class TitleHandler(AbstractAdminTitleHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		pass
		self.verifyRequest()
		self.verifyAnyPermission(['apptTitleEdit'])

		connection = self.getConnection()
		try:
			titleList = titleSvc.TitleService(connection).getAllTitles()
			count = len(titleList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['titleList'] = titleList
			context['count'] = count
			context['countDisplayString'] = "%i Titles" % count

			self.render('adminTitleList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Render Add/Edit screens

class AbstractAdminTitleAddeditHandler(AbstractAdminTitleHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptTitleEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		titleid = kwargs.get('titleid', '')
		if (isEdit) and (not titleid):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			title = {}
			if isEdit:
				title = titleSvc.TitleService(connection).getTitle(titleid)
			tracks = lookupSQL.getLookupTable(connection, 'wf_track', _orderBy='code')

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['title'] = title
			context['tracks'] = tracks

			self.render("adminTitleDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

class TitleAddHandler(AbstractAdminTitleAddeditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class TitleEditHandler(AbstractAdminTitleAddeditHandler):
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

class TitleSaveHandler(AbstractAdminTitleHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptTitleEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		titleId = formData.get('titleId', 0)
		if (isEdit) and (not titleId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			self.validateFormData(connection, formData)

			#   Build data structure for persistence.

			titleDict = {}
			titleDict['id'] = titleId
			titleDict['code'] = formData.get('code', '').strip()
			titleDict['descr'] = formData.get('descr', '').strip()
			titleDict['active'] = True if formData.get('active', '') == 'true' else False
			titleDict['isactionable'] = True if formData.get('isactionable', '') == 'true' else False
			titleDict['job_code'] = formData.get('job_code', '').strip()
			titleDict['track_id'] = formData.get('track_id', None)
			titleDict['position_criteria'] = formData.get('position_criteria', '').strip()
			titleDict['rank_order'] = formData.get('rank_order', 0)
			titleDict['tags'] = formData.get('tags', '').strip()
			titleSvc.TitleService(connection).saveTitle(titleDict, isEdit)

			responseDict = self.getPostResponseDict("Title saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/titles'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['code','descr','job_code']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Track, if specified, must be valid.
		trackId = _formData.get('track_id', 0)
		if trackId:
			trackDict = lookupSvc.getEntityByKey(_connection, 'wf_track', trackId, _key='id')
			if not trackDict:
				jErrors.append({ 'code': 'track_id', 'field_value': '', 'message': 'Invalid Track' })
			_formData['track_id'] = int(trackId)
		else:
			_formData['track_id'] = None

		#   Rank Order, if specified, must be an integer.
		rankOrder = _formData.get('rank_order', '')
		if rankOrder:
			try:
				_formData['rank_order'] = int(rankOrder)
			except Exception, e:
				jErrors.append({ 'code': 'rank_order', 'field_value': rankOrder, 'message': 'Invalid Rank Order' })
		else:
			_formData['rank_order'] = 0

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/titles', TitleHandler),
	(r'/appt/titles/add', TitleAddHandler),
	(r'/appt/titles/edit/(?P<titleid>[^/]*)', TitleEditHandler),
	(r'/appt/titles/save', TitleSaveHandler),
]
