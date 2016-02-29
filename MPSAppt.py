# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import optparse
import os
import os.path
import sys
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import MPSCore.utilities.configUtilities as configUtils
import MPSCore.utilities.logUtils as logUtils
import MPSAppt.utilities.environmentUtils as envUtils

#   Runs the MPS Appointment application.

class MPSAppt():

	def get_parser(self):
		parser = optparse.OptionParser(description='MPS Appointment application')
		parser.add_option('-e', '--env', dest='env',
			default='dev',
			help='environment (default=dev)')
		parser.add_option('-f', '--file', dest='file',
			default='config/{env}/MPSAppt/config.json',
			help='json config file (default=config/{env}/MPSAppt/config.json)')
		return parser

	def run(self, options, args):

		#   Load the configuration file.
		configFilePath = options.file.replace('{env}', options.env)
		srcRootFolderPath = os.path.dirname(os.path.abspath(__file__))
		configDict = self.loadConfig(options.env, self.resolveFilePath(srcRootFolderPath, configFilePath))

		#   Initialize the global environment.
		env = envUtils.getEnvironment()
		env.setEnvCode(configDict['environment'])
		env.setListenPort(configDict['listenport'])
		env.setSrcRootFolderPath(srcRootFolderPath)
		env.setAuthServiceUrl(configDict['authserviceurl'])
		env.setWkhtmltopdfBinPath(configDict['wkhtmltopdfbinpath'])
		env.setPDFtkBinPath(configDict['pdftkbinpath'])
		env.setSkinFolderPath(configDict['skinfolderpath'])
		env.setEmailOn(configDict['email'])
		env.setEmailTo(configDict['emailto'])
		env.setJobActionCompletionOn(configDict['jobcompletiontask'])
		env.setReportingCleanupOn(configDict['reportingcleanuptask'])
		env.setBackgroundCheckCompletionOn(configDict['backgroundchecktask'])
		env.setBackgroundCheckIntervalMinutes(configDict['backgroundcheckintervalminutes'])

		#   Initialize logging.
		logUtils.initLogging(self.resolveFilePath(srcRootFolderPath, configDict['loggingconfig']))
		logger = logging.getLogger(__name__)
		logger.info("MPSAppt started")
		logger.info("MPSAppt CoreEnvironment '%s'" % str(env.getEnvCode()))
		logger.info("MPSAppt Listening on port '%s'" % str(env.getListenPort()))
		logger.info("MPSAppt Email '%s'" % str(env.getEmailOn()))
		logger.info("MPSAppt EmailTo Override '%s'" % str(env.getEmailTo()))
		if os.environ.has_key('CAR_EMAILTO'):
			logger.info("MPSAppt EmailTo Environment Override '%s'" % str(os.environ['CAR_EMAILTO']))
		if env.getAvoidNetwork():
			logger.info("MPSAppt Internet access is not available")

		#   Set up the Service request handlers.
		import tornado.web
		from MPSAppt.handlers import mainHandler
		from MPSAppt.handlers import positionHandler
		from MPSAppt.handlers import personHandler
		from MPSAppt.handlers import jobActionHandler
		from MPSAppt.handlers import fileUploadHandler
		from MPSAppt.handlers import packetDownloadHandler
		from MPSAppt.handlers import approvalHandler
		from MPSAppt.handlers import completionHandler
		from MPSAppt.handlers import placeholderHandler
		from MPSAppt.handlers import dashboardHandler
		from MPSAppt.handlers import identifyCandidateHandler
		from MPSAppt.handlers import evalAddEditHandler
		from MPSAppt.handlers import evalDeleteDeclineReviewHandler
		from MPSAppt.handlers import evalSendHandler
		from MPSAppt.handlers import evalFileHandler
		from MPSAppt.handlers import evalFormHandler
		from MPSAppt.handlers import evalOverviewHandler
		from MPSAppt.handlers import evalImportHandler
		from MPSAppt.handlers import rosterHandler
		from MPSAppt.handlers import adminUserHandler
		from MPSAppt.handlers import adminDeptHandler
		from MPSAppt.handlers import adminTrackHandler
		from MPSAppt.handlers import adminTitleHandler
		from MPSAppt.handlers import adminBuildingHandler
		from MPSAppt.handlers import adminInternalEvalHandler
		from MPSAppt.handlers import adminLookupHandler
		from MPSAppt.handlers import adminUberQuestionHandler
		from MPSAppt.handlers import adminUberGroupHandler
		from MPSAppt.handlers import adminUberExportHandler
		from MPSAppt.handlers import adminWorkflowHandler
		from MPSAppt.handlers import qaHandler
		from MPSAppt.handlers import autofillHandler
		from MPSAppt.handlers import confirmTitleHandler
		from MPSAppt.handlers import jobPostingHandler
		from MPSAppt.handlers import viewAsCandidateHandler
		from MPSAppt.handlers import attestHandler
		from MPSAppt.handlers import visitorHandler
		from MPSAppt.handlers import npiHandler
		from MPSAppt.handlers import disclosureHandler
		from MPSAppt.handlers import backgroundCheckHandler
		from MPSAppt.handlers import uberFormHandler
		from MPSAppt.handlers import itemInjectionHandler
		from MPSAppt.handlers import jointPromotionHandler
		from MPSAppt.handlers import rosterEntryHandler
		from MPSAppt.handlers import reportingHandler
		from MPSAppt.handlers import serviceAndRankHandler
		from MPSAppt.handlers import fieldLevelRevisionsHandler

		urlMappings = []
		figgerUtils = configUtils.ConfigUtilities()
		figgerUtils.addURLMappingsFromModule(mainHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(positionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(personHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(jobActionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(fileUploadHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(packetDownloadHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(approvalHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(completionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(placeholderHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(identifyCandidateHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalAddEditHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalDeleteDeclineReviewHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalSendHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalFileHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalFormHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalOverviewHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(evalImportHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(rosterHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(dashboardHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminUserHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminDeptHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminTrackHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminTitleHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminBuildingHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminInternalEvalHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminLookupHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminUberQuestionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminUberGroupHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminUberExportHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminWorkflowHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(qaHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(autofillHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(confirmTitleHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(jobPostingHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(viewAsCandidateHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(attestHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(visitorHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(npiHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(disclosureHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(backgroundCheckHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(uberFormHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(itemInjectionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(jointPromotionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(rosterEntryHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(reportingHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(serviceAndRankHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(fieldLevelRevisionsHandler, urlMappings)

		import MPSCore.utilities.mpsTemplateLoader as loaderUtils
		mpsLoader = loaderUtils.MPSTemplateLoader()
		mpsLoader.addDirectory(os.path.join(srcRootFolderPath, "MPSAppt", "html"))
		mpsLoader.addDirectory(env.getSrcCoreHtmlFolderPath())
		env.setTemplateLoader(mpsLoader)
		isDebug = True if env.getEnvCode() == 'dev' else False
		application = tornado.web.Application(urlMappings, template_loader=mpsLoader, debug=isDebug, xsrf_cookies=True, cookie_secret=env.generateUniqueId())

		#   Run the web server on specified port.
		import tornado.ioloop
		application.listen(env.getListenPort())

		#   Run the backgroundCheckCompletion periodic task to update outstanding Background Check requests, if requested.
		if env.getBackgroundCheckCompletionOn():
			intervalMinutes = env.getBackgroundCheckIntervalMinutes()
			import MPSAppt.core.backgroundCheck.backgroundCheckTask as bcTask
			checker = tornado.ioloop.PeriodicCallback(bcTask.BackgroundCheckTask, intervalMinutes * 60 * 1000)
			checker.start()
			logger.info("MPSAppt Background Check Task scheduled at %i minute intervals" % intervalMinutes)

		#   Run the jobActionCompletion daily task to complete scheduled Job Actions, if requested.
		if env.getJobActionCompletionOn():
			import MPSCore.utilities.mpsDailyCallback as dailyCallback
			import MPSAppt.core.jobActionCompleter as jaCompleter
			completer = dailyCallback.MPSDailyCallback(jaCompleter.JobActionCompletionTask, (2 * 60), _descr='MPSAppt Job Action Completion Task')    # daily at 2:00 AM
			completer.start()

		#   Run the reportingArchiveWiper periodic task to delete outdated reports, if requested.
		if env.getReportingCleanupOn():
			import MPSCore.utilities.mpsDailyCallback as dailyCallback
			import MPSAppt.core.reportingArchiveWiper as raWiper
			wiper = dailyCallback.MPSDailyCallback(raWiper.ReportingArchiveWiperTask, (5 * 60), _descr='MPSAppt Reporting Cleanup Task')    # daily at 5:00 AM
			wiper.start()

		tornado.ioloop.IOLoop.instance().start()

	def resolveFilePath(self, _srcRootFolderPath, _filePath):
		filePath = _filePath
		if not filePath.startswith('/'):
			filePath = os.path.join(_srcRootFolderPath, filePath)
		return filePath

	def loadConfig(self, _env, _configFilePath):
		configDict = {
			"environment": "{env}",
			"listenport": 8004,
			"loggingconfig": "config/{env}/MPSAppt/logging.conf",
			"wkhtmltopdfbinpath": "/usr/local/bin/wkhtmltopdf",
			"pdftkbinpath":"/opt/pdflabs/pdftk/bin/pdftk",
			"skinfolderpath": "/usr/local/mps",
			"email": "off",
			"emailto": [],
			"jobcompletiontask": "off",
			"reportingcleanuptask": "off",
			"backgroundchecktask": "off",
			"backgroundcheckintervalminutes": "120",
		}
		for key in configDict.keys():
			if type(configDict[key]) == str:
				configDict[key] = configDict[key].replace('{env}', _env)
		return configUtils.ConfigUtilities().loadConfig(_configFilePath, configDict)

if __name__ == '__main__':
	mpsAppt = MPSAppt()
	parser = mpsAppt.get_parser()
	(options, args) = parser.parse_args()
	mpsAppt.run(options, args)
