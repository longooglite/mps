# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os
import base64
import MPSAppt.services.reportingService as reportingSvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.sqlUtilities as sqlUtils
import MPSCore.utilities.dateUtilities as dateUtils



class BaseReport:
	def __init__(self,_context):
		self.context = _context
		self.env = self.context.get('env',{})
		self.connection = None

	def run(self):
		pass

	def getDbConnection(self):
		if not hasattr(self, 'connection'):
			self.connection(None)
		return self.connection

	def setDbConnection(self, _dbConnection): self.connection = _dbConnection

	def getConnection(self):
		if self.context.get('dbConnectionParms',{}):
			connection = sqlUtils.SqlUtilities(self.context['dbConnectionParms'])
			self.setDbConnection(connection)
			return self.getDbConnection()
		return None

	def closeConnection(self):
		if self.getDbConnection():
			self.getDbConnection().closeMpsConnection()
			self.setDbConnection(None)

	def persistReport(self,connection,_filePath):
		handle = None
		try:
			if self.context.get('formData',{}).get('file_type','') == constants.kFileTypePDF:
				handle = open(_filePath,'rb')
				bytes = bytearray(handle.read())
				content = base64.b64encode(str(bytes))
			else:
				handle = open(_filePath,'rU')
				content = handle.read()
			reportSvc = reportingSvc.ReportingService(connection)
			reportSvc.persistReport(self.context,content)
			self.displayUnreadReports()
		except:
			pass
		finally:
			if handle:
				handle.close()

	def generatePDF(self,html,_footerText = '',_setFooter = True, _prefix = 'report',_portrait=True):
		uiPath,fullPath = pdfUtils.createPDFFromHTML(html, self.env, name = _footerText, setFooter = _setFooter, prefix = _prefix,portrait=_portrait)
		return uiPath,fullPath

	def generateTextFile(self,textList):
		txtFilePath = self.env.createGeneratedOutputFilePath('deptlist', '.txt')
		f = open(txtFilePath,'w')
		try:
			for row in textList:
				f.write('\t'.join(row) + '\n')
		except:
			pass
		finally:
			f.close()
		return txtFilePath

	def getInitialContext(self):
		context = {}
		context['noDataMessage'] = "0 items meet report criteria"
		context['reportingcss'] = self.context.get('reportingcss','')
		return context

	def displayUnreadReports(self):
		#tbd need to send message to front end, some how, some way
		community = self.context.get('profile',{}).get('userProfile',{}).get('community', 'default')
		username = self.context.get('profile',{}).get('userProfile',{}).get('username','')
		unreadReports = reportingSvc.ReportingService(self.connection).getNbrUnreadReportsForUser(community, username)

	def getHTML(self,templateName,context):

		headerTemplate = self.getTemplate(self.getHeaderFooterTemplatePath(),'reportHeader.html')
		headerhtml = headerTemplate.generate(context=context)

		variableContentTemplate = self.getTemplate(self.getTemplatesPath(templateName),templateName)
		bodyhtml = variableContentTemplate.generate(context=context)

		footerTemplate = self.getTemplate(self.getHeaderFooterTemplatePath(),'reportFooter.html')
		footerhtml = footerTemplate.generate(context=context)
		return ''.join([headerhtml,bodyhtml,footerhtml])


	def getPrefAsInt(self,key, defaultValue):
		prefs = self.context.get('profile',{}).get('siteProfile',{}).get('sitePreferences',{})
		value = defaultValue
		try:
			value = int(prefs.get(key,defaultValue))
		except:
			pass
		return value

	def getReportParameter(self,key):
		params = self.context.get('reporting_params',[])
		for param in params:
			if param.get('controlName',{}) == key:
				return param.get('input',None)
		return None

	# path-related stuff

	def getNewFilePath(self,fileName,extension):
		return self.env.createGeneratedOutputFileInFolderPath(fileName + extension)

	def getFileName(self):
		name = self.context.get('config',{}).get('reportName','')
		return self.getNewFilePath(name,'.'+ self.getExtension())

	def getExtension(self):
		if self.context.get('formData',{}).get('file_type','') == constants.kFileTypePDF:
			extension = 'pdf'
		else:
			extension = 'txt'
		return extension

	def getSite(self):
		return self.context.get('profile',{}).get('siteProfile',{}).get('site','')

	def getCorePath(self):
		path = os.path.abspath(__file__).split('reporting')[0]
		return path

	def getTemplatesPath(self,templateName):
		site = self.getSite()
		path = self.getCorePath() + 'atramData%ssites%s%s%sreports%stemplates%s' % (os.sep,os.sep,site,os.sep,os.sep,os.sep)
		if os.path.exists(path + templateName):
			return path
		path = self.getCorePath() + 'reporting%stemplates%s' % (os.sep,os.sep)
		return path

	def getConfigurationsPath(self):
		site = self.getSite()
		path = self.getCorePath() + 'atramData%ssites%s%s%sreports%sconfigurations%s' % (os.sep,os.sep,site,os.sep,os.sep,os.sep)
		if os.path.exists(path):
			return path
		path = self.getCorePath() + 'reporting%sconfigurations%s' % (os.sep,os.sep)
		return path

	def getScriptsPath(self):
		site = self.getSite()
		path = self.getCorePath() + 'atramData%ssites%s%s%sreports%sscripts%s' % (os.sep,os.sep,site,os.sep,os.sep,os.sep)
		if os.path.exists(path):
			return path
		path = self.getCorePath() +  'reporting%sscripts%s' % (os.sep,os.sep)

		return path

	def getTemplate(self,templatePath,templateName):
		return self.context['loader'].load(templatePath + templateName)

	def getHeaderFooterTemplatePath(self):
		path = self.getCorePath() + 'reporting%s' % (os.sep,)
		return path

	#   Dates

	def formatDateForDisplay(self,dateStr):
		if dateStr:
			dateFormat = self.context.get('profile',{}).get('siteProfile',{}).get('sitePreferences',{}).get('ymdformat','%m/%d/%Y')
			return dateUtils.parseDate(dateStr, dateFormat)
		return ''

	#   URL

	def getJobActionURL(self, jobActionId, appCode="APPT"):
		siteAppList = self.context.get('profile',{}).get('siteProfile',{}).get('siteApplications',{})
		for app in siteAppList:
			if app.get('code','') == appCode:
				return app.get('url','') + '/jobaction/' + str(jobActionId)
		return ''

	#   Graphing
	def getColors(self):
		return ('#F44336', '#3F51B5', '#009688', '#FFC107', '#FF5722', '#9C27B0', '#03A9F4', '#8BC34A', '#FF9800', '#E91E63', '#2196F3', '#4CAF50', '#FFEB3B', '#673AB7', '#00BCD4', '#CDDC39', '#795548', '#9E9E9E', '#607D8B')
