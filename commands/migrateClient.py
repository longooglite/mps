# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import optparse
import sys
import tornado.escape
import tornado.httpclient
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
python migrateClient.py %s -n my_mps_migration

Example for migrating a single database instance:
python migrateClient.py %s -d mpsdev

Example for migrating all database instances on server:
python migrateClient.py -s all''' % (MF.kCommands[0], MF.kCommands[1], MF.kCommands[0], MF.kCommands[1])


class Migrator(MF.AbstractMigrator):
	def __init__(self, _options, _connectionParms=None, isAuth = False):
		MF.AbstractMigrator.__init__(self,_options,_connectionParms,isAuth)
		self.connectionParms = _connectionParms


	#	Override delegate to handle router-based migrations.
	
	def migrateDelegate(self):
		result = (-1,'Unknown Error')
		try:
			if self.options.scope == 'all':
				self.logMessage("Preparing to migrate multiple instances")
				for each in self.connectionParms:
					try:
						result = self.migrateSingleInstance(each)
					except Exception,e:
						return (-1,e.message)
			else:
				self.logMessage("Preparing to migrate %s" % (self.options.dbname))
				result = self.migrateSingleInstance(self.connectionParms)
		except Exception,e:
			return (-1,e.message)
		finally:
			return result

class MigrationInterface:
	DESCR = usage

	def __init__(self):
		self.options = None
		self.args = None

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-a', '--authport', dest='authport', default=9001, help='database port (default=9001)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
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
			return self.getConnectionParmsFromAuth()

	def getConnectionParmsFromAuth(self):
		payload = {}
		sites = self.postToAuthSvc("/sitelistbypass", {})
		connectionParms = []
		for site in sites:
			payload['profileSite'] = site.get('code','')
			profile = self.postToAuthSvc("/siteprofiledetailbypass", payload)
			connectionParms.append(dbConnParms.DbConnectionParms(profile.get('sitePreferences',{}).get('dbhost',''),
			                                                     profile.get('sitePreferences',{}).get('dbport',''),
			                                                     profile.get('sitePreferences',{}).get('dbname',''),
			                                                     profile.get('sitePreferences',{}).get('dbusername',''),
			                                                     profile.get('sitePreferences',{}).get('dbpassword','')))
		return connectionParms

	def postToAuthSvc(self, _uri, _unJsonifiedPayload):
		response = ""
		authserviceurl = "http://localhost:%s" % (str(self.options.authport))
		http_client = tornado.httpclient.HTTPClient()
		try:
			jsonResponse = http_client.fetch(
				authserviceurl + _uri,
				method='POST',
				headers = {'Content-Type':'application/json'},
				body=tornado.escape.json_encode(_unJsonifiedPayload))
			response = tornado.escape.json_decode(jsonResponse.body)
		finally:
			http_client.close()

		return response

	def run(self, options, args):
		self.options = options
		self.args = args
		result = (-1,'Unknown Error')
		try:
			isAuth = False
			connectionParms = self.getConnectionParms(options)
			migrator = Migrator(options,connectionParms,isAuth)

			if args and args[0] == MF.kCommands[0]:
				migrator.createMigration()
				result = (0,"")
			else:
				result = migrator.migrate()
		except Exception, e:
			print e.message
			result = (-1,e.message)
		finally:
			return result

def main():
	result = (-1,'Unknown Error')
	try:
		migrationInterface = MigrationInterface()
		parser = migrationInterface.get_parser()
		(options, args) = parser.parse_args()
		result = migrationInterface.run(options, args)
	except Exception,e:
		result = (-1,e.message)
	finally:
		if result[0] > -1:
			print "SUCCESS"
		else:
			print 'ERROR - ' + result[1]
			sys.exit(-999)
		return result

if __name__ == '__main__':
	result = main()
