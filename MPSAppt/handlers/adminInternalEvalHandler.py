# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import json
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.internalEvalService as internalEvalSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractAdminInternalEvalHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


#   Render Building List

class InternalEvalHandler(AbstractAdminInternalEvalHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyAnyPermission(['apptInternalEvalEdit'])

		connection = self.getConnection()
		try:
			evalList = internalEvalSvc.InternalEvalService(connection).getAllEvaluators(_includeInactive=True)
			count = len(evalList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['evaluatorList'] = evalList
			context['count'] = count
			context['countDisplayString'] = "%i Reviewers" % count

			self.render('adminInternalEvalList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Render Add/Edit screens

class AbstractAdminInternalEvalAddeditHandler(AbstractAdminInternalEvalHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptInternalEvalEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		evaluatorId = kwargs.get('evaluatorid', '')
		if (isEdit) and (not evaluatorId):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			evaluator = {}
			if isEdit:
				evaluator = internalEvalSvc.InternalEvalService(connection).getEvaluator(evaluatorId)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['evaluator'] = evaluator

			self.render("adminInternalEvalDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


class InternalEvalAddHandler(AbstractAdminInternalEvalAddeditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class InternalEvalEditHandler(AbstractAdminInternalEvalAddeditHandler):
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

class InternalEvalSaveHandler(AbstractAdminInternalEvalHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptInternalEvalEdit'])

		#   Validate form data.

		formData = tornado.escape.json_decode(self.request.body)
		mode = formData.get('mode', 'add')
		isEdit = (mode == 'edit')
		evaluatorId = formData.get('evaluatorId', 0)
		if (isEdit) and (not evaluatorId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			self.validateFormData(connection, formData)

			#   Build data structure for persistence.

			evaluatorDict = {}
			evaluatorDict['id'] = evaluatorId
			evaluatorDict['first_name'] = formData.get('first_name', '').strip()
			evaluatorDict['last_name'] = formData.get('last_name', '').strip()
			evaluatorDict['email_address'] = formData.get('email_address', '').strip()
			evaluatorDict['active'] = True if formData.get('active', '') == 'true' else False
			internalEvalSvc.InternalEvalService(connection).saveInternalEvaluator(evaluatorDict, isEdit)
			responseDict = self.getPostResponseDict("Evaluator saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/internalEvals'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['first_name','last_name','email_address']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Narc'em if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/internalEvals',InternalEvalHandler),
	(r'/appt/internalEvals/add', InternalEvalAddHandler),
	(r'/appt/internalEvals/edit/(?P<evaluatorid>[^/]*)', InternalEvalEditHandler),
	(r'/appt/internalEvals/save', InternalEvalSaveHandler),
]
