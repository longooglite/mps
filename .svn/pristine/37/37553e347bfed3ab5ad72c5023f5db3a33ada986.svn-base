# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime
import logging
import os
import os.path
import uuid
import json
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.stringUtilities as stringUtils

#   Global CoreEnvironment settings.
#   Intended to be used as a super-class for application-specified CoreEnvironment classes.

class CoreEnvironment():
	logger = logging.getLogger(__name__)

	#   Release Code Names use an automobile manufacturer theme:
	#
	#   Audi
	#   Buick
	#   Chevrolet
	#   Dodge
	#   Eagle
	#   Ferrari
	#   Geo
	#   Honda
	#   Infiniti
	#   Jaguar
	#   Kia
	#   Lincoln
	#   Mercury
	#   Nissan
	#   Oldsmobile
	#   Plymouth
	#   Queen
	#   Rolls
	#   Subaru
	#   Tesla
	#   Union
	#   Volkswagen
	#   Willys
	#   Xander
	#   Yugo
	#   Zimmer

	def __init__(self):
		self.srcCoreFolderPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

		f = open(self.srcCoreFolderPath.split('MPSCore')[0] + '%s%s%s%s' % (os.sep,'config',os.sep,'version.json'),'rU')
		versionDict = json.loads(f.read())
		versionDict['releaseBuildDate'] = datetime.datetime.strptime(versionDict.get('releaseBuildDate','1000-01-01 10:00'),"%Y-%m-%d %H:%M")
		f.close()

		self.version = versionDict.get('version','')
		self.releaseCodeName = versionDict.get('releaseCodeName','')
		self.releaseStatus = versionDict.get('releaseStatus','')
		self.releaseBuildDate = versionDict.get('releaseBuildDate',None)

		self.envCode = None
		self.appCode = None
		self.listenPort = None
		self.templateLoader = None
		self.authServiceUrl = None
		self.srcRootFolderPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).split('/car')[0] + '/car/'
		self.generatedOutputFolderPath = os.sep + "tmp" + os.sep + "pdf" + os.sep
		self.wkhtmltopdfBinPath = ''
		self.pdftkBinPath = ''
		self.dropdbbinpath = ''
		self.createdbbinpath = ''
		self.pgdumpbinpath = ''
		self.psqlbinpath = ''
		self.dumpFolderPath = ''
		self.skinFolderPath = '/usr/local/mps'
		self.emailOn = False
		self.emailTo = []

		self.loginUri = '/mps/login'
		self.toastUri = '/mps/toast'


	#   Read-only Version code.
	#   Read-only Release Code Name.
	#   Read-only Release Status.
	#   Read-only Release Build Date.
	#   Set and maintained entirely by this module.

	def getVersion(self): return self.version
	def getReleaseCodeName(self): return self.releaseCodeName
	def getReleaseStatus(self): return self.releaseStatus
	def getReleaseBuildDate(self): return self.releaseBuildDate


	#   CoreEnvironment code, set by application.

	def getEnvCode(self): return self.envCode
	def setEnvCode(self, _envCode): self.envCode = _envCode


	#   Application code, set by application.

	def getAppCode(self): return self.appCode
	def setAppCode(self, _appCode): self.appCode = _appCode


	#   Application URI Prefix, set by application.

	def getAppUriPrefix(self): return self.appUriPrefix
	def setAppUriPrefix(self, _appUriPrefix): self.appUriPrefix = _appUriPrefix


	#   Listener port, set by application.

	def getListenPort(self): return self.listenPort
	def setListenPort(self, _listenPort): self.listenPort = _listenPort


	#   Template Loader, set by application.

	def getTemplateLoader(self): return self.templateLoader
	def setTemplateLoader(self, _templateLoader): self.templateLoader = _templateLoader


	#   URL to the MPS Platform Authorization Service, set by application.

	def getAuthServiceUrl(self): return self.authServiceUrl
	def setAuthServiceUrl(self, _authServiceUrl): self.authServiceUrl =_authServiceUrl


	#   Absolute path to the application's 'root' folder, set by application.

	def getSrcRootFolderPath(self): return self.srcRootFolderPath
	def setSrcRootFolderPath(self, _srcRootFolderPath): self.srcRootFolderPath = _srcRootFolderPath


	#   Email services Master Switch, set by application.

	def getEmailOn(self): return self.emailOn
	def setEmailOn(self, _emailOn): self.emailOn = stringUtils.interpretAsTrueFalse(_emailOn)


	#   EmailTo, set by application.
	#   Specify a non-empty EmailTo *LIST* to force the application to send all email to the
	#   specified address(es), ignoring any to, cc, and bcc settings for any particular email.
	#   Useful primarily in non-production environments.

	def getEmailTo(self): return self.emailTo
	def setEmailTo(self, _emailTo): self.emailTo = _emailTo


	#   Full path to wkhtmltopdf binary, set by application.

	def getWkhtmltopdfBinPath(self): return self.wkhtmltopdfBinPath
	def setWkhtmltopdfBinPath(self, _wkhtmltopdfBinPath): self.wkhtmltopdfBinPath = _wkhtmltopdfBinPath

	#   Full path to pdftfBin binary, sey by application.

	def getPDFtkBinPath(self): return self.pdftkBinPath
	def setPDFtkBinPath(self, _pdftkBinPath): self.pdftkBinPath = _pdftkBinPath

	#   Full path to dropdb binary (postgres), sey by application.

	def getDropdbBinPath(self): return self.dropdbbinpath
	def setDropdbBinPath(self, _dropdbbinpath): self.dropdbbinpath = _dropdbbinpath

	#   Full path to createdb binary (postgres), sey by application.

	def getCreatedbBinPath(self): return self.createdbbinpath
	def setCreatedbBinPath(self, _createdbbinpath): self.createdbbinpath = _createdbbinpath

	#   Full path to pg_dump binary (postgres), sey by application.

	def getPgdumpBinPath(self): return self.pgdumpbinpath
	def setPgdumpBinPath(self, _pgdumpbinpath): self.pgdumpbinpath = _pgdumpbinpath

	#   Full path to psql binary (postgres), sey by application.

	def getPsqlBinPath(self): return self.psqlbinpath
	def setPsqlBinPath(self, _psqlbinpath): self.psqlbinpath = _psqlbinpath

	#   Path to dump folder (postgres database dumps), set by application.

	def getDumpFolderPath(self): return self.dumpFolderPath
	def setDumpFolderPath(self, _dumpFolderPath): self.dumpFolderPath = _dumpFolderPath

	#   Path to skin folder (the folder from which nginx serves static content), set by application.

	def getSkinFolderPath(self): return self.skinFolderPath
	def setSkinFolderPath(self, _skinFolderPath): self.skinFolderPath = _skinFolderPath


	#   Read-only absolute path to the MPS Platform's 'Core' folder.
	#   Set and maintained entirely by this module.

	def getSrcCoreFolderPath(self): return self.srcCoreFolderPath
	def getSrcCoreHtmlFolderPath(self): return os.path.join(self.getSrcCoreFolderPath(), 'html')


	#   Read-only absolute path to folder where generated output is placed.
	#   Set and maintained entirely by this module.

	def getGeneratedOutputFolderPath(self): return self.generatedOutputFolderPath

	def createGeneratedOutputFileInFolderPath(self, fileName):
		if not os.path.exists(self.getGeneratedOutputFolderPath()):
			os.mkdir(self.getGeneratedOutputFolderPath())
		uniqueFolderPath = self.getGeneratedOutputFolderPath() + self.generateUniqueId() + os.sep
		os.mkdir(uniqueFolderPath)
		return uniqueFolderPath + fileName


	#   Read-only absolute path to the a site's template and image folders.

	def buildFullPathToSiteTemplatesList(self, _site):
		import MPSAppt.utilities.environmentUtils as envUtils
		root = envUtils.getEnvironment().getSrcRootFolderPath()
		site = _site.replace('-','_')
		siteFilePath = os.path.join(root, 'data', 'atramData', 'sites', site, 'templates')
		commonFilePath = os.path.join(root, 'data', 'atramData', 'common', 'templates')
		return [siteFilePath, commonFilePath]

	def buildFullPathToSiteImagesList(self, _site):
		import MPSAppt.utilities.environmentUtils as envUtils
		root = envUtils.getEnvironment().getSrcRootFolderPath()
		site = _site.replace('-','_')
		siteFilePath = os.path.join(root, 'data', 'atramData', 'sites', site, 'images')
		commonFilePath = os.path.join(root, 'data', 'atramData', 'common', 'images')
		return [siteFilePath, commonFilePath]

	def buildFullPathToCVSiteTemplatesList(self, _site):
		import MPSCV.utilities.environmentUtils as cvenvUtils
		site = _site.replace('-','_')
		root = cvenvUtils.getEnvironment().getSrcRootFolderPath()
		siteFilePath = os.path.join(root, 'data', 'cvMetaData', 'sites', site, 'templates')
		commonFilePath = os.path.join(root, 'MPSCV', 'html')
		return [siteFilePath, commonFilePath]

	#   Read-only absolute path to common documentation folder.

	def buildFullPathToCommonDocumentation(self):
		import MPSAppt.utilities.environmentUtils as envUtils
		root = envUtils.getEnvironment().getSrcRootFolderPath()
		documentationFolderPath = os.path.join(root, 'data', 'documentation')
		return documentationFolderPath


	def createGeneratedOutputFilePath(self, _optionalPrefix='', _optionalSuffix=''):
		if not os.path.exists(self.getGeneratedOutputFolderPath()):
			os.mkdir(self.getGeneratedOutputFolderPath())

		parts = []
		parts.append(self.getGeneratedOutputFolderPath())
		if _optionalPrefix: parts.append(_optionalPrefix)
		parts.append(self.generateUniqueId())
		if _optionalSuffix: parts.append(_optionalSuffix)
		return ''.join(parts)

	def getUxGeneratedOutputFilePath(self, _generatedPath):
		idx = _generatedPath.find(os.sep,1)
		return _generatedPath[idx:]


	#   Read-only network availability.
	#   Indicates whether or not a connection to the internet is available to this application.
	#   Set and maintained entirely by this module.
	#   Intent here is to avoid communication with the outside world when running a demo
	#   version of SmartPath on a laptop which does not have internet access.

	def getAvoidNetwork(self):
		if os.environ.has_key('CAR_AVOIDNETWORK'):
			return stringUtils.interpretAsTrueFalse(os.environ['CAR_AVOIDNETWORK'])
		return False


	#   Read-only Login URI.
	#   Global URI to get to the MPS Platform's Login application.
	#   Set and maintained entirely by this module.

	def getLoginUri(self): return self.loginUri


	#   Read-only U-R-Toast URI.
	#   Global URI to get to the MPS Platform's hey-there's-an-error and/or you-logged-out screen.
	#   Set and maintained entirely by this module.

	def getToastUri(self): return self.toastUri


	#   Read-only UTC Date format.
	#   Date format used for storing dates in databases, and
	#   for transmitting dates between applications.
	#   Set and maintained entirely by this module.

	def getUTCDateFormat(self): return dateUtils.kUTCDateFormat


	#   Format the given datetime using the global date format.

	def formatUTCDate(self, _datetime=None):
		return dateUtils.formatUTCDate(_datetime)


	#   Parses the given date string using the global date format.

	def parseUTCDate(self, _datestring):
		return dateUtils.parseUTCDate(_datestring)


	#   Convert a given datetime string to a localized datetime string.
	#   The given date is assumed to be in utcDateFormat, and is assumed
	#   to be a UTC time. The timezone name (i.e. 'US/Eastern') is used
	#   to convert the UTC time to the indicated timezone.
	#
	#   Errors simply return to original _utcDateString and note the
	#   problem by logging an error.

	def localizeUTCDate(self, _utcDateString, _tzname='US/Eastern'):
		return dateUtils.localizeUTCDate(_utcDateString, _tzname)


	#   Convert a given local datetime string to a UTC datetime string.
	#   The given date is assumed to be in utcDateFormat, and is assumed
	#   to be a time in the given timezone name (i.e. 'US/Eastern').
	#
	#   Errors simply return to original _localDateString and note the
	#   problem by logging an error.

	def utcizeLocalDate(self, _localDateString, _tzname='US/Eastern'):
		return dateUtils.utcizeLocalDate(_localDateString, _tzname)


	#   Generate a unique identifier.
	#   Used for session and message identifiers.

	def generateUniqueId(self):
		return uuid.uuid4().get_hex()


	#   Get core application URL for a given app.

	def getApplicationURLPrefix(self, _appCode, _appList):
		appURL = self.getApplicationURL(_appCode,_appList)
		return appURL[:appURL.rfind('/')]

	def getApplicationURL(self, _appCode, _appList):
		for appDict in _appList:
			if appDict.get('code','') == _appCode:
				return appDict.get('url','')
		return ''


def getEnvironment():
	#   Must implement in subclass.
	pass
