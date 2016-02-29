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
import MPSAdmin.utilities.environmentUtils as envUtils

#   Runs the MPS Administration application.

class MPSAdmin():

	def get_parser(self):
		parser = optparse.OptionParser(description='MPS Administration application')
		parser.add_option('-e', '--env', dest='env',
			default='dev',
			help='environment (default=dev)')
		parser.add_option('-f', '--file', dest='file',
			default='config/{env}/MPSAdmin/config.json',
			help='json config file (default=config/{env}/MPSAdmin/config.json)')
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
		env.setDropdbBinPath(configDict['dropdbbinpath'])
		env.setCreatedbBinPath(configDict['createdbbinpath'])
		env.setPgdumpBinPath(configDict['pgdumpbinpath'])
		env.setPsqlBinPath(configDict['psqlbinpath'])
		env.setDumpFolderPath(configDict['dumpfolderpath'])
		env.setSkinFolderPath(configDict['skinfolderpath'])
		env.setEmailOn(configDict['email'])
		env.setEmailTo(configDict['emailto'])


		#   Initialize logging.
		logUtils.initLogging(self.resolveFilePath(srcRootFolderPath, configDict['loggingconfig']))
		logger = logging.getLogger(__name__)
		logger.info("MPSAdmin started")
		logger.info("MPSAdmin CoreEnvironment '%s'" % str(env.getEnvCode()))
		logger.info("MPSAdmin Listening on port '%s'" % str(env.getListenPort()))
		logger.info("MPSAdmin Email '%s'" % str(env.getEmailOn()))
		logger.info("MPSAdmin EmailTo Override '%s'" % str(env.getEmailTo()))
		if os.environ.has_key('CAR_EMAILTO'):
			logger.info("MPSAdmin EmailTo Environment Override '%s'" % str(os.environ['CAR_EMAILTO']))
		if env.getAvoidNetwork():
			logger.info("MPSAdmin Internet access is not available")

		#   Set up the Service request handlers.
		import tornado.web
		from MPSAdmin.handlers import mainHandler
		from MPSAdmin.handlers import siteHandler
		from MPSAdmin.handlers import communityHandler
		from MPSAdmin.handlers import prefHandler
		from MPSAdmin.handlers import roleHandler
		from MPSAdmin.handlers import userHandler
		from MPSAdmin.handlers import sessionHandler
		from MPSAdmin.handlers import cacheHandler
		from MPSAdmin.handlers import databaseHandler

		urlMappings = []
		figgerUtils = configUtils.ConfigUtilities()
		figgerUtils.addURLMappingsFromModule(mainHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(siteHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(communityHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(prefHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(roleHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(userHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(sessionHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(cacheHandler, urlMappings)
		figgerUtils.addURLMappingsFromModule(databaseHandler, urlMappings)

		import MPSCore.utilities.mpsTemplateLoader as loaderUtils
		mpsLoader = loaderUtils.MPSTemplateLoader()
		mpsLoader.addDirectory(os.path.join(srcRootFolderPath, "MPSAdmin", "html"))
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
			"listenport": 8003,
			"loggingconfig": "config/{env}/MPSAdmin/logging.conf",
			"wkhtmltopdfbinpath": "/usr/local/bin/wkhtmltopdf",
			"pdftkbinpath":"/opt/pdflabs/pdftk/bin/pdftk",
			"dropdbbinpath": "/usr/local/bin/dropdb",
			"createdbbinpath": "/usr/local/bin/createdb",
			"pgdumpbinpath": "/usr/local/bin/pg_dump",
			"psqlbinpath": "/usr/local/bin/psql",
			"dumpfolderpath": "/usr/local/mpsDatabases",
			"skinfolderpath": "/usr/local/mps",
			"email": "off",
			"emailto": [],
		}
		for key in configDict.keys():
			if type(configDict[key]) == str:
				configDict[key] = configDict[key].replace('{env}', _env)
		return configUtils.ConfigUtilities().loadConfig(_configFilePath, configDict)

if __name__ == '__main__':
	mpsAdmin = MPSAdmin()
	parser = mpsAdmin.get_parser()
	(options, args) = parser.parse_args()
	mpsAdmin.run(options, args)
