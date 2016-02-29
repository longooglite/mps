# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.utilities.environmentUtils as envUtils
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.sqlUtilities as sqlUtils
import MPSCore.utilities.stringUtilities as stringUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

class DatabaseUtils():

	#   Housekeeping.

	def __init__(self):
		self.myConn = None

	@mpsExceptionWrapper("Unable to establish database connection")
	def getConnection(self):
		if not self.myConn:
			self.myConn = sqlUtils.SqlUtilities(envUtils.getEnvironment().getDbConnectionParms())
		return self.myConn

	def closeConnection(self):
		if self.myConn:
			try: self.myConn.closeMpsConnection()
			except Exception, e: pass
			self.myConn = None

	@mpsExceptionWrapper("Unable to save data")
	def performCommit(self):
		if self.myConn:
			self.myConn.performCommit()

	def performRollback(self):
		if self.myConn:
			try: self.myConn.performRollback()
			except Exception, e: pass


	#   P U B L I C   M E T H O D S .

	#   Generic

	def executeSQLQuery(self, _sql, _args, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery(_sql, _args)
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   Application-related.

	@mpsExceptionWrapper("Unable to obtain Application list")
	def getAllApplications(self, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery("SELECT * FROM application ORDER BY code")
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain Application data")
	def getApplicationForCode(self, _appCode, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery("SELECT * FROM application WHERE code=%s", (_appCode,))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain Site Application data")
	def getSiteApplications(self, _site, _shouldCloseConnection=True):
		sql = '''SELECT APP.code,APP.descr,APP.url FROM site_application AS SITEAPP JOIN application AS APP ON SITEAPP.application_id = APP.id WHERE SITEAPP.site_id = (SELECT id FROM site WHERE code = %s) ORDER BY APP.code'''
		try:
			return self.getConnection().executeSQLQuery(sql, (_site,))
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   Site-related.

	@mpsExceptionWrapper("Unable to obtain Site list")
	def getAllSites(self, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery("SELECT * FROM site ORDER BY code")
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to verify Site")
	def getSite(self, _site, _shouldCloseConnection=True):
		try:
			siteList = self.getConnection().executeSQLQuery("SELECT * FROM site WHERE code = %s", (_site,))
			if not siteList or len(siteList) != 1:
				raise excUtils.MPSValidationException("Site not found")
			return siteList[0]
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site data")
	def addSite(self, _siteDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO site (code,descr,active_start,active_end) VALUES (%s,%s,%s,%s)'''
		try:
			args = (_siteDict.get('code',None), _siteDict.get('descr',None), _siteDict.get('active_start',None), _siteDict.get('active_end',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site data")
	def saveSite(self, _siteDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''UPDATE site SET descr=%s,active_start=%s,active_end=%s WHERE code=%s'''
		try:
			args = (_siteDict.get('descr',None), _siteDict.get('active_start',None), _siteDict.get('active_end',None), _siteDict.get('code',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site/Application data")
	def associateSiteWithApplication(self, _siteCode, _appCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO site_application (site_id,application_id) VALUES ((SELECT id FROM SITE WHERE code=%s),(SELECT id FROM application WHERE code=%s))'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _appCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site data")
	def disassociateSiteApplication(self, _siteCode, _appCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM site_application WHERE site_id = (SELECT id FROM SITE WHERE code=%s) AND application_id = (SELECT id FROM application WHERE code=%s)'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _appCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site data")
	def disassociateSiteApplicationUsers(self, _siteCode, _appCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM mpsuser_application WHERE id IN
				(SELECT USRAPP.id FROM mpsuser_application USRAPP
				JOIN mpsuser USR ON USRAPP.mpsuser_id = USR.id
				WHERE USR.site_id = (SELECT id FROM SITE WHERE code=%s) AND
				USRAPP.application_id = (SELECT id FROM application WHERE code=%s))'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _appCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   Community-related.

	@mpsExceptionWrapper("Unable to obtain Community list")
	def getAllCommunities(self, _shouldCloseConnection=True):
		try:
			sql = '''SELECT site_community.*, site.code AS site_code, site.descr AS site_descr FROM site_community JOIN site ON site_community.site_id = site.id ORDER BY site_code, site_community.code, site_community.id'''
			return self.getConnection().executeSQLQuery(sql)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain Site Community data")
	def getSiteCommunities(self, _site, _shouldCloseConnection=True):
		sql = '''SELECT * FROM site_community WHERE site_id = (SELECT id FROM site WHERE code = %s) ORDER BY code, id'''
		try:
			return self.getConnection().executeSQLQuery(sql, (_site,))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Community data")
	def addCommunity(self, _communityDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO site_community (site_id,code,descr) VALUES (%s,%s,%s)'''
		try:
			args = (_communityDict.get('site_id',None), _communityDict.get('code',None), _communityDict.get('descr',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Community data")
	def saveCommunity(self, _communityDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''UPDATE site_community SET descr=%s WHERE site_id=%s AND code=%s'''
		try:
			args = (_communityDict.get('descr',None), _communityDict.get('site_id',None), _communityDict.get('code',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   Preference-related.

	@mpsExceptionWrapper("Unable to save Site Preference data")
	def getSitePreferences(self, _site, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery("SELECT * FROM site_preference WHERE site_code = %s", (_site,))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site Preference data")
	def getOneSitePreference(self, _id, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery("SELECT * FROM site_preference WHERE id = %s", (_id,))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain Site Prefix list")
	def getSitePreferencePrefixes(self, _shouldCloseConnection=True):
		try:
			return self.getConnection().executeSQLQuery("SELECT DISTINCT site_code FROM site_preference ORDER BY site_code")
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site Preference data")
	def addSitePref(self, _sitePrefDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO site_preference (site_code,code,value) VALUES (%s,%s,%s)'''
		try:
			args = (_sitePrefDict.get('site_code',None), _sitePrefDict.get('code',None), _sitePrefDict.get('value',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Site Preference data")
	def saveSitePref(self, _sitePrefDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''UPDATE site_preference SET site_code=%s,code=%s,value=%s WHERE id=%s'''
		try:
			args = (_sitePrefDict.get('site_code',None), _sitePrefDict.get('code',None), _sitePrefDict.get('value',None), _sitePrefDict.get('id',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to delete Site Preference data")
	def deleteSitePref(self, _sitePrefDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM site_preference WHERE id=%s'''
		try:
			args = (_sitePrefDict.get('id',None),)
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   Role-related.

	@mpsExceptionWrapper("Unable to obtain Site Role data")
	def getSiteRoles(self, _site, _shouldCloseConnection=True):
		sql = '''SELECT ROLE.id AS id, ROLE.code AS code, ROLE.descr AS descr, APP.code AS app_code, APP.descr AS app_descr
				FROM role AS ROLE
					JOIN application AS APP ON ROLE.application_id = APP.id
				WHERE site_id = (SELECT id FROM site WHERE code = %s)
				ORDER BY APP.code, ROLE.code'''
		try:
			return self.getConnection().executeSQLQuery(sql, (_site,))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain Role Permission data")
	def getRolePermissions(self, _site, _role, _shouldCloseConnection=True):
		sql = '''SELECT APP.code AS app_code, APP.descr AS app_descr, PERM.code AS perm_code, PERM.descr AS perm_descr
					FROM role AS ROLE
						JOIN role_permission AS ROLEPERM
							JOIN permission AS PERM
								JOIN application AS APP ON PERM.application_id = APP.id
							ON ROLEPERM.permission_id = PERM.id
						ON ROLE.id = ROLEPERM.role_id
					WHERE ROLE.site_id = (SELECT id FROM site WHERE code = %s)
					AND ROLE.code = %s
					ORDER BY APP.code, PERM.code;'''
		try:
			args = (_site, _role)
			return self.getConnection().executeSQLQuery(sql, args)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Role data")
	def addRole(self, _roleDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO role (site_id,application_id,code,descr) VALUES ((SELECT id FROM site WHERE code=%s),(SELECT id FROM application WHERE code=%s),%s,%s)'''
		try:
			args = (_roleDict.get('site',None), _roleDict.get('app',None), _roleDict.get('code',None), _roleDict.get('descr',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Role data")
	def saveRole(self, _roleDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''UPDATE role SET descr=%s WHERE site_id = (SELECT id FROM site WHERE code=%s) AND application_id = (SELECT id FROM application WHERE code=%s) AND code=%s'''
		try:
			args = (_roleDict.get('descr',None), _roleDict.get('site',None), _roleDict.get('app',None), _roleDict.get('code',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Role/Permission data")
	def associateRoleWithPermission(self, _siteCode, _roleAppCode, _roleCode, _appCode, _permCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO role_permission (role_id,permission_id) VALUES (
			(SELECT id FROM role WHERE site_id=(SELECT id FROM site WHERE code=%s) AND application_id=(SELECT id FROM application WHERE code=%s) AND code=%s),
			(SELECT id FROM permission WHERE (site_code = '' OR site_code = %s) AND application_id=(SELECT id FROM application WHERE code=%s) AND code=%s))'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _roleAppCode, _roleCode, _siteCode, _appCode, _permCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Role data")
	def disassociateRolePermission(self, _siteCode, _roleAppCode, _roleCode, _appCode, _permCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM role_permission WHERE
			role_id = (SELECT id FROM role WHERE site_id=(SELECT id FROM site WHERE code=%s) AND application_id=(SELECT id FROM application WHERE code=%s) AND code=%s) AND
			permission_id = (SELECT id FROM permission WHERE (site_code = '' OR site_code = %s) AND application_id=(SELECT id FROM application WHERE code=%s) AND code=%s)'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _roleAppCode, _roleCode, _siteCode, _appCode, _permCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to delete Role")
	def disassociateAllRolePermissions(self, _siteCode, _roleAppCode, _roleCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM role_permission WHERE
			role_id = (SELECT id FROM role WHERE site_id=(SELECT id FROM site WHERE code=%s) AND application_id=(SELECT id FROM application WHERE code=%s) AND code=%s)'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _roleAppCode, _roleCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save Role data")
	def deleteRole(self, _siteCode, _roleAppCode, _roleCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM role WHERE site_id=(SELECT id FROM site WHERE code=%s) AND application_id=(SELECT id FROM application WHERE code=%s) AND code=%s'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _roleAppCode, _roleCode), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   Permission-related.

	@mpsExceptionWrapper("Unable to obtain Site Permission data")
	def getPermissionsForSite(self, site, _shouldCloseConnection=True):
		try:
			sql = '''SELECT PERM.id AS id, PERM.application_id AS application_id, PERM.code AS code, PERM.descr AS descr, APP.code AS app_code, APP.descr AS app_descr
				FROM permission AS PERM
					JOIN application AS APP ON PERM.application_id = APP.id
				WHERE PERM.site_code = '' OR PERM.site_code = %s
				ORDER BY PERM.site_code, APP.code, PERM.code, PERM.id'''
			return self.getConnection().executeSQLQuery(sql, (site,))
		finally:
			if _shouldCloseConnection: self.closeConnection()


	#   User-related.

	@mpsExceptionWrapper("Unable to verify User")
	def getUser(self, _site, _community, _username, _shouldCloseConnection=True):
		try:
			sql = '''SELECT mpsuser.* , site_community.code AS community FROM mpsuser JOIN site_community ON site_community.id = mpsuser.community_id WHERE mpsuser.site_id = (SELECT id FROM site WHERE code = %s) AND community_id = (SELECT id FROM site_community WHERE site_id = (SELECT id FROM site WHERE code = %s) AND code = %s) AND lower(username) = %s;'''
			userList = self.getConnection().executeSQLQuery(sql, (_site, _site, _community, _username.lower()))
			if not userList or len(userList) != 1:
				raise excUtils.MPSValidationException("User not found")
			return userList[0]
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain User Application data")
	def getUserApplications(self, _site, _community, _username, _shouldCloseConnection=True):
		sql = '''SELECT APP.code,APP.descr,APP.url,seqnbr FROM mpsuser_application AS USERAPP
					JOIN application AS APP ON USERAPP.application_id = APP.id
				WHERE USERAPP.mpsuser_id = (SELECT mpsuser.id FROM mpsuser WHERE site_id = (SELECT id FROM site WHERE code = %s) AND community_id = (SELECT id FROM site_community WHERE site_id = (SELECT id FROM site WHERE code = %s) AND code = %s) AND lower(username) = %s)
				ORDER BY seqnbr,APP.code'''
		try:
			return self.getConnection().executeSQLQuery(sql, (_site, _site, _community, _username.lower()))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain User Role data")
	def getUserRoles(self, _site, _community, _username, _shouldCloseConnection=True):
		sql = '''SELECT ROLE.code AS code, ROLE.descr AS descr, APP.code AS application_code, APP.descr AS application_descr
				FROM mpsuser_role AS USERROLE
					JOIN role AS ROLE
						JOIN application AS APP ON ROLE.application_id = APP.id
					ON USERROLE.role_id = ROLE.id
				WHERE USERROLE.mpsuser_id = (SELECT mpsuser.id FROM mpsuser WHERE site_id = (SELECT id FROM site WHERE code = %s) AND community_id = (SELECT id FROM site_community WHERE site_id = (SELECT id FROM site WHERE code = %s) AND code = %s) AND lower(username) = %s)
				ORDER BY ROLE.code'''
		try:
			return self.getConnection().executeSQLQuery(sql, (_site, _site, _community, _username.lower()))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to obtain User Permission data")
	def getUserPermissions(self, _site, _community, _username, _shouldCloseConnection=True):
		sql = '''SELECT DISTINCT APP.code AS appcode, PERM.code, PERM.descr
				FROM mpsuser_role AS USERROLE
					JOIN role AS ROLE
						JOIN role_permission AS ROLEPERM
							JOIN permission AS PERM
								JOIN application AS APP ON PERM.application_id = APP.id
							ON ROLEPERM.permission_id = PERM.id
						ON ROLEPERM.role_id = ROLE.id
					ON USERROLE.role_id = ROLE.id
				WHERE USERROLE.mpsuser_id = (SELECT mpsuser.id FROM mpsuser WHERE site_id = (SELECT id FROM site WHERE code = %s) AND community_id = (SELECT id FROM site_community WHERE site_id = (SELECT id FROM site WHERE code = %s) AND code = %s) AND lower(username) = %s)
				ORDER BY APP.code, PERM.code;'''
		try:
			return self.getConnection().executeSQLQuery(sql, (_site, _site, _community, _username.lower()))
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save User data")
	def addUser(self, _userDict, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO mpsuser (site_id,community_id,username,password,first_name,last_name,email,auth_override,active) VALUES (
				(SELECT id FROM site WHERE code=%s),
				(SELECT id FROM site_community WHERE site_id = (SELECT id FROM site WHERE code=%s) AND code=%s),
				%s,%s,%s,%s,%s,%s,%s)'''
		try:
			encryptedPassword = _userDict.get('password','')
			if encryptedPassword:
				encryptedPassword = stringUtils.encryptValue(encryptedPassword)
			args = (_userDict.get('site',None),
				_userDict.get('site',None),
				_userDict.get('community',None),
				_userDict.get('username','').lower(),
				encryptedPassword,
				_userDict.get('first_name',None),
				_userDict.get('last_name',None),
				_userDict.get('email',None),
				_userDict.get('auth_override',''),
				_userDict.get('active',None))
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save User data")
	def saveUser(self, _userDict, _shouldCloseConnection=True, _doCommit=True):
		sql = []
		args = []

		sql.append('''UPDATE mpsuser SET first_name=%s,last_name=%s,email=%s,active=%s''')
		args.append(_userDict.get('first_name',None))
		args.append(_userDict.get('last_name',None))
		args.append(_userDict.get('email',None))
		args.append(_userDict.get('active',None))

		if 'auth_override' in _userDict:
			sql.append(''',auth_override=%s''')
			args.append(_userDict.get('auth_override',None))

		if 'password' in _userDict:
			encryptedPassword = _userDict.get('password',None)
			if encryptedPassword:
				encryptedPassword = stringUtils.encryptValue(encryptedPassword)
			sql.append(''',password=%s''')
			args.append(encryptedPassword)

		sql.append(''' WHERE site_id=(SELECT id FROM site WHERE code=%s)''')
		sql.append(''' AND community_id=(SELECT id FROM site_community WHERE site_id = (SELECT id FROM site WHERE code=%s) AND code=%s)''')
		sql.append(''' AND lower(username)=%s''')
		args.append(_userDict.get('site',None))
		args.append(_userDict.get('site',None))
		args.append(_userDict.get('community',None))
		args.append(_userDict.get('username','').lower())

		try:
			self.getConnection().executeSQLCommand(''.join(sql), tuple(args), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save User data")
	def disassociateAllApplicationsFromUser(self, _siteCode, _community, _username, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM mpsuser_application WHERE mpsuser_id = (
					SELECT mpsuser.id FROM mpsuser JOIN site_community JOIN site ON site_community.site_id = site.id ON mpsuser.community_id = site_community.id WHERE site.code = %s AND site_community.code = %s AND lower(mpsuser.username) = %s)'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _community, _username.lower()), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save User data")
	def associateApplicationWithUser(self, _siteCode, _community, _username, _appCode, _seqnbr, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO mpsuser_application (mpsuser_id,application_id,seqnbr) VALUES
				((SELECT mpsuser.id FROM mpsuser JOIN site_community JOIN site ON site_community.site_id = site.id ON mpsuser.community_id = site_community.id WHERE site.code = %s AND site_community.code = %s AND lower(mpsuser.username) = %s),
				(SELECT id FROM application WHERE code=%s),
				%s)'''
		args = (_siteCode, _community, _username, _appCode, _seqnbr)
		try:
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
 			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save User data")
	def disassociateAllRolesFromUser(self, _siteCode, _community, _username, _shouldCloseConnection=True, _doCommit=True):
		sql = '''DELETE FROM mpsuser_role WHERE mpsuser_id = (
					SELECT mpsuser.id FROM mpsuser JOIN site_community JOIN site ON site_community.site_id = site.id ON mpsuser.community_id = site_community.id WHERE site.code = %s AND site_community.code = %s AND lower(mpsuser.username) = %s)'''
		try:
			self.getConnection().executeSQLCommand(sql, (_siteCode, _community, _username.lower()), _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to save User data")
	def associateRoleWithUser(self, _siteCode, _community, _username, _appCode, _roleCode, _shouldCloseConnection=True, _doCommit=True):
		sql = '''INSERT INTO mpsuser_role (mpsuser_id,role_id) VALUES
				((SELECT mpsuser.id FROM mpsuser JOIN site_community JOIN site ON site_community.site_id = site.id ON mpsuser.community_id = site_community.id WHERE site.code = %s AND site_community.code = %s AND lower(mpsuser.username) = %s),
				(SELECT role.id FROM role,site,application WHERE role.site_id=site.id AND role.application_id=application.id AND site.code=%s AND application.code=%s AND role.code=%s))'''
		args = (_siteCode, _community, _username, _siteCode, _appCode, _roleCode)
		try:
			self.getConnection().executeSQLCommand(sql, args, _doCommit)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	@mpsExceptionWrapper("Unable to get list of User data")
	def getUsersForSiteAndApplication(self, _siteCode, _appCode, _shouldCloseConnection=True):
		sql = '''SELECT USR.id,COMM.code AS community,USR.username,USR.first_name,USR.last_name,USR.email
				FROM mpsuser AS USR JOIN mpsuser_application AS USERAPP ON USR.id = USERAPP.mpsuser_id JOIN site_community AS COMM ON USR.community_id = COMM.id
				WHERE USR.site_id = (SELECT id FROM site WHERE code=%s) AND USR.active = 't' AND USERAPP.application_id = (SELECT id FROM application WHERE code=%s)
				ORDER BY USR.last_name, USR.first_name, USR.username, USR.id'''
		args = (_siteCode, _appCode)
		try:
			return self.getConnection().executeSQLQuery(sql, args)
		finally:
			if _shouldCloseConnection: self.closeConnection()

	def logLogin(self, _now, _site, _community, _user, _mpsid, _action):
		sql = "INSERT INTO access_log (created,username,community,site,mpsid,access_action) VALUES (%s, %s, %s, %s , %s, %s)"
		args = (_now, _user, _community, _site, _mpsid, _action)
		try:
			self.getConnection().executeSQLCommand(sql, args)
		except Exception,e:
			pass
		finally:
			self.closeConnection()

	def logLogout(self, _now, _mpsid, _action):
		try:
			loginRecord = self.getLoginLog(_mpsid)
			self.logLogin(_now, loginRecord.get('site',''), loginRecord.get('community',''), loginRecord.get('username',''), _mpsid, _action)
		except:
			pass

	def logLoginUnsuccessful(self, _now, _site, _community, _username, _action):
		try:
			self.logLogin(_now, _site, _community, _username, '', _action)
		except:
			pass

	def getLoginLog(self, _mpsid):
		sql = "SELECT * FROM access_log WHERE mpsid = %s"
		args = (_mpsid,)
		try:
			qry = self.getConnection().executeSQLQuery(sql,args)
			return qry[0]
		except Exception,e:
			pass
