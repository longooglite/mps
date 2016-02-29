# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractUberAdminHandler as absHandler
import MPSAppt.services.uberService as uberSvc


#   Export

class AbstractUberExportHandler(absHandler.AbstractUberAdminHandler):
	logger = logging.getLogger(__name__)

	def _exportHandler(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptUberEdit'])

		connection = self.getConnection()
		try:
			dstFilePath = self.getEnvironment().createGeneratedOutputFileInFolderPath(kwargs.get('outputFilename', 'data.xls'))
			with open(dstFilePath, "wb") as dstFile:
				columnDefinitions = self.getColumnDefinitions()
				line =  '#' + '\t'.join(columnDefinitions) + '\n\n'
				dstFile.write(line)

				for row in self.getRowData(connection):
					parts = []
					for columnName in columnDefinitions:
						parts.append(str(row.get(columnName, '')))
					dstFile.write('\t'.join(parts) + '\n')

				dstFile.flush()

			uiPath = self.getEnvironment().getUxGeneratedOutputFilePath(dstFilePath)
			self.redirect(uiPath)

		finally:
			self.closeConnection()

	def writeColumnHeaders(self, _dstFile, _columnDefinitions):
		line =  '#' + '\t'.join(_columnDefinitions)
		_dstFile.write(line)


	#   Subclasses must implement:

	def getColumnDefinitions(self):
		return []

	def getRowData(self, _connection):
		return []


class UberGroupExportHandler(AbstractUberExportHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['outputFilename'] = 'uberGroups.xls'
		self._exportHandler(**kwargs)

	def getColumnDefinitions(self):
		return ['code','descr','display_text','cols_offset','cols_label','repeating','repeating_table','required','wrap','filler','children']

	def getRowData(self, _connection):
		return uberSvc.UberService(_connection).getUberGroups()


class UberQuestionExportHandler(AbstractUberExportHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['outputFilename'] = 'uberQuestions.xls'
		self._exportHandler(**kwargs)

	def getColumnDefinitions(self):
		return ['code','descr','display_text','header_text','cols_offset','cols_label','cols_prompt','required','wrap','encrypt','data_type','data_type_attributes','job_action_types','identifier_code','show_codes','hide_codes']

	def getRowData(self, _connection):
		return uberSvc.UberService(_connection).getUberQuestions()


class UberOptionExportHandler(AbstractUberExportHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		kwargs['outputFilename'] = 'uberOptions.xls'
		self._exportHandler(**kwargs)

	def getColumnDefinitions(self):
		return ['question_code','code','descr','display_text','seq','show_codes','hide_codes']

	def getRowData(self, _connection):
		questionCache = {}
		for each in uberSvc.UberService(_connection).getUberQuestions():
			id = each.get('id', 0)
			code = each.get('code', '')
			if id and code:
				questionCache[id] = code

		options = uberSvc.UberService(_connection).getUberOptions()
		for each in options:
			questionId = each.get('uber_question_id')
			each['question_code'] = questionCache.get(questionId, '')

		return options


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/uber/export/groups', UberGroupExportHandler),
	(r'/appt/uber/export/questions', UberQuestionExportHandler),
	(r'/appt/uber/export/options', UberOptionExportHandler),
]
