# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#
#	migrationFramework.py
#

import commands
import datetime
import os
import sys
import MPSCore.utilities.sqlUtilities as sqlUtilities

kClientPath = "car%sdata%smigrations%sclient%s" % (os.sep,os.sep,os.sep,os.sep)
kAuthPath = "car%sdata%smigrations%sauth%s" % (os.sep,os.sep,os.sep,os.sep)
sys.path.append(os.path.abspath(__file__).split("car")[0] + kClientPath)
sys.path.append(os.path.abspath(__file__).split("car")[0] + kAuthPath)

kCommands = ['createmigration','migrate']

class AbstractMigrator():
	def __init__(self,_options,_connectionParms,_isAuth):
		self.isAuth = _isAuth
		self.options = _options
		self.verbose = self.options.verbose == 1
		self.descriptor = ''
		self.connectionParms = _connectionParms

	def migrate(self):
		self.logProcessStart()
		result = (0,"")
		try:
			result = self.migrateDelegate()
		except Exception,e:
			self.logException(e)
			result = (-1,e.message)
		finally:
			self.logProcessEnd()
			return result

	def migrateDelegate(self):
		self.logMessageDatabase(("Preparing to migrate %s" % self.options.dbname), self.options.dbname)
		self.migrateSingleInstance(self.connectionParms)

	def migrateSingleInstance(self, connectionParms):
		connection = sqlUtilities.SqlUtilities(connectionParms)
		self.logMessage("Beginning migration for %s" % (connectionParms.dbname))
		scriptName = ''
		result = (0,"")
		try:
			count = 0
			fileListing = self.getFileListing()
			if fileListing:
				for f in fileListing:
					scriptName = self.getScriptName(f)
					if not self.alreadyApplied(connection, scriptName):
						count += 1
						result = self.applyMigration(connection, scriptName)
						if result[0] < 0:
							break
						self.markAsApplied(connection, scriptName)
					if count > 0:
						self.logMessageDatabase(("%s migration(s) applied" % count), str(connection.dbConnectionParms.dbname))
		except Exception,e:
			self.logException(e,' | %s - An error ocurred while processing %s.' % (connection.dbConnectionParms.dbname, scriptName))
		finally:
			if connection:
				connection.closeMpsConnection()
			return result

	def applyMigration(self, _connection, _script):
		result = (-1,'Unknown Error')
		try:
			self.logMessageDatabase("Applying migration %s" % _script, _connection.dbConnectionParms.dbname)
			importString = "from %s import Migrator" % (_script[0:len(_script)-3])
			exec importString

			mInstance = Migrator(_connection)
			result = mInstance.migrate()

			self.logMessageDatabase('result: %s %s' % (result[0],result[1]),str(_connection.dbConnectionParms.dbname))
		except Exception,e:
			self.logException(e, ' | %s - An error ocurred while processing %s.' % (str(_connection.dbConnectionParms.dbname), _script))
		finally:
			return result

	#	Tracking which migrations have been applied.

	def alreadyApplied(self, _connection, _scriptName):

		#	Check that the migration history table exists. If not, assume this is
		#	the initial migration, and that the migration will create the appropriate
		#	migration history table.

		try:
			sql = "SELECT COUNT(*) AS count FROM migration_history WHERE migration = %s AND applied = 't'"
			qry = _connection.executeSQLQuery(sql, (_scriptName,))
			return qry[0]['count']
		except Exception,e:
			self.logException(e,' | %s - An error occurred in method alreadyApplied()' % str(_connection.dbConnectionParms.dbname))

	def markAsApplied(self, _connection, _scriptName):
		try:
			self.logMessageDatabase(("Marking %s as applied" % _scriptName),_connection.dbConnectionParms.dbname)
			sqlStr = '''INSERT INTO migration_history (migration,applied) values (%s,%s)'''
			args = (_scriptName, True,)
			_connection.executeSQLCommand(sqlStr, args)
		except Exception,e:
			self.logException(e, ' | %s - An error occurred in method markAsApplied()' % str(_connection.dbConnectionParms.dbname))


	#	Miscellaneous

	def getFileListing(self):
		try:
			fileListing = []
			cmd = 'ls -l ' + os.path.join(self.getFilePath(), "migration_*.py")
			files = commands.getstatusoutput(cmd)
			if files[0] == 0:
				fileListing = files[1].split(chr(10))
			return fileListing
		except Exception,e:
			self.logException(e,'An error ocurred while retrieving file listing')

	def createMigration(self):
		try:
			fileName = self.getNewMigrationFileName()
			f = open(fileName,'w')
			f.write("import MPSCore.utilities.migrationFramework as MF\n")
			f.write("\n")
			f.write("class Migrator(MF.MigrationHelper):\n")
			f.write("\tdef __init__(self,_connection):\n")
			f.write("\t\tself.connection = _connection\n")
			f.write("\n")
			f.write("\tdef migrate(self):\n")
			f.write("\t\ttry:\n")
			f.write("\t\t\t#place migration code here\n")
			f.write('''\t\t\treturn 0,""\n''')
			f.write("\t\texcept Exception,e:\n")
			f.write("\t\t\tself.connection.executeSQLCommand('ROLLBACK',())\n")
			f.write("\t\t\treturn -1,e.message\n")
			f.write("\n")
			f.close()
			self.logMessage("Migration %s was created." % (fileName))
			return fileName #used by tests
		except Exception,e:
			self.logException(e,'Unable to create migration file')

	def getScriptName(self, fileName):
		scriptName = ''
		try:
			pathParts = fileName.split(os.path.sep)
			scriptName = pathParts[len(pathParts)-1]
			return scriptName
		except Exception,e:
			self.logException(e,'An error ocurred while getting script name %s.' % (scriptName))


	def getFilePath(self):
		if self.isAuth:
			return os.path.abspath(__file__).split("car")[0] + kAuthPath
		else:
			return os.path.abspath(__file__).split("car")[0] + kClientPath

	def getNewMigrationFileName(self):
		return self.getFilePath() + 'migration_' + str(datetime.datetime.now()).replace(' ','').replace('.','').replace('-','').replace(':','') + '_' + self.options.name + '.py'

	#	Logging

	def logMessage(self, _message):
		if self.shouldLogMessages() and _message:
			print "%s - %s" % (self.getLogTimestamp(), _message)

	def logMessageDatabase(self, _message, _dbname):
		if self.shouldLogMessages() and _message and _dbname:
			print "%s | %s - %s" % (self.getLogTimestamp(), _dbname, _message)

	def logProcessStart(self):
		self.processStart = self.getLogTimestamp()
		if self.shouldLogMessages():
			print "%s %s Migration process started" % (self.processStart, self.descriptor)

	def logProcessEnd(self):
		self.processEnd = self.getLogTimestamp()
		if self.shouldLogMessages():
			print "%s %s Migration process completed" % (self.processEnd, self.descriptor)
			print "%s %s Migration elapsed time: %s" % (self.processEnd, self.descriptor, str(self.processEnd - self.processStart))

	def logException(self, e, optionalMessage = None):
		self.verbose = True
		if optionalMessage is not None:
			self.logMessage(optionalMessage)
		self.logMessage("Exception: %s" % str(type(e)))
		for each in e.args:
			self.logMessage(each)
		try:
			self.logMessage(e.originalException.message)
		except:
			pass
		self.logMessage("Process aborted.")
		#on any exception, drop dead. It's best to not proceed in an unknown db state.
		sys.exit(1)

	def getLogTimestamp(self):
		return datetime.datetime.now()

	def shouldLogMessages(self):
		return self.verbose

class MigrationHelper():

	def tableExists(self,_dbConnection, tableName):
		qryStr = "SELECT count(*) as count FROM pg_stat_user_tables WHERE upper(relname) = %s "
		args = (tableName.upper(),)
		stat = _dbConnection.executeSQLQuery(qryStr,args)
		return stat[0]['count']

	def columnExists(self,_dbConnection, _tableName, _columnName):
		if not self.tableExists(_dbConnection,_tableName):
			return False
		sql = '''SELECT column_name FROM information_schema.columns WHERE upper(table_name)=%s AND upper(column_name)=%s'''
		results = _dbConnection.executeSQLQuery(sql, (_tableName.upper(), _columnName.upper()))
		return len(results) > 0


