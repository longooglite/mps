# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import os
import base64
import datetime
from dateutil.relativedelta import relativedelta

from multiprocessing import Process

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.reportingService as reportingSvc
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.core.constants as constants


kSinglePicklist = 'singlepicklist'
kMultiPicklist = 'multipicklist'

class ReportingViewHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()

		reportid = kwargs.get('reportid', '')
		if not reportid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			now = self.getEnvironment().formatUTCDate()
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			rawFileContent = reportingSvc.ReportingService(connection).getReportForUser(community, username, int(reportid), now)
			if rawFileContent:
				env = envUtils.getEnvironment()
				contentType  = rawFileContent.get('file_type','PDF')
				if contentType == constants.kFileTypeExcel:
					extension = '.xls'
					path = env.createGeneratedOutputFileInFolderPath(rawFileContent.get('report_name','') + extension)
					content = rawFileContent.get('content','')
					f = open(path,'w')
					f.write(bytearray(content))
					f.close()
				else:
					extension = '.pdf'
					path = env.createGeneratedOutputFileInFolderPath(rawFileContent.get('report_name','') + extension)
					content =  base64.b64decode(str(rawFileContent.get('content','')))
					f = open(path,'wb')
					f.write(bytearray(content))
					f.flush()
					f.close()

				uiPath = env.getUxGeneratedOutputFilePath(path)
				self.redirect(uiPath)
			else:
				self.redirect("/appt")

		finally:
			self.closeConnection()


class ReportingHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		connection = self.getConnection()
		try:
			formData = tornado.escape.json_decode(self.request.body)
			configDict = self.getConfig(formData.get('config',{}))
			context = {}
			context['dbConnectionParms'] = self.dbConnection.dbConnectionParms
			context['profile'] = self.getProfile()
			context['config'] = configDict
			formData.pop("_xsrf", None)
			formData.pop("mpsid", None)
			context['formData'] = formData
			context['reportingcss'] = self.getCSSPath()
			context['env'] = self.getEnvironment()
			context['loader'] = self.getEnvironment().getTemplateLoader()
			context['reporting_params'] = self.validateFormDataAndReturnReportParams(formData,configDict)
			p = Process(target=self.loadAndRunReport, args=(configDict,context,))
			p.start()
			responseDict = self.getPostResponseDict("Processing report. It will appear in the Reports Archive upon completion.")
			responseDict['redirect'] = '/appt'
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()

	def loadAndRunReport(self,configDict,params):
		fileName = configDict.get('srcFile','')
		className = fileName[0].upper()+fileName[1:len(fileName)]
		importStrings = []
		#   Try to load from site specific script first, if that fails load from application script
		importStrings.append("import data.atramData.sites.%s.reports.scripts.%s as reporter" % (self.getProfile().get('siteProfile',{}).get('site',''),fileName))
		importStrings.append("import data.reporting.scripts.%s as reporter" % (fileName))
		for importString in importStrings:
			try:
				exec(importString)
				report = eval("reporter.%s(params)" % (className))
				hasData = report.run()
				break
			except Exception,e:
				pass

	def getCSSPath(self):
		path = os.path.abspath(__file__).split('MPSAppt')[0] + 'data/reporting/reports.css'
		return path

	def validateFormDataAndReturnReportParams(self, _formData, _configDict):
		reportParams = []
		jErrors = []
		for prompt in _configDict.get('prompts',[]):
			if prompt.get('required',False):
				controlName = prompt.get('controlName','')
				userInput =  _formData.get(controlName,'')
				if prompt.get('affordancetype','') <> 'date_entry':
					reportParams.append({"controlName":controlName,"input":userInput})
				if not userInput:
					jErrors.append({'code':controlName,'field_value': userInput,'message': "Required"})
				elif prompt.get('affordancetype','') == 'date_entry':
					try:
						format = self.getDateFormat(prompt.get('validate_date_format',''))
						aDate = dateUtils.flexibleDateMatch(userInput, format)
						reportParams.append({"controlName":controlName,"input":aDate})
					except Exception, e:
						jErrors.append({'code':controlName, 'field_value': userInput, 'message': "Invalid Date"})
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)
		reportParams.append({"controlName":'file_type',"input":_formData.get('file_type','PDF')})
		return reportParams

	def getDateFormat(self,configFormat):
		if configFormat:
			if configFormat.upper() == 'Y/M/D' or configFormat.upper() == 'MM/DD/YYYY':
				return  self.getSiteYearMonthDayFormat()
			elif configFormat.upper() == 'M/Y' or configFormat.upper() == 'MM/YYYY':
				return self.getSiteYearMonthFormat()
			elif configFormat.upper() == 'Y/M/D H:M':
				return self.getSiteYearMonthDayHourMinuteFormat()
		return self.getSiteYearMonthDayFormat()


	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()

		item = kwargs.get('reportconfig', '')
		if item == 'viewarchive':
			self._viewArchiveHandler(**kwargs)
			return

		connection = self.getConnection()
		try:
			config = self.getConfig(item)
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['config'] = config
			self.setDefaults(config)
			context['configFile'] = item
			context['url'] = '/appt/reporting/%s' % (item)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.getPicklists(config,connection,context,community,username)
			self.render("reporting.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

	def setDefaults(self,config):
		for prompt in config.get('prompts',[]):
			if prompt.get('affordancetype') == 'date_entry':
				default = prompt.get('default','')
				if default:
					prompt['defaultValue'] = self.getDateDefault(default,prompt.get('date_format',''))

	def getDateDefault(self,default,format):
		if default == 'now':
			date = dateUtils.formatUTCDateOnly()
			return dateUtils.parseDate(date,self.getDateFormat(format))
		elif default.startswith('minus') or default.startswith('plus'):
			parts = default.split('_')
			operator = parts[0]
			number = int(parts[1])
			qualifier = parts[2]
			now = datetime.datetime.now()
			offset_date = now
			if operator == 'minus':
				number = -number
			rDelta = None
			if qualifier == "Y":
				rDelta = relativedelta(years=number)
			elif qualifier == "M":
				rDelta = relativedelta(months=number)
			elif qualifier == "D":
				rDelta = relativedelta(days=number)
			if rDelta:
				offset_date = now + rDelta
			date = dateUtils.formatUTCDateOnly(offset_date)
			return dateUtils.parseDate(date,self.getDateFormat(format))

	def _viewArchiveHandler(self,**kwargs):
		connection = self.getConnection()
		try:
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			reportsService = reportingSvc.ReportingService(connection)
			reports = reportsService.getReportsForUser(community, username)
			self.formatReportData(reports)
			context['reports'] = reports
			context['reportpurgedays'] = self.getSitePreference("reportpurgedays","90")
			self.render("reportingarchive.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

	def formatReportData(self,reports):
		for report in reports:
			datePref = self.getDateFormat('Y/M/D H:M')
			if datePref:
				dateString = report.get('date_created','')
				if dateString:
					dateString = dateUtils.localizeUTCDate(dateString,self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('timezone','US/Eastern'))
					formattedValue = dateUtils.parseDate(dateString,datePref)
					report['date_created'] = formattedValue
			url = '/appt/reporting/view/%i' % (report.get('id',-1))
			report['report_url'] = url

	def getPicklists(self,config,connection,context,community,username):
		reportingService = reportingSvc.ReportingService(connection)
		prompts = config.get('prompts',[])
		for entity in prompts:
			if entity.get('affordancetype','') == kSinglePicklist or entity.get('affordancetype','') == kMultiPicklist:
				tableName = entity.get('tableName')
				retrictToUserPermission = entity.get('restrictToUserPermission',False)
				entityList = reportingService.getReportingFilterForKey(tableName,community,username,retrictToUserPermission)
				context[tableName] = entityList

	def getConfig(self,filename):
		config = {}
		foundConfig = False
		try:
			importString = "from data.atramData.sites.%s.reports.configurations import %s" % (self.getProfile().get('siteProfile',{}).get('site',''),filename)
			exec(importString)
			config =  eval(filename).config
			foundConfig = True
		except:
			pass
		try:
			if not foundConfig:
				importString = "from data.reporting.configurations import %s" % (filename)
				exec(importString)
				config =  eval(filename).config
		except Exception,e:
			pass
		return config

	def getReportsPath(self):
		coreEnvUtilities = coreEnvUtils.CoreEnvironment()
		corePath = coreEnvUtilities.getSrcCoreFolderPath()
		configPath = corePath.split('MPSCore')[0] + "%s%s%s%s%s%s%s%s%s%s" % ('data',os.sep,'atramData',os.sep,'sites',os.sep,self.getProfile().get('siteProfile',{}).get('site',''),os.sep,"reports",os.sep)
		return configPath


class DeleteArchiveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl( **kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.

		reportid = kwargs.get('reportid', '')
		if not reportid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			reportingSvc.ReportingService(connection).deleteReport(reportid)
			responseDict = self.getPostResponseDict('')
			responseDict['redirect'] = '/appt/reporting/viewarchive'
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/reporting/(?P<reportconfig>[^/]*)", ReportingHandler),
	(r"/appt/reporting/view/(?P<reportid>[^/]*)", ReportingViewHandler),
	(r"/appt/reporting/delete/(?P<reportid>[^/]*)", DeleteArchiveHandler),
]
