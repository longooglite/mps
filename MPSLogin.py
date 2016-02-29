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
import MPSLogin.utilities.environmentUtils as envUtils

#   Runs the MPS Login application.

class MPSLogin():

	def get_parser(self):
		parser = optparse.OptionParser(description='MPS Login application')
		parser.add_option('-e', '--env', dest='env',
			default='dev',
			help='environment (default=dev)')
		parser.add_option('-f', '--file', dest='file',
			default='config/{env}/MPSLogin/config.json',
			help='json config file (default=config/{env}/MPSLogin/config.json)')
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
		env.setAuthServiceUrl(configDict['authserviceurl'])
		env.setSrcRootFolderPath(srcRootFolderPath)
		env.setWkhtmltopdfBinPath(configDict['wkhtmltopdfbinpath'])
		env.setPDFtkBinPath(configDict['pdftkbinpath'])
		env.setSkinFolderPath(configDict['skinfolderpath'])
		env.setEmailOn(configDict['email'])
		env.setEmailTo(configDict['emailto'])

		#   Initialize logging.
		logUtils.initLogging(self.resolveFilePath(srcRootFolderPath, configDict['loggingconfig']))
		logger = logging.getLogger(__name__)
		logger.info("MPSLogin started")
		logger.info("MPSLogin CoreEnvironment '%s'" % str(env.getEnvCode()))
		logger.info("MPSLogin Using MPS Auth Service at '%s'" % str(env.getAuthServiceUrl()))
		logger.info("MPSLogin Listening on port '%s'" % str(env.getListenPort()))
		logger.info("MPSLogin Email '%s'" % str(env.getEmailOn()))
		logger.info("MPSLogin EmailTo Override '%s'" % str(env.getEmailTo()))
		if os.environ.has_key('CAR_EMAILTO'):
			logger.info("MPSLogin EmailTo Environment Override '%s'" % str(os.environ['CAR_EMAILTO']))
		if env.getAvoidNetwork():
			logger.info("MPSLogin Internet access is not available")

		#   Set up the Service request handlers.
		import tornado.web
		from MPSLogin.handlers import loginHandlers
		from MPSLogin.handlers import shibbolethHandler

		urlMappings = []
		figgerUtils = configUtils.ConfigUtilities()
		figgerUtils.addURLMappingsFromModule(loginHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(shibbolethHandler, urlMappings)

		import MPSCore.utilities.mpsTemplateLoader as loaderUtils
		mpsLoader = loaderUtils.MPSTemplateLoader()
		mpsLoader.addDirectory(os.path.join(srcRootFolderPath, "MPSLogin", "html"))
		mpsLoader.addDirectory(env.getSrcCoreHtmlFolderPath())
		env.setTemplateLoader(mpsLoader)
		isDebug = True if env.getEnvCode() == 'dev' else False
		application = tornado.web.Application(urlMappings, template_loader=mpsLoader, debug=isDebug)

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
			"listenport": 8001,
			"authserviceurl": "http://localhost:9000",
			"loggingconfig": "config/{env}/MPSLogin/logging.conf",
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
	mpsLogin = MPSLogin()
	parser = mpsLogin.get_parser()
	(options, args) = parser.parse_args()
	mpsLogin.run(options, args)
