# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
cvRosterLoad.py

loads tab delimitted file - userid
'''

import sys
import os
import os.path
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import logging
import logging.config
import optparse
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.core.constants

import cStringIO


kGetApplicationId = '''SELECT id FROM application WHERE code = %s'''

kGetSiteId = '''SELECT id FROM site WHERE code = %s'''

kMPSUserInsert = '''INSERT INTO mpsuser (site_id,username,password,first_name,last_name,email,auth_override,active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
kMPSUserUpdate = '''UPDATE mpsuser SET password = %s,first_name = %s,last_name = %s,email = %s,auth_override = %s,active = %s WHERE site_id = %s and username = %s;'''
kGetUserId = '''SELECT id FROM mpsuser WHERE site_id = %s AND username = %s'''

kJoinUserAndApplicaton = '''INSERT INTO mpsuser_application (mpsuser_id,application_id,seqnbr) VALUES (%s,%s,%s);'''

kGetPermissionId = '''SELECT id FROM permission WHERE (site_code = %s OR site_code = '') AND application_id = %s AND code = %s;'''

kGetRoleId = '''SELECT id FROM ROLE WHERE site_id = %s and code = %s;'''

kJoinMPSUserRole = '''INSERT INTO mpsuser_role (mpsuser_id,role_id) VALUES (%s,%s)'''


class CVRosterLoad(object):

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsauth'
		self.user = 'mps'
		self.password = 'mps'

		self.db = None
		self.filePath = ''
		self.importData = []
		self.siteid = None
		self.messageList = []
		self.sitecode = ''
		self.applicationCode = "CV"
		self.cvRole = 'cvUser'

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.filepath: self.filePath = options.filepath
			if options.sitecode: self.sitecode = options.sitecode
		self.sitecode = self.sitecode.replace('-','_')

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		self.connectToDatabase()
		self.siteid = self.getSiteId()
		self.importData = self.getImportFileData()
		if self.importData <> None:
			self.updateMPSUsers()
			self.joinUsersToCVApplication()
			self.updateMPSUserRole()


	def getSiteId(self):
		sql = "SELECT id FROM site WHERE code = %s;"
		args = (self.sitecode,)
		qry = self.db.executeSQLQuery(sql,args)
		return qry[0]['id']


	def getImportFileData(self):
		try:
			f = open(self.filePath,'rU')
			returnVal = f.readlines()
			f.close()
			return returnVal
		except Exception,e:
			print "Unable to open file: %s" % (self.filePath)


	def updateMPSUsers(self):
		i = 0
		for rawRow in self.importData:
			i += 1
			if self.validRow(rawRow,i):
				if len(rawRow[0].strip()) > 0:
					self.upsertMPSUsers(rawRow.split('\t'))


	def upsertMPSUsers(self, userData):
		userid = userData[0].strip()
		password = ''
		first_name = userData[2].strip()
		last_name = userData[3].strip()
		email = userData[1]
		auth_override = ''
		activeBoolValue = True

		if self.db.getRowCount('mpsuser', "site_id = %i AND username = '%s'" % (self.siteid,userid)):
			self.db.executeSQLCommand(kMPSUserUpdate,(password,
			                                          first_name,
			                                          last_name,
			                                          email,
			                                          auth_override,
			                                          activeBoolValue,
			                                          self.siteid,
			                                          userid))
		else:
			self.db.executeSQLCommand(kMPSUserInsert,(self.siteid,
			                                          userid,
			                                          password,
			                                          first_name,
			                                          last_name,
			                                          email,
			                                          auth_override,
			                                          activeBoolValue))

	def joinUsersToCVApplication(self):
		i = 0
		for rawRow in self.importData:
			i += 1
			if self.validRow(rawRow,i):
				if len(rawRow[0].strip()) > 0:
					self.joinUserWithApplication(rawRow.split('\t'))

	def joinUserWithApplication(self,row):
		username = row[0].strip()
		userId = self.db.executeSQLQuery(kGetUserId,(self.siteid,username,))[0]['id']
		applicationId = self.db.executeSQLQuery(kGetApplicationId,(self.applicationCode,))[0]['id']
		if self.db.getRowCount('mpsuser_application','mpsuser_id = %i and application_id = %i' % (userId,applicationId)) == 0:
			self.db.executeSQLCommand(kJoinUserAndApplicaton,(userId,
			                                                  applicationId,
			                                                  1))

	def updateMPSUserRole(self):
		i = 0
		for rawRow in self.importData:
			i += 1
			if self.validRow(rawRow,i):
				if len(rawRow[0].strip()) > 0:
					self.upsertMPSUserRole(rawRow.split('\t'))

	def upsertMPSUserRole(self, row):
		username = row[0].strip()
		userid = self.db.executeSQLQuery(kGetUserId,(self.siteid,username,))
		role_id = self.db.executeSQLQuery(kGetRoleId,(self.siteid,self.cvRole,))
		if self.db.getRowCount('mpsuser_role','mpsuser_id = %i and role_id = %i' % (userid[0]['id'],role_id[0]['id'])) == 0:
			self.db.executeSQLCommand(kJoinMPSUserRole,(userid[0]['id'],role_id[0]['id']))


#########################################################################



	def validRow(self,row,rowNumber):
		if rowNumber == 1:
			return False
		if not len(row.strip()) > 0:
			return False
		if row.startswith("#"):
			return False
		return True

	def getImportFile(self, fileName):
		filepath = os.path.abspath(__file__).split("car")[0] + "car/data/authData/" + fileName
		f = open(filepath,'rU')
		return f,f.readlines()

	def getBool(self, instr):
		return stringUtils.interpretAsTrueFalse(instr)

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)


class DataLoadInterface:
	DESCR = ''''''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsauth', help='database name (default=mpsauth')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mpsauth)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-f', '--file', dest='filepath', default='', help='load file')
		parser.add_option('-s', '--sitecode', dest='sitecode', default='dev', help='sitecode')

		return parser


	def run(self, options, args):
		cvRosterLoad = None
		try:
			cvRosterLoad = CVRosterLoad(options, args)
			cvRosterLoad.process()
		except Exception, e:
			print e.message
		finally:
			if cvRosterLoad:
				cvRosterLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
