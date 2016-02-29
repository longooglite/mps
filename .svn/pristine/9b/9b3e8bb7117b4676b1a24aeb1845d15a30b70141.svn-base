# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
authLoad.py
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


kApplicationInsert = '''INSERT INTO application (code,descr,url) VALUES (%s, %s, %s);'''
kApplicationUpdate = '''UPDATE application SET descr = %s, url = %s WHERE code = %s;'''
kGetApplicationId = '''SELECT id FROM application WHERE code = %s'''

kSiteInsert = '''INSERT INTO site (code,descr,active_start,active_end) VALUES (%s, %s, %s, %s);'''
kSiteUpdate = '''UPDATE site SET descr = %s, active_start = %s, active_end = %s WHERE code = %s'''
kGetSiteId = '''SELECT id FROM site WHERE code = %s'''

kJoinSiteAndApplicaton = '''INSERT INTO site_application (site_id,application_id) VALUES (%s,%s);'''

kInsertPref = '''INSERT INTO site_preference (site_code,code,value) VALUES (%s,%s,%s);'''
kUpdatePref = '''UPDATE site_preference SET value = %s WHERE site_code = %s AND code = %s;'''

kMPSUserInsert = '''INSERT INTO mpsuser (site_id,community_id,username,password,first_name,last_name,email,auth_override,active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''
kMPSUserUpdate = '''UPDATE mpsuser SET password = %s,first_name = %s,last_name = %s,email = %s,auth_override = %s,active = %s WHERE site_id = %s AND community_id = %s AND username = %s;'''
kGetUserId = '''SELECT id FROM mpsuser WHERE site_id = %s AND community_id = %s AND username = %s'''

kJoinUserAndApplicaton = '''INSERT INTO mpsuser_application (mpsuser_id,application_id,seqnbr) VALUES ((SELECT id FROM mpsuser WHERE site_id = %s AND community_id = %s AND username = %s), (SELECT id FROM application WHERE code = %s), %s);'''
kJoinMPSUserRole = '''INSERT INTO mpsuser_role (mpsuser_id,role_id) VALUES (%s,%s)'''
kJoinRolePermission = '''INSERT INTO role_permission (role_id,permission_id) VALUES (%s,%s);;'''

kInsertPermission = '''INSERT INTO permission (site_code,application_id,code,descr) VALUES (%s, %s, %s, %s);'''
kUpdatePermission = '''UPDATE permission SET descr = %s WHERE site_code = %s AND application_id = %s AND code = %s;'''
kGetPermissionId = '''SELECT id FROM permission WHERE (site_code = %s OR site_code = '') AND application_id = %s AND code = %s;'''

kRoleInsert = '''INSERT INTO role (site_id,application_id,code,descr) VALUES (%s, %s, %s, %s);'''
kRoleUpdate = '''UPDATE role SET descr = %s WHERE site_id = %s AND application_id = %s AND code = %s;'''
kGetRoleId = '''SELECT id FROM ROLE WHERE site_id = %s and code = %s;'''

kCommunityInsert = '''INSERT INTO site_community (site_id,code,descr) VALUES (%s,%s,%s);'''
kCommunityUpdate = '''UPDATE site_community SET descr = %s WHERE site_id = %s AND code = %s;'''
kCommunityId = '''SELECT id FROM site_community WHERE site_id = %s AND code = %s'''


class AuthLoad(object):

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsauth'
		self.user = 'mps'
		self.password = 'mps'
		self.env = 'dev'
		self.sites = 'dev'

		self.db = None
		self.messageList = []

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.env: self.env = options.env
			if options.sites: self.sites = options.sites

	def shutdown(self):
		self.db.closeMpsConnection()


	# "Execution", such a cruel term

	def process(self):
		self.connectToDatabase()

		#   Environment-related data:
		#       Applications
		#       GLOBAL Site Preferences

		self.updateApplications()
		self.updateEnvironmentPrefs()

		#   Process each Site.

		for site in self.sites.split(','):
			self.curSite = site
			self.updateMPSAuth()

	def updateMPSAuth(self):
		self.updateSites()
		self.joinSitesWithApplications()
		self.updateSitePrefs()
		self.updateCommonCommunities()
		self.updateSiteSpecificCommunities()
		self.updateMPSUsers()
		self.joinMPSUsersToApplications()
		self.updateCommonPermissions()
		self.updateSiteSpecificPermissions()
		self.updateCommonRoles()
		self.updateSiteSpecificRoles()
		self.joinCommonRolesToPermissions()
		self.joinSiteSpecificRolesToPermissions()
		self.updateMPSUserRole()

	def updateMPSUserRole(self):
		file,rawData = self.getSiteImportFile('mpsuser_role.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertMPSUserRole(rawRow.split('|'))
		file.close()

	def upsertMPSUserRole(self, roleData):
		siteId = self.db.executeSQLQuery(kGetSiteId,(roleData[0].strip(),))
		communityCode = roleData[1].strip()
		if not communityCode:
			communityCode = 'default'
		communityId = self.db.executeSQLQuery(kCommunityId,(siteId[0]['id'], communityCode))[0]['id']
		userId = self.db.executeSQLQuery(kGetUserId,(siteId[0]['id'],communityId,roleData[2].strip(),))
		role_id = self.db.executeSQLQuery(kGetRoleId,(siteId[0]['id'], roleData[3].strip()))
		if self.db.getRowCount('mpsuser_role','mpsuser_id = %i and role_id = %i' % (userId[0]['id'],role_id[0]['id'])) == 0:
			self.db.executeSQLCommand(kJoinMPSUserRole,(userId[0]['id'],role_id[0]['id']))

	def joinCommonRolesToPermissions(self):
		file,rawData = self.getCommonSiteImportFile('common_role_permissions.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertRolePermission(rawRow.split('|'), _siteOverride = self.curSite)
		file.close()

	def joinSiteSpecificRolesToPermissions(self):
		file,rawData = self.getSiteImportFile('role_permission.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertRolePermission(rawRow.split('|'))
		file.close()

	def upsertRolePermission(self, roleData, _siteOverride=None):
		applicationId = self.db.executeSQLQuery(kGetApplicationId,(roleData[0].strip(),))
		siteCode = _siteOverride
		if not siteCode:
			siteCode = roleData[1].strip()
		siteId = self.db.executeSQLQuery(kGetSiteId,(siteCode,))
		role_id = self.db.executeSQLQuery(kGetRoleId,(siteId[0]['id'],
													  roleData[2].strip()))
		permission_id = self.db.executeSQLQuery(kGetPermissionId,(roleData[1].strip(),
												applicationId[0]['id'],
												roleData[3].strip()))
		if self.db.getRowCount('role_permission','role_id = %i and permission_id = %i' % (role_id[0]['id'],permission_id[0]['id'])) == 0:
			self.db.executeSQLCommand(kJoinRolePermission,(role_id[0]['id'],
														   permission_id[0]['id']))

	def updateCommonRoles(self):
		file,rawData = self.getCommonSiteImportFile('common_roles.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertRole(rawRow.split('|'), _siteOverride = self.curSite)
		file.close()

	def updateSiteSpecificRoles(self):
		file,rawData = self.getSiteImportFile('role.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertRole(rawRow.split('|'))
		file.close()

	def upsertRole(self, roleData, _siteOverride=None):
		siteCode = _siteOverride
		if not siteCode:
			siteCode = roleData[0].strip()
		siteId = self.db.executeSQLQuery(kGetSiteId,(siteCode,))
		applicationId = self.db.executeSQLQuery(kGetApplicationId,(roleData[1].strip(),))
		if self.db.getRowCount('role', "site_id = %s AND application_id = %s AND code = '%s'" % (siteId[0]['id'], applicationId[0]['id'], roleData[2].strip())):
			self.db.executeSQLCommand(kRoleUpdate,(roleData[3].strip(),
												   siteId[0]['id'],
												   applicationId[0]['id'],
												   roleData[2].strip()))
		else:
			self.db.executeSQLCommand(kRoleInsert,(siteId[0]['id'],
														 applicationId[0]['id'],
														 roleData[2].strip(),
														 roleData[3].strip()))

	def updateCommonPermissions(self):
		file,rawData = self.getCommonSiteImportFile('common_permissions.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertPermissions(rawRow.split('|'))
		file.close()

	def updateSiteSpecificPermissions(self):
		file,rawData = self.getSiteImportFile('permission.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertPermissions(rawRow.split('|'))
		file.close()

	def upsertPermissions(self, permissionData):
		siteCode = permissionData[0].strip()
		applicationId = self.db.executeSQLQuery(kGetApplicationId,(permissionData[1].strip(),))
		if self.db.getRowCount('permission', "site_code = '%s' AND application_id = %s AND code = '%s'" % (siteCode,applicationId[0]['id'],permissionData[2].strip())):
			self.db.executeSQLCommand(kUpdatePermission,(permissionData[3].strip(),
												   siteCode,
												   applicationId[0]['id'],
												   permissionData[2].strip()))
		else:
			self.db.executeSQLCommand(kInsertPermission,(siteCode,
														 applicationId[0]['id'],
														 permissionData[2].strip(),
														 permissionData[3].strip()))

	def joinMPSUsersToApplications(self):
		file,rawData = self.getSiteImportFile('mpsuser_application.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.joinUserWithApplication(rawRow.split('|'))
		file.close()

	def joinUserWithApplication(self,row):
		siteId = self.db.executeSQLQuery(kGetSiteId,(row[0].strip(),))
		communityCode = row[1].strip()
		if not communityCode:
			communityCode = 'default'
		communityId = self.db.executeSQLQuery(kCommunityId,(siteId[0]['id'], communityCode))[0]['id']
		userId = self.db.executeSQLQuery(kGetUserId,(siteId[0]['id'],communityId,row[2].strip(),))
		applicationId = self.db.executeSQLQuery(kGetApplicationId,(row[3].strip(),))
		if self.db.getRowCount('mpsuser_application','mpsuser_id = %i and application_id = %i' % (userId[0]['id'],applicationId[0]['id'])) == 0:
			self.db.executeSQLCommand(kJoinUserAndApplicaton,(siteId[0]['id'],
			                                                  communityId,
															  row[2].strip(),
															  row[3].strip(),
															  int(row[4].strip())))

	def updateMPSUsers(self):
		file,rawData = self.getSiteImportFile('mpsuser.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertMPSUsers(rawRow.split('|'))
		file.close()

	def upsertMPSUsers(self, userData):
		siteId = self.db.executeSQLQuery(kGetSiteId,(userData[0].strip(),))[0]['id']
		communityCode = userData[1].strip()
		if not communityCode:
			communityCode = 'default'
		communityId = self.db.executeSQLQuery(kCommunityId,(siteId, communityCode))[0]['id']
		activeBoolValue = self.getBool(userData[8])
		if self.db.getRowCount('mpsuser', "site_id = %i AND community_id = %s AND username = '%s'" % (siteId, communityId, userData[2].strip())):
			self.db.executeSQLCommand(kMPSUserUpdate,(userData[3].strip(),
													  userData[4].strip(),
													  userData[5].strip(),
													  userData[6].strip(),
													  userData[7].strip(),
													  activeBoolValue,
													  siteId,
													  communityId,
													  userData[2].strip()))
		else:
			self.db.executeSQLCommand(kMPSUserInsert,(siteId,
			                                          communityId,
													  userData[2].strip(),
													  userData[3].strip(),
													  userData[4].strip(),
													  userData[5].strip(),
													  userData[6].strip(),
													  userData[7].strip(),
													  activeBoolValue))

	def updateEnvironmentPrefs(self):
		file,rawData = self.getEnvironmentImportFile('site_preference.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertSitePrefs(rawRow.split('|'))
		file.close()

	def updateSitePrefs(self):
		file,rawData = self.getSiteImportFile('site_preference.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertSitePrefs(rawRow.split('|'))
		file.close()

	def upsertSitePrefs(self,prefsData):
		if self.db.getRowCount('site_preference', "site_code = '%s' AND code = '%s'" % (prefsData[0].strip(),prefsData[1].strip())):
			self.db.executeSQLCommand(kUpdatePref,(prefsData[2].strip(),
												   prefsData[0].strip(),
												   prefsData[1].strip()))
		else:
			self.db.executeSQLCommand(kInsertPref,(prefsData[0].strip(),
												   prefsData[1].strip(),
												   prefsData[2].strip()))

	def joinSitesWithApplications(self):
		file,rawData = self.getSiteImportFile('site_application.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.joinSiteWithApplicationData(rawRow.split('|'))
		file.close()

	def joinSiteWithApplicationData(self,row):
		siteId = self.db.executeSQLQuery(kGetSiteId,(row[0].strip(),))
		applicationId = self.db.executeSQLQuery(kGetApplicationId,(row[1].strip(),))
		if not self.db.getRowCount('site_application','site_id = %i and application_id = %i' % (siteId[0]['id'],applicationId[0]['id'])):
			self.db.executeSQLCommand(kJoinSiteAndApplicaton,(siteId[0]['id'],
															  applicationId[0]['id']))

	def updateSites(self):
		file,rawData = self.getSiteImportFile('site.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertSiteData(rawRow.split('|'))
		file.close()

	def upsertSiteData(self,siteData):
		if self.db.getRowCount('site', "code = '%s'" % (siteData[0])):
			self.db.executeSQLCommand(kSiteUpdate,(siteData[1].strip(),
												   siteData[2].strip(),
												   siteData[3].strip(),
												   siteData[0].strip()))
		else:
			self.db.executeSQLCommand(kSiteInsert,(siteData[0].strip(),
												   siteData[1].strip(),
												   siteData[2].strip(),
												   siteData[3].strip()))

	def updateApplications(self):
		file,rawData = self.getEnvironmentImportFile('application.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertApplicationData(rawRow.split('|'))
		file.close()

	def upsertApplicationData(self,applicationData):
		if self.db.getRowCount('application', "code = '%s'" % (applicationData[0])):
			self.db.executeSQLCommand(kApplicationUpdate,(applicationData[1].strip(),
														  applicationData[2].strip(),
														  applicationData[0].strip()))
		else:
			self.db.executeSQLCommand(kApplicationInsert,(applicationData[0].strip(),
														  applicationData[1].strip(),
														  applicationData[2].strip()))

	def updateCommonCommunities(self):
		file,rawData = self.getCommonSiteImportFile('common_communities.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertCommunity(rawRow.split('|'), _siteOverride = self.curSite)
		file.close()

	def updateSiteSpecificCommunities(self):
		file,rawData = self.getSiteImportFile('community.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertCommunity(rawRow.split('|'))
		file.close()

	def upsertCommunity(self, communityData, _siteOverride=None):
		siteCode = _siteOverride
		if not siteCode:
			siteCode = communityData[0].strip()
		siteId = self.db.executeSQLQuery(kGetSiteId,(siteCode,))
		code = communityData[1].strip()
		descr = communityData[2].strip()
		if self.db.getRowCount('site_community', "site_id = %s AND code = '%s'" % (siteId[0]['id'], code)):
			self.db.executeSQLCommand(kCommunityUpdate, (descr, siteId[0]['id'], code))
		else:
			self.db.executeSQLCommand(kCommunityInsert, (siteId[0]['id'], code, descr))

	def validRow(self,row):
		if not len(row.strip()) > 0:
			return False
		if row.startswith("#"):
			return False
		return True

	def getCommonSiteImportFile(self, fileName):
		filepath = os.path.abspath(__file__).split("car")[0] + "car/data/authData/sites/%s" % (fileName,)
		f = open(filepath,'rU')
		return f,f.readlines()

	def getSiteImportFile(self, fileName):
		mySite = self.curSite.replace('.','_').replace('-','_')
		filepath = os.path.abspath(__file__).split("car")[0] + "car/data/authData/sites/%s/%s" % (mySite, fileName)
		f = open(filepath,'rU')
		return f,f.readlines()

	def getEnvironmentImportFile(self, fileName):
		filepath = os.path.abspath(__file__).split("car")[0] + "car/data/authData/environments/%s/%s" % (self.env, fileName)
		f = open(filepath,'rU')
		return f,f.readlines()

	def getBool(self, instr):
		return stringUtils.interpretAsTrueFalse(instr)

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)


class DataLoadInterface:
	DESCR = '''Bare bones simple, yet POWERFUL! "AuthLoad.py is "The best application written since 1974 - PC Magazine"'''

	def __init__(self):
		pass

	def get_parser(self):
		allSites = 'dev,test,demo,umms,shib,dent-umich,engin-umich,accept-umich,med-oakland'
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsauth', help='database name (default=mpsauth')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mpsauth)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-e', '--env', dest='env', default='dev', help='environment (default=dev)')
		parser.add_option('-s', '--sites', dest='sites', default=allSites, help='list of sites to load (%s)' % allSites)

		return parser

	def run(self, options, args):
		authLoad = None
		try:
			authLoad = AuthLoad(options, args)
			authLoad.process()
		except Exception, e:
			print e.message
		finally:
			if authLoad:
				authLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
