# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
cactusLoad.py
'''

import sys
import os
import os.path
import csv
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import cStringIO
import logging
import logging.config
import optparse
import os
import time
import json
import glob
import datetime
import shutil
import MPSCore.core.constants
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.placeholderService as placeholderSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.stringUtilities as stringUtils
from logging.handlers import RotatingFileHandler

kDelimiter = "|"
kNumColumns = 3

class CactusLoad(object):
	logger = logging.getLogger(__name__)

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'umms'
		self.user = 'mps'
		self.password = 'mps'
		self.rootFolderPath = ''
		self.namePrefix = ''
		self.debug = ''
		self.db = None
		self.jobActionTypeCache = {}
		self.messageList = []

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.rootFolderPath: self.rootFolderPath = options.rootFolderPath
			if options.namePrefix: self.namePrefix = options.namePrefix
			if options.debug: self.debug = options.debug

		self.mapping = self.getMapping()

	def process(self):
		fullPath = ''
		allDone = False
		try:
			self.dbl('Begin Cactus Load')
			self.connectToDatabase()
			self.getJobActionTypeCache()
			self.dbl('Connection to database established')
			self.dbl('Loaded JobActionLog cache')

			self.purge('processed' + os.sep)
			while not allDone:
				fileData,fullPath = self.getSingleFileData()
				if not fileData:
					self.dbl('End Cactus Load')
					allDone = True
				else:
					self.dbl('Begin Processing %s' % (os.path.basename(fullPath)))
					self.processSingleFile(fileData)
					self.moveFile(fullPath,'processed')
		except Exception,e:
			try:
				#db connection throws an MPSException. Log and eat
				self.dbl(e.originalException[0])
			except:
				pass
			self.dbl('Exception Thrown while Processing %s' % (os.path.basename(fullPath)))
			try:
				self.dbl(e.message)
			except:
				pass
			self.moveFile(fullPath,'errors')

	def purge(self,subfolder):
		search_dir = os.path.join(self.rootFolderPath,subfolder)
		files = filter(os.path.isfile, glob.glob(search_dir + "*"))
		files.sort(key=lambda x: os.path.getmtime(x))
		try:
			for file in files:
				updatedString = time.ctime(os.path.getmtime(file))
				updatedDate = datetime.datetime.strptime(updatedString,'%a %b %d %H:%M:%S %Y')
				expired, days = dateUtils.datePlusDaysExceedsNow(updatedDate.strftime('%Y-%m-%d'),90)
				if expired:
					os.remove(file)
		except:
			pass

	def processSingleFile(self,fileData):
		for row in fileData:
			self.dbl(str(row))
			if self.rowValid(row):
				uniqname = row[0]
				aceId = row[1]
				value = row[2]
				self.processCactusStatusRow(uniqname,aceId,value)

	def processCactusStatusRow(self,uniqname,aceId,value):
		cactusUser = 'cactus'
		jaService = jobActionSvc.JobActionService(self.db)
		map = self.mapping.get(aceId,None)
		if map:
			jobActionType = self.jobActionTypeCache.get(map.get('workflow',None))
			if jobActionType:
				jobActionTypeId = jobActionType.get('id',-1)
				personId = self.getPersonId('default', uniqname)
				if personId:
					jobAction = jaService.getJobActionForPersonIdAndJobActionTypeId(personId,jobActionTypeId)
					if jobAction:
						if not jobAction.get('complete',True):
							workflow = workflowSvc.WorkflowService(self.db).getWorkflowForJobAction(jobAction, {})
							if workflow:
								container = workflow.getContainer(map.get('container',''))
								if container:
									container.loadInstance()
									now = envUtils.getEnvironment().formatUTCDate()
									jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, cactusUser)
									placeholderDict = {}
									placeholderDict['job_task_id'] = jobTask.get('id',None)
									placeholderDict['complete'] = stringUtils.interpretAsTrueFalse(value)
									placeholderDict['created'] = now if not jobTask.get('created','') else jobTask.get('created','')
									placeholderDict['updated'] = now
									placeholderDict['lastuser'] = cactusUser
									placeholderSvc.PlaceholderService(self.db).handleSubmit(jobAction, jobTask, placeholderDict, container, {}, now, cactusUser)
								else:
									self.dbl('Unable to find container %s' % (map.get('container','')))
							else:
								self.dbl('Unable to load workflow')
					else:
						self.dbl('Unable to find jobaction')
				else:
					self.dbl('Unable to find person')
			else:
				self.dbl('Unable to find job action type')
		else:
			self.dbl('Unable to find item in map for ace id %s' % (aceId))


	def rowValid(self,row):
		if not row:
			return False
		if row[0].strip().startswith("#"):
			return False
		if not len(row) == kNumColumns:
			self.dbl("invalid file format")
			return False
		return True

	def getPersonId(self, _community, _uniqname):
		person = personSvc.PersonService(self.db).getPersonByCommunityUserName(_community, _uniqname)
		if person:
			return person.get('id',None)
		return None

	def getJobActionTypeCache(self):
		cache = lookupTableSvc.getLookupTable(self.db, 'wf_job_action_type','code')
		self.jobActionTypeCache = cache

	def moveFile(self,filePath,targetDirectory):
		if self.debug <> 't':
			try:
				fileName = os.path.basename(filePath)
				parts = fileName.split('.')
				dtstamp = '_' + datetime.datetime.now().strftime('%H_%M_%S_%f')
				if len(parts) == 2:
					fileName = parts[0] + dtstamp + '.' +  parts[1]
				else:
					fileName = fileName + dtstamp

				targetPath = os.path.join(self.rootFolderPath,targetDirectory,fileName)
				shutil.move(filePath,targetPath)
			except Exception,e:
				self.dbl('Unable to move file')
				self.dbl(e.message)


	def getSingleFileData(self):
		f = None
		try:
			search_dir = os.path.join(self.rootFolderPath,'')
			files = filter(os.path.isfile, glob.glob(search_dir + "*"))
			files.sort(key=lambda x: os.path.getmtime(x))
			fullFilePath = ''
			for fullFilePath in files:
				filename = os.path.basename(fullFilePath)
				if filename.startswith(self.namePrefix):
					break
			if fullFilePath:
				f = open(fullFilePath, 'rU')
				data = list(csv.reader(f, delimiter=kDelimiter))
				f.close()
				return data,fullFilePath
			else:
				return None,None
		except Exception,e:
			self.dbl('Unable to read file')
			self.dbl(e.message)
			return None,None
		finally:
			if f <> None:
				f.close()

	def getMapping(self):
		f = None
		try:
			mappingFile = os.path.join(self.rootFolderPath, 'mappings/mappings.json')
			f = open(mappingFile,'r')
			jsonData = f.read()
			return json.loads(jsonData)
		except:
			self.dbl('Unable to open mapping')
			sys.exit(0)
		finally:
			if f:
				f.close()

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

	def shutdown(self):
		self.db.closeMpsConnection()

	def dbl(self,logmsg):
		try:
			#locate path for debug log in prefs file
			logfilePath=os.path.join(self.rootFolderPath,'errors')
			fileName = 'debugLog'
			logSize = 5000000
			logCount = 5
			#if path does not exist, create it
			if not os.path.exists(logfilePath):
				os.makedirs(logfilePath)
			if os.path.exists(logfilePath):
				logHandler = RotatingFileHandler(logfilePath + "/" + fileName,"a", logSize, logCount)
				logFormatter = logging.Formatter("%(asctime)s:%(message)s")
				logHandler.setFormatter(logFormatter)
				logger = logging.getLogger(__name__)
				logger.disabled = False
				logger.addHandler(logHandler)
				logger.setLevel(logging.DEBUG)
				logger.debug(logmsg)
				logHandler.flush()
				logHandler.close()
				logger.removeHandler(logHandler)
		except Exception:
			#if we can't write to the log for any reason, eat the error and continue.
			pass



class DataLoadInterface:
	DESCR = '''Data Load for Cactus. '''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='umms', help='database name (default=umms')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-r', '--rootFolderPath', dest='rootFolderPath', default='/Users/erpaul/Desktop/CACTUS', help='root path to cactus drop folder')
		parser.add_option('-n', '--namePrefix', dest='namePrefix', default='cactus', help='prefix for cactus files')
		parser.add_option('-x', '--debug', dest='debug', default='f', help="with debug on, don't move files")
		return parser

	def run(self, options, args):
		cactusLoad = None
		try:
			cactusLoad = CactusLoad(options, args)
			cactusLoad.process()
		except Exception, e:
			print e.message
		finally:
			if cactusLoad:
				cactusLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities
	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
	sys.exit(0)