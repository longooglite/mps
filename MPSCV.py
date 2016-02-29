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
import MPSCV.utilities.environmentUtils as envUtils

#   Runs the MPS CV application.

class MPSCV():

	def get_parser(self):
		parser = optparse.OptionParser(description='MPS CV application')
		parser.add_option('-e', '--env', dest='env',
			default='dev',
			help='environment (default=dev)')
		parser.add_option('-f', '--file', dest='file',
			default='config/{env}/MPSCV/config.json',
			help='json config file (default=config/{env}/MPSCV/config.json)')
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


		#   Initialize logging.
		logUtils.initLogging(self.resolveFilePath(srcRootFolderPath, configDict['loggingconfig']))
		logger = logging.getLogger(__name__)
		logger.info("MPSCV started")
		logger.info("MPSCV CoreEnvironment '%s'" % str(env.getEnvCode()))
		logger.info("MPSCV Listening on port '%s'" % str(env.getListenPort()))
		logger.info("MPSCV Email '%s'" % str(env.getEmailOn()))
		logger.info("MPSCV EmailTo Override '%s'" % str(env.getEmailTo()))
		if os.environ.has_key('CAR_EMAILTO'):
			logger.info("MPSCV EmailTo Environment Override '%s'" % str(os.environ['CAR_EMAILTO']))
		if env.getAvoidNetwork():
			logger.info("MPSCV Internet access is not available")

		#   Set up the Service request handlers.
		import tornado.web
		from MPSCV.handlers import mainHandler
		from MPSCV.handlers import categoryHandler
		from MPSCV.handlers import detailHandler
		from MPSCV.handlers import proxyHandler
		from MPSCV.handlers import printCVHandler
		from MPSCV.handlers import importHandler
		from MPSCV.handlers import exportHandler
		from MPSCV.handlers import adminHandler
		from MPSCV.handlers import pubMedHandler


		urlMappings = []
		figgerUtils = configUtils.ConfigUtilities()
		figgerUtils.addURLMappingsFromModule(mainHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(categoryHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(detailHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(proxyHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(printCVHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(importHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(exportHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(adminHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(pubMedHandler, urlMappings)

		import MPSCore.utilities.mpsTemplateLoader as loaderUtils
		mpsLoader = loaderUtils.MPSTemplateLoader()
		mpsLoader.addDirectory(os.path.join(srcRootFolderPath, "MPSCV", "html"))
		mpsLoader.addDirectory(env.getSrcCoreHtmlFolderPath())
		env.setTemplateLoader(mpsLoader)
		isDebug = True if env.getEnvCode() == 'dev' else False
		application = tornado.web.Application(urlMappings, template_loader=mpsLoader, debug=isDebug, xsrf_cookies=True, cookie_secret=env.generateUniqueId())

		#   Run the web server on specified port.
		import tornado.ioloop
		application.listen(env.getListenPort())
		tornado.ioloop.IOLoop.instance().start()

	def resolveFilePath(self, _srcRootFolderPath, _filePath):
		filePath = _filePath
		if not filePath.startswith('/'):
			filePath = os.path.join(_srcRootFolderPath, filePath)
		return filePath

	def loadConfig(self, _env, _configFilePath):
		configDict = {
			"environment": "{env}",
			"listenport": 8002,
			"loggingconfig": "config/{env}/MPSCV/logging.conf",
			"wkhtmltopdfbinpath": "/usr/local/bin/wkhtmltopdf",
			"pdftkbinpath":"/opt/pdflabs/pdftk/bin/pdftk",
			"skinfolderpath": "/usr/local/mps",
			"email": "off",
			"emailto": [],
		}
		for key in configDict.keys():
			if type(configDict[key]) == str:
				configDict[key] = configDict[key].replace('{env}', _env)
		return configUtils.ConfigUtilities().loadConfig(_configFilePath, configDict)

if __name__ == '__main__':
	mpsCV = MPSCV()
	parser = mpsCV.get_parser()
	(options, args) = parser.parse_args()
	mpsCV.run(options, args)
