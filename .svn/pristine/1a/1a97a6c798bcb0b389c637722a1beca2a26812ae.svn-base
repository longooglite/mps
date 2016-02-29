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
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.logUtils as logUtils
import MPSAuthSvc.utilities.environmentUtils as envUtils

#   Runs the MPS Authentication/Session/Configuration service.

class MPSAuthSvc():

	def get_parser(self):
		parser = optparse.OptionParser(description='MPS Authorization Service')
		parser.add_option('-e', '--env', dest='env',
			default='dev',
			help='environment (default=dev)')
		parser.add_option('-f', '--file', dest='file',
			default='config/{env}/MPSAuthSvc/config.json',
			help='json config file (default=config/{env}/MPSAuthSvc/config.json)')
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
		connectionParms = dbConnParms.DbConnectionParms(
			host=configDict['dbhost'],
			port=configDict['dbport'],
			dbname=configDict['dbname'],
			username=configDict['dbusername'],
			password=configDict['dbpassword']
		)
		env.setDbConnectionParms(connectionParms)
		env.setSrcRootFolderPath(srcRootFolderPath)
		env.setWkhtmltopdfBinPath(configDict['wkhtmltopdfbinpath'])
		env.setPDFtkBinPath(configDict['pdftkbinpath'])
		env.setSkinFolderPath(configDict['skinfolderpath'])
		env.setEmailOn(configDict['email'])
		env.setEmailTo(configDict['emailto'])


		#   Initialize logging.
		logUtils.initLogging(self.resolveFilePath(srcRootFolderPath, configDict['loggingconfig']))
		logger = logging.getLogger(__name__)
		logger.info("MPSAuthSvc started")
		logger.info("MPSAuthSvc CoreEnvironment '%s'" % str(env.getEnvCode()))
		logger.info("MPSAuthSvc Database '%s:%s %s'" % (str(connectionParms.getHost()), str(connectionParms.getPort()), str(connectionParms.getDbname())))
		logger.info("MPSAuthSvc Listening on port '%s'" % str(env.getListenPort()))
		logger.info("MPSAuthSvc Email '%s'" % str(env.getEmailOn()))
		logger.info("MPSAuthSvc EmailTo Override '%s'" % str(env.getEmailTo()))
		if os.environ.has_key('CAR_EMAILTO'):
			logger.info("MPSAuthSvc EmailTo Environment Override '%s'" % str(os.environ['CAR_EMAILTO']))
		if env.getAvoidNetwork():
			logger.info("MPSAuthSvc Internet access is not available")

		#   Set up the Service request handlers.
		import tornado.web
		from MPSAuthSvc.handlers import applicationHandlers
		from MPSAuthSvc.handlers import authenticationHandlers
		from MPSAuthSvc.handlers import cacheHandlers
		from MPSAuthSvc.handlers import messageHandlers
		from MPSAuthSvc.handlers import permissionHandlers
		from MPSAuthSvc.handlers import roleHandlers
		from MPSAuthSvc.handlers import sessionHandlers
		from MPSAuthSvc.handlers import siteHandlers
		from MPSAuthSvc.handlers import communityHandlers
		from MPSAuthSvc.handlers import userHandlers

		urlMappings = []
		figgerUtils = configUtils.ConfigUtilities()
		figgerUtils.addURLMappingsFromModule(applicationHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(authenticationHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(cacheHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(messageHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(permissionHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(roleHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(sessionHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(siteHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(communityHandlers, urlMappings)
		figgerUtils.addURLMappingsFromModule(userHandlers, urlMappings)
		isDebug = True if env.getEnvCode() == 'dev' else False
		application = tornado.web.Application(urlMappings, debug=isDebug)

		#   Run the web server on specified port.
		#   Run the sessionWatcher periodic task to enforce session timeouts.
		#   Run the workAreaWiper daily task to clean out the temporary file work area.
		import tornado.ioloop
		application.listen(env.getListenPort())

		import MPSAuthSvc.caches.sessionWatcher as sessionWatchr
		watcher = tornado.ioloop.PeriodicCallback(sessionWatchr.sessionWatcherTask, 60000)
		watcher.start()

		import MPSCore.utilities.mpsDailyCallback as dailyCallback
		import MPSAuthSvc.utilities.workAreaWiper as waWiper
		wiper = dailyCallback.MPSDailyCallback(waWiper.WorkAreaWiperTask, (4 * 60), _descr='MPSAuthSvc Work Area Wiper Task')    # daily at 4:00 AM
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
			"listenport": 9001,
			"dbhost": "localhost",
			"dbport": 5432,
			"dbname": "mpsauth",
			"dbusername": "mps",
			"dbpassword": "mps",
			"loggingconfig": "config/{env}/MPSAuthSvc/logging.conf",
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
	mpsAuthSvc = MPSAuthSvc()
	parser = mpsAuthSvc.get_parser()
	(options, args) = parser.parse_args()
	mpsAuthSvc.run(options, args)
