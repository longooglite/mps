# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAuthSvc.authenticators.abstractAuthenticator as absAuthenticator
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.exceptionUtils as excUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

#   LDAP Authenticator.

class MpsAuthenticator(absAuthenticator.AbstractAuthenticator):
	logger = logging.getLogger(__name__)

	#   LDAP Authentication.

	@mpsExceptionWrapper("Invalid Username")
	def authenticate(self, _siteProfile, _community, _username, _password):

		#   Verify that we have a password.
		#   A password is always required for LDAP.

		if not _password:
			raise excUtils.MPSValidationException("Password required")

		#   Bypass LDAP lookup if network is not available.

		if envUtils.getEnvironment().getAvoidNetwork():
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug("granting access: Internet access is not available")
			return self.generateUniqueId()

		#   Get parameters for discussing issues with the LDAP.

		sitePreferences = _siteProfile.get('sitePreferences', {})
		ldapUrl = self._getSitePreferenceForCommunity(sitePreferences, 'ldapurl', _community)
		ldapPattern = self._getSitePreferenceForCommunity(sitePreferences, 'ldappattern', _community)
		dn = ldapPattern % _username

		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("authenticating '%s' against LDAP '%s'" % (dn, ldapUrl))

		bindResult = {}
		ldapConnection = None
		try:
			import ldap
			ldapConnection = ldap.initialize(ldapUrl)
			bindResult = ldapConnection.simple_bind_s(dn, _password)
		finally:
			if ldapConnection:
				try: ldapConnection.unbind_s()
				except Exception, e: pass

		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("LDAP authentication successful with result '%s'" % str(bindResult))

		return self.generateUniqueId()


	#   LDAP Search.

	@mpsExceptionWrapper("Unknown Username")
	def search(self, _siteProfile, _community, _username):

		#   Bypass LDAP lookup if network is not available.

		if envUtils.getEnvironment().getAvoidNetwork():
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug("LDAP search successful: Internet access is not available")

			result = {}
			result['cn'] = ['tbd']
			result['sn'] = ['tbd']
			result['mail'] = ['tbd@gomountainpass.com']
			result['givenName'] = ['tbd']
			return result

		#   Get parameters for discussing issues with the LDAP.

		sitePreferences = _siteProfile.get('sitePreferences', {})
		ldapUrl = self._getSitePreferenceForCommunity(sitePreferences, 'ldapurl', _community)
		ldapPattern = self._getSitePreferenceForCommunity(sitePreferences, 'ldappattern', _community)
		ldapBindUsername = self._getSitePreferenceForCommunity(sitePreferences, 'ldapsearchusername', _community)
		ldapBindPassword = self._getSitePreferenceForCommunity(sitePreferences, 'ldapsearchpassword', _community)
		ldapSearchAttrlist = self._getSitePreferenceForCommunity(sitePreferences, 'ldapsearchattrlist', _community)
		bindDN = ldapPattern % ldapBindUsername
		searchDN = ldapPattern % _username

		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("binding with '%s' against LDAP '%s'" % (bindDN, ldapUrl))

		bindResult = {}
		searchResult = {}
		ldapConnection = None
		try:
			import ldap
			ldapConnection = ldap.initialize(ldapUrl)
			bindResult = ldapConnection.simple_bind_s(bindDN, ldapBindPassword)

			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug("searching for '%s' against LDAP '%s'" % (searchDN, ldapUrl))

			attrlist = None
			if ldapSearchAttrlist:
				attrlist = []
				for thisAttr in ldapSearchAttrlist.split(','): attrlist.append(thisAttr)
			searchResult = ldapConnection.search_s(searchDN, ldap.SCOPE_BASE, attrlist=attrlist)

		finally:
			if ldapConnection:
				try: ldapConnection.unbind_s()
				except Exception, e: pass

		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("LDAP search successful with result '%s'" % str(searchResult))

		if not searchResult:
			return None
		firstTuple = searchResult[0]
		if len(firstTuple) < 2:
			return None
		return firstTuple[1]

	def _getSitePreferenceForCommunity(self, _sitePreferences, _key, _community):
		communityOverrideKey = "%s_%s" % (_key, _community)
		if communityOverrideKey in _sitePreferences:
			return _sitePreferences.get(communityOverrideKey, '')
		return _sitePreferences.get(_key, '')
