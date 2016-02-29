# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import optparse
import sys
import urllib2
import base64
import json
import datetime
import os
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)
import MPSCore.utilities.dbConnectionParms as dbConnParms
from MPSCore.utilities import migrationFramework as MF

usage = '''
Schema and data migrator for MPS.

Arguments:
1) '%s': Create new migration file.
2) '%s': Perform migration on a single database instance or all database instances.

Example for creating a new migration file:
python migrate %s -n my_mps_migration

Example for migrating a single database instance:
python migrate %s -d mpsdev

Example for migrating all database instances from router connection strings:
python migrate -s all
''' % (MF.kCommands[0], MF.kCommands[1], MF.kCommands[0], MF.kCommands[1])


class Migrator(MF.AbstractMigrator):
	def __init__(self, _options, _connectionParms=[], isAuth = False):
		MF.AbstractMigrator.__init__(self,options,_connectionParms,isAuth)
		self.connectionParms = _connectionParms


	#	Override delegate to handle router-based migrations.
	
	def migrateDelegate(self):
		if self.options.scope == 'all':
			self.logMessage("Preparing to migrate multiple instances")
			self.logMessage("-- the migration of multiple instances not implemented --")
		else:
			self.logMessage("Preparing to migrate %s" % (self.options.dbname))
			self.migrateSingleInstance(self.connectionParms)


class MigrationInterface:
	DESCR = '''Migration utility for MPS application data'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsauth', help='database name (default=mpsauth')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option("-n", "--name", dest="name", default="",help="optional descriptive suffix for migration file")
		parser.add_option("-v", "--verbose", dest="verbose", default=1, help="verbose output. 1 = on, 0 = off.")
		parser.add_option("-s", "--scope", dest="scope", default='one', help="migrate one instance, or all instances")
		return parser

	def getConnectionParms(self,options):
		if options.scope == 'one':
			return dbConnParms.DbConnectionParms(options.host, options.port, options.dbname, options.user, options.password)
		else:
			return []

	def run(self, options, args):
		try:
			isAuth = True
			connectionParms = self.getConnectionParms(options)
			migrator = Migrator(options,connectionParms,isAuth)
			if args[0] == MF.kCommands[0]:
				migrator.createMigration()
			else:
				migrator.migrate()
		except Exception, e:
			print e.message

if __name__ == '__main__':
	migrationInterface = MigrationInterface()
	parser = migrationInterface.get_parser()
	(options, args) = parser.parse_args()
	migrationInterface.run(options, args)
