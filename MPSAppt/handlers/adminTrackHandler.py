# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.trackService as trackSvc
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.core.sql.lookupTableSQL as lookupSQL
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractAdminTrackHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


#   Render Track List

class TrackHandler(AbstractAdminTrackHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		pass
		self.verifyRequest()
		self.verifyAnyPermission(['apptTrackEdit'])

		connection = self.getConnection()
		try:
			trackList = trackSvc.TrackService(connection).getAllTracks(_includeInactive=True, _joinMetatrack=True)
			count = len(trackList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['trackList'] = trackList
			context['count'] = count
			context['countDisplayString'] = "%i Tracks" % count

			self.render('adminTrackList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Render Add/Edit screens

class AbstractAdminTrackAddeditHandler(AbstractAdminTrackHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptTrackEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		trackid = kwargs.get('trackid', '')
		if (isEdit) and (not trackid):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			track = {}
			if isEdit:
				track = trackSvc.TrackService(connection).getTrackForTrackId(trackid, _includeInactive=True)
			metatracks = lookupSQL.getLookupTable(connection, 'wf_metatrack', _orderBy='code')

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['track'] = track
			context['metatracks'] = metatracks

			self.render("adminTrackDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

class TrackAddHandler(AbstractAdminTrackAddeditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class TrackEditHandler(AbstractAdminTrackAddeditHandler):
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

class TrackSaveHandler(AbstractAdminTrackHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptTrackEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		trackId = formData.get('trackId', 0)
		if (isEdit) and (not trackId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			self.validateFormData(connection, formData)

			#   Build data structure for persistence.

			trackDict = {}
			trackDict['id'] = trackId
			trackDict['code'] = formData.get('code', '').strip()
			trackDict['descr'] = formData.get('descr', '').strip()
			trackDict['active'] = True if formData.get('active', '') == 'true' else False
			trackDict['metatrack_id'] = formData.get('metatrack_id', None)
			trackDict['tags'] = formData.get('tags', '').strip()
			trackSvc.TrackService(connection).saveTrack(trackDict, isEdit)

			responseDict = self.getPostResponseDict("Track saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/tracks'
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

		#   Metatrack, if specified, must be valid.
		metatrackId = _formData.get('metatrack_id', 0)
		if metatrackId:
			metatrackDict = lookupSvc.getEntityByKey(_connection, 'wf_metatrack', metatrackId, _key='id')
			if not metatrackDict:
				jErrors.append({ 'code': 'metatrack_id', 'field_value': '', 'message': 'Invalid metatrack' })
			_formData['metatrack_id'] = int(metatrackId)
		else:
				_formData['metatrack_id'] = None

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/tracks', TrackHandler),
	(r'/appt/tracks/add', TrackAddHandler),
	(r'/appt/tracks/edit/(?P<trackid>[^/]*)', TrackEditHandler),
	(r'/appt/tracks/save', TrackSaveHandler),
]
