# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import sys
import os
import os.path
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import cStringIO
import json
import logging
import logging.config
import optparse
import uuid

import tornado.escape
import tornado.httpclient

import MPSCore.core.constants
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCV.core.cvImporter as cvImputer


class CVBulkDataFabricator(object):
	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsdev'
		self.user = 'mps'
		self.password = 'mps'
		self.db = None

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			self.connectToDatabase()
			self.loadYerJSONs()
			self.establishSession()
			self.doImport()

		except Exception, e:
			print e.message

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

	def loadYerJSONs(self):
		self.margaret = json.loads(self.getFileContents('/Users/gpoth/Desktop/margaret.json'))
		self.chung = json.loads(self.getFileContents('/Users/gpoth/Desktop/chung.json'))

	def getFileContents(self, _filePath):
		f = None
		try:
			f = open(_filePath, 'r')
			return f.read()
		finally:
			if f:
				try: f.close()
				except Exception, e: pass

	def establishSession(self):
		payload = {}
		payload['site'] = 'dev'
		payload['username'] = 'greg'
		response = self.postToAuthSvc('/authenticate', payload)
		self.mpsid = response.get('mpsid', None)
		if not self.mpsid:
			print "Could not establish connection to Whoville"
			exit()

	def doImport(self):
		importer = cvImputer.CVImporter()

		loopMax = 125
		for i in range(0,loopMax):
			randomDude = uuid.uuid4().get_hex()
			self.doOneImport(importer, randomDude[0:8], self.margaret)
			self.doOneImport(importer, randomDude[8:16], self.chung)
			self.doOneImport(importer, randomDude[16:24], self.margaret)
			self.doOneImport(importer, randomDude[24:32], self.chung)

	def doOneImport(self, _importer, _username, _cvDict):
		self.addUser(_username)
		_importer.doImport(self.db, _cvDict, _overrideUsername=_username, _erasePubmedData=False)

	def addUser(self, _username):
		payload = {}
		payload['site'] = 'dev'
		payload['mpsid'] = self.mpsid
		payload['app'] = 'CV'
		payload['username'] = _username
		payload['first_name'] = _username
		payload['last_name'] = _username
		payload['active'] = 'true'
		payload['apps'] = ['CV']
		payload['roles'] = ['CV|cvUser']
		ignoredResponseDict = self.postToAuthSvc("/useradd", payload)

	def postToAuthSvc(self, _uri, _unJsonifiedPayload):
		response = ""
		authserviceurl = "http://localhost:9000"
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


class DataLoadInterface:
	DESCR = '''Bulk Data Fabricator for CV'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		return parser

	def run(self, options, args):
		cvLoad = None
		try:
			cvLoad = CVBulkDataFabricator(options, args)
			cvLoad.process()
		except Exception, e:
			print e.message
		finally:
			if cvLoad:
				cvLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
