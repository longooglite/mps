# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
dbBackup.py
'''

import sys
import os

sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)
from logging.handlers import RotatingFileHandler
import socket
import logging
import logging.config
import optparse
import commands
import datetime
import time
import glob
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.emailService as emailSvc

kOneMeg = 1024 * 1024

class DBBackup(object):
	def __init__(self, options=None, args=None):
		self.rootpath = '/'
		self.keepdays = 15
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'postgres'
		self.user = 'mps'
		self.password = 'mps'
		self.emailAddresses = ''
		self.backupReport = ''
		self.beginSpace = 0
		self.endSpace = 0
		self.hasException = False

		if options:
			if options.rootpath: self.rootpath = options.rootpath
			if options.keepdays: self.keepdays = int(options.keepdays)
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.emailAddresses: self.emailAddresses = options.emailAddresses

	def process(self):
		try:
			self.dbl(self.disk_usage('/',True))
			self.connectToDatabase()
			dbNames = self.getDBNames()
			self.dbl("Start Backup")
			for dbname in dbNames:
				try:
					dbPath = os.path.join(self.rootpath,dbname) + os.sep
					if not os.path.exists(dbPath):
						os.makedirs(dbPath)
					dbbackupname = dbname + '_' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
					dumpName = dbbackupname
					dumpPath = dbPath + dumpName
					dumpCommand = "pg_dump %s -U mps  > %s" % (dbname,dumpPath)
					self.dbl("dumping %s to %s" % (dbname,dumpPath))
					result = commands.getoutput(dumpCommand)
					if result == '':
						self.dbl("success")
					else:
						self.dbl(result)
					zipCommand = "gzip %s" % (dumpPath)
					self.dbl("zipping %s to %s.gz" % (dbbackupname,dumpPath))
					result = commands.getoutput(zipCommand)
					if result == '':
						self.dbl("success")
					else:
						self.dbl(result)
					self.purge(dbPath)
				except Exception,e:
					self.hasException = True
					self.dbl("<b>Exception on backup %s</b>" % (e.message))
		except Exception,e:
			self.dbl("<b>Exception on backup %s</b>" % (e.message))
			self.hasException = True

		finally:
			self.dbl("End Backup")
			self.shutdown()
			self.dbl(self.disk_usage('/'))
			self.dbl("Space consumed by backup: %i megabyte(s)" % (self.beginSpace - self.endSpace))
			self.sendBackupReport()

	def sendBackupReport(self):
		emailer = emailSvc.EmailService(None,None,_username='daemon',_now=envUtils.getEnvironment().formatUTCDate())
		backupHTML = self.getBackupBody()
		subjectLine = 'Backup Report for %s - (status = success)' % (socket.gethostname())
		if self.hasException:
			subjectLine = 'Backup Report for %s - (status = ERRORS)' % (socket.gethostname())
		emailer.prepareAndSendAdministrativeEmail(self.emailAddresses,subjectLine,backupHTML)

	def getBackupBody(self):
		body = '''<!DOCTYPE html><html lang="en"><head></head><body><table>''' + self.backupReport + '''</table></body></html>'''
		return body

	def disk_usage(self,path,begin=False):
		st = os.statvfs(path)
		free = st.f_bavail * st.f_frsize/kOneMeg
		total = st.f_blocks * st.f_frsize/kOneMeg
		used = ((st.f_blocks - st.f_bfree) * st.f_frsize)/kOneMeg
		if begin:
			self.beginSpace = free
		else:
			self.endSpace = free
		diskUsage = "Disk usage in megabytes (Free: %i, Total: %i, Used: %i)" % (free,total,used)
		return diskUsage

	def purge(self,search_dir):
		self.dbl("Purging %s" % (search_dir))
		files = filter(os.path.isfile, glob.glob(search_dir + "*"))
		files.sort(key=lambda x: os.path.getmtime(x))
		try:
			for file in files:
				updatedString = time.ctime(os.path.getmtime(file))
				updatedDate = datetime.datetime.strptime(updatedString,'%a %b %d %H:%M:%S %Y')
				expired, days = dateUtils.datePlusDaysExceedsNow(updatedDate.strftime('%Y-%m-%d'),self.keepdays)
				if expired:
					self.dbl("Purging %s" % (file))
					os.remove(file)
					self.dbl("success")
		except Exception,e:
			self.hasException = True
			self.dbl("<b>Exception on purge %s</b>" % (e.message))
			pass

	def getDBNames(self):
		invalidEntries = ['postgres','template1','template0']
		sql = "select datname from pg_database;"
		qry = self.db.executeSQLQuery(sql,args)
		processList = []
		for dbentry in qry:
			if dbentry.get('datname','') not in invalidEntries:
				processList.append(dbentry.get('datname',''))
		return processList


	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

	def shutdown(self):
		self.db.closeMpsConnection()

	def dbl(self,logmsg):
		try:
			#locate path for debug log in prefs file
			logfilePath=os.path.join(self.rootpath,'debugLogs')
			fileName = 'debugLog'
			logSize = 5000000
			logCount = 5
			#if path does not exist, create it
			if not os.path.exists(logfilePath):
				os.makedirs(logfilePath)
			if os.path.exists(logfilePath):
				env = envUtils.getEnvironment()
				self.backupReport += "<tr><td>%s - %s</td></tr>" % (env.localizeUTCDate(env.formatUTCDate()), logmsg)
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


class DBBackupInterface:
	DESCR = '''DB Backup'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='postgres', help='database name (default=postgres')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-e', '--emailAddresses', dest='emailAddresses', default='eric.paul@gomountainpass.com,greg.poth@gomountainpass.com', help='administrative email addresses that receive backup report')

		parser.add_option('-k', '--keepdays', dest='keepdays', default='15', help='number of days to keep backup')
		parser.add_option('-r', '--rootpath', dest='rootpath', default='/home/mpsadmin/mpsBackups', help='root backup folder. All files will be placed in named subfolders in this directory')
		return parser

	def run(self, options, args):
		dbBackup = None
		try:
			dbBackup = DBBackup(options, args)
			dbBackup.process()
		except Exception, e:
			print e.message


if __name__ == '__main__':
	import MPSCore.utilities.sqlUtilities as sqlUtilities
	dbBackupInterface = DBBackupInterface()
	parser = dbBackupInterface.get_parser()
	(options, args) = parser.parse_args()
	dbBackupInterface.run(options, args)
	sys.exit(0)