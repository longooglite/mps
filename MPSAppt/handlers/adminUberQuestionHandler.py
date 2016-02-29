# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import os
import tornado.escape

import MPSAppt.handlers.abstractUberAdminHandler as absHandler
import MPSAppt.services.uberService as uberSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSCore.utilities.exceptionUtils as excUtils


#   Render Uber Question List

class UberQuestionHandler(absHandler.AbstractUberAdminHandler):
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
			questionList = uberSvc.UberService(connection).getUberQuestions()
			count = len(questionList)

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['questionList'] = questionList
			context['count'] = count
			context['countDisplayString'] = "%i Questions" % count

			self.render('adminUberQuestionList.html', context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   Render Add/Edit screens

class AbstractUberQuestionAddEditHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def _getImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		mode = kwargs.get('mode', 'add')
		isEdit = (mode == 'edit')
		questionid = kwargs.get('questionid', '')
		if (isEdit) and (not questionid):
			self.redirect('/' + self.getEnvironment().getAppUriPrefix())
			return

		connection = self.getConnection()
		try:
			question = {}
			if isEdit:
				question = lookupTableSvc.getEntityByKey(connection, 'wf_uber_question', questionid, _key='id')
				if not question:
					raise excUtils.MPSValidationException("Question not found")

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['mode'] = mode
			context['question'] = question
			context['dataTypes'] = self.getQuestionDataTypes()
			context['jobActionTypes'] = self.getJobActionTypes(connection)

			maxJobActionTypes = self.getMaxJobActionTypes()
			self.breakoutJobActionTypes(question, maxJobActionTypes)
			context['maxJobActionTypes'] = maxJobActionTypes

			maxOptions = self.getMaxOptions()
			self.breakoutOptions(connection, question, maxOptions)
			context['maxOptions'] = maxOptions

			self.render("adminUberQuestionDetail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def breakoutJobActionTypes(self, _question, _maxJobActionTypes):
		jaTypesStr = _question.get('job_action_types', '')
		jaTypes = jaTypesStr.split(',')
		for i in range(1, 1 + _maxJobActionTypes):
			if len(jaTypes) < i:
				jaTypes.append('')
		_question['jobActionTypeBreakout'] = jaTypes

	def breakoutOptions(self, _connection, _question, _maxOptions):
		questionId = _question.get('id', 0)
		optionList = uberSvc.UberService(_connection).getUberOptionsForQuestion(_question)
		for i in range(1, 1 + _maxOptions):
			if len(optionList) < i:
				optionList.append({})
		_question['optionList'] = optionList


class UberQuestionAddHandler(AbstractUberQuestionAddEditHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['mode'] = 'add'
		self._getImpl(**kwargs)

class UberQuestionEditHandler(AbstractUberQuestionAddEditHandler):
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

class UberQuestionSaveHandler(absHandler.AbstractUberAdminHandler):
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
		questionId = formData.get('questionId', '')
		if (isEdit) and (not questionId):
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Find existing Question.
			question = {}
			if isEdit:
				question = lookupTableSvc.getEntityByKey(connection, 'wf_uber_question', questionId, _key='id')
				if not question:
					raise excUtils.MPSValidationException("Question not found")

			#   Validate form data.
			optionData = self.organizeOptionData(formData)
			originalCodeList = self.getOriginalCodeList(formData, optionData)
			self.removeEmptyOptionGroups(optionData)
			self.validateFormData(connection, question, formData, optionData, originalCodeList, isEdit)

			#   Build data structures for persistence.

			questionDict = {}
			questionDict['id'] = questionId
			questionDict['code'] = formData.get('code', '').strip()
			questionDict['descr'] = formData.get('descr', '').strip()
			questionDict['display_text'] = formData.get('display_text', '').strip()
			questionDict['header_text'] = formData.get('header_text', '').strip()
			questionDict['cols_offset'] = formData.get('cols_offset', 0)
			questionDict['cols_label'] = formData.get('cols_label', 0)
			questionDict['cols_prompt'] = formData.get('cols_prompt', 0)
			questionDict['required'] = True if formData.get('required', '') == 'true' else False
			questionDict['wrap'] = True if formData.get('wrap', '') == 'true' else False
			questionDict['encrypt'] = True if formData.get('encrypt', '') == 'true' else False
			questionDict['data_type'] = formData.get('data_type', '').strip()
			questionDict['data_type_attributes'] = formData.get('data_type_attributes', '').strip()
			questionDict['job_action_types'] = formData.get('job_action_types', '').strip()
			questionDict['identifier_code'] = formData.get('identifier_code', '').strip()
			questionDict['show_codes'] = formData.get('show_codes', '').strip()
			questionDict['hide_codes'] = formData.get('hide_codes', '').strip()
			optionList = self.resequenceOptionData(formData, optionData)
			uberSvc.UberService(connection).saveQuestionAndOptions(questionDict, optionList, isEdit)

			responseDict = self.getPostResponseDict("Question saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/uber/questions'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def organizeOptionData(self, _formData):

		#   Returns a multi-level dictionary structure of Option data elements from submitted form data.
		#   At the top-level, the dictionary is keyed by a sequence number. For each sequence number,
		#   the 'value' is another dictionary, structured as follows:
		#
		#       key = sequence nbr (int)
		#       value = data field codes and values (another dictionary)
		#
		#   This structure will be used to drive validation and data persistence for options.

		maxOptions = self.getMaxOptions()
		optionData = {}

		for idx in range(1, maxOptions + 1):
			optionDict = {}
			optionDict['id'] = _formData.get('option_id_%i' % idx, '').strip()
			optionDict['code'] = _formData.get('option_code_%i' % idx, '').strip()
			optionDict['descr'] = _formData.get('option_descr_%i' % idx, '').strip()
			optionDict['display_text'] = _formData.get('option_display_text_%i' % idx, '').strip()
			optionDict['seq'] = idx
			optionDict['show_codes'] = _formData.get('option_show_codes_%i' % idx, '').strip()
			optionDict['hide_codes'] = _formData.get('option_hide_codes_%i' % idx, '').strip()
			optionDict['original_code'] = _formData.get('original_option_code_%i' % idx, '').strip()
			optionData[str(idx)] = optionDict

		return optionData

	def getOriginalCodeList(self, _formData, _optionData):
		originalCodeList = []
		questionCode = _formData.get('original_code', '').strip()
		if questionCode:
			originalCodeList.append(questionCode)

		for optionDict in _optionData.values():
			optionCode = optionDict.get('original_code', '')
			if (optionCode) and (optionCode not in originalCodeList):
				originalCodeList.append(optionCode)

		return originalCodeList

	def removeEmptyOptionGroups(self, _optionData):

		#   Whack empty Option occurrences, as if they don't even exist.

		maxOptions = self.getMaxOptions()
		keysToDelete = []

		for idx in range(1, maxOptions + 1):
			idxStr = str(idx)
			optionDict = _optionData[idxStr]
			if (not optionDict['code']) and \
				(not optionDict['descr']) and \
				(not optionDict['display_text']) and \
				(not optionDict['show_codes']) and \
				(not optionDict['hide_codes']):
				keysToDelete.append(idxStr)

		for key in keysToDelete:
			del _optionData[key]

	def resequenceOptionData(self, _formData, _optionData):
		optionList = []
		newSequenceNbr = 0
		optionSequence = _formData.get('option_sequence', [])
		for seqNbr in optionSequence:
			if seqNbr in _optionData:
				newSequenceNbr += 1
				optionDict = _optionData[seqNbr]
				optionDict['seq'] = newSequenceNbr
				optionList.append(optionDict)
		return optionList

	def validateFormData(self, _connection, _question, _formData, _optionData, _originalCodeList, _isEdit):
		jErrors = []

		#   --------
		#   QUESTION
		#   --------

		#   Check required fields.
		requiredFields = ['code','descr','required','wrap','encrypt','data_type']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Size and Placement fields must be integers if specified, otherwise fill in default values.
		intErrors = []
		self._validateInteger(_formData, 'cols_offset', 0, intErrors)
		self._validateInteger(_formData, 'cols_label', 2, intErrors)
		self._validateInteger(_formData, 'cols_prompt', 8, intErrors)
		if intErrors:
			jErrors.extend(intErrors)
		else:
			total = _formData.get('cols_offset', 0) + _formData.get('cols_label', 0) + _formData.get('cols_prompt', 0)
			if total > 12:
				jErrors.append({ 'code': 'cols_offset', 'field_value': '', 'message': 'Cannot specify more than 12 total columns' })

		#   Data type must be valid.
		dataType = _formData.get('data_type', '').strip()
		if dataType:
			dataTypesCache = self.getQuestionDataTypesCache()
			if dataType not in dataTypesCache:
				jErrors.append({ 'code': 'data_type', 'field_value': '', 'message': 'Unknown data type' })

		#   Job Action types must be valid.
		jobActionTypes = []
		jobActionTypesCache = self.getJobActionTypesCache(_connection)
		maxJobActionTypes = self.getMaxJobActionTypes()
		for idx in range(1, maxJobActionTypes + 1):
			key = "job_action_type_%i" % idx
			jaType = _formData.get(key, '').strip()
			if jaType:
				if jaType not in jobActionTypesCache:
					jErrors.append({ 'code': key, 'field_value': '', 'message': 'Unknown Job Action Type' })
				else:
					jobActionTypes.append(jaType)
		_formData['job_action_types'] = ','.join(jobActionTypes)


		#   -------
		#   OPTIONS
		#   -------

		for key in _optionData.keys():
			optionDict = _optionData[key]

			#   Check required fields.
			requiredFields = ['code','descr']
			for fieldCode in requiredFields:
				fieldValue = optionDict.get(fieldCode, '')
				if not fieldValue:
					jErrors.append({ 'code': "%s_%s" % (fieldCode, key), 'field_value': '', 'message': 'Required' })


		#   ------------------------------------------------------------
		#   CODES
		#   All Codes must be unique across Question, Option, and Group.
		#   ------------------------------------------------------------

		usedCodeList = []
		questionCode = _formData.get('code', '').strip()
		if questionCode:
			usedCodeList.append(questionCode)
			if questionCode in _originalCodeList:
				_originalCodeList.remove(questionCode)
			else:
				self._duplicateCodeCheck(_connection, questionCode, 'code', jErrors)

		for key in _optionData.keys():
			optionDict = _optionData[key]
			optionCode = optionDict.get('code', '')
			fieldName = 'option_code_%s' % key
			if optionCode:
				if optionCode in usedCodeList:
					jErrors.append({ 'code': fieldName, 'field_value': optionCode, 'message': 'Duplicate code' })
				else:
					usedCodeList.append(optionCode)
					if optionCode in _originalCodeList:
						_originalCodeList.remove(optionCode)
					else:
						self._duplicateCodeCheck(_connection, optionCode, fieldName, jErrors)


		#   Narc if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)


#   Uber Administrative Documentation

class UberDocumentationHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		#   Locate the documentation PDF.
		#   Copy to the PDF area.
		#   Redirect to URL.

		docFolder = self.getEnvironment().buildFullPathToCommonDocumentation()
		docFilePath = os.path.join(docFolder, 'SmartPathForms.pdf')
		with open(docFilePath, "rb") as f:
			data = f.read()

		dstFilePath = self.getEnvironment().createGeneratedOutputFileInFolderPath('SmartPathForms.pdf')
		with open(dstFilePath, "wb") as f:
			f.write(data)
			f.flush()

		uiPath = self.getEnvironment().getUxGeneratedOutputFilePath(dstFilePath)
		self.redirect(uiPath)


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/uber/questions', UberQuestionHandler),
	(r'/appt/uber/questions/add', UberQuestionAddHandler),
	(r'/appt/uber/questions/edit/(?P<questionid>[^/]*)', UberQuestionEditHandler),
	(r'/appt/uber/questions/save', UberQuestionSaveHandler),
	(r'/appt/uber/documentation', UberDocumentationHandler),
]
