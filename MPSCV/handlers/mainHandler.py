# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import operator

import MPSCV.handlers.abstractHandler as absHandler
import MPSCV.services.cvService as cvService
import MPSCore.utilities.dateUtilities as dateUtilities
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCV.utilities.environmentUtils as envUtils

class MainHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)
	cvList = []

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		self.verifyAnyPermission(['cvView','cvEdit','cvCreate'])

		cvList = []
		loggedInCommunity = self.profile.get('userProfile',{}).get('community','')
		loggedInUsername = self.profile.get('userProfile',{}).get('username','')
		myUserPreferences = self.profile.get('userProfile',{}).get('userPreferences',{})

		try:
			connection = self.getConnection()

			sitePrefs = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			allowProxyRequests = stringUtils.interpretAsTrueFalse(sitePrefs.get('cvallowproxyrequests', 'no'))
			if self.hasPermission("cvProxyAll"):
				allowProxyRequests = False

			allowProxyAssignments = stringUtils.interpretAsTrueFalse(sitePrefs.get('cvallowproxyassignments', 'no'))
			#   Determine which CVs the user has access to.
			canOwnCV = self.hasPermission('cvCreate')
			if canOwnCV:
				cvDict = self.createCVListEntry(loggedInCommunity, loggedInUsername, myUserPreferences.get('first_name',''), myUserPreferences.get('last_name',''), True)
				cvList.append(cvDict)

			payload = self.getInitialPayload()
			tmpList = []
			if self.hasPermission("cvProxyAll"):
				payload['permissions'] = ['cvCreate']
				rawUserList = self.postToAuthSvc("/userlist", payload)
				for thisUserDict in rawUserList:
					thisUserCommunity = thisUserDict.get('community','')
					thisUsername = thisUserDict.get('username','')
					if (loggedInCommunity <> thisUserCommunity) or (loggedInUsername <> thisUsername):
						tmpList.append(self.createCVListEntry(thisUserCommunity, thisUsername, thisUserDict.get('first_name',''), thisUserDict.get('last_name',''), False))
			else:
				proxyUsers = cvService.getProxiedCVsForGrantee(connection, loggedInCommunity, loggedInUsername)
				if proxyUsers:
					for pUser in proxyUsers:
						thisUserCommunity = pUser.get('grantor_community','')
						thisUsername = pUser.get('grantor', '')
						if (thisUserCommunity) and (thisUsername):
							payload['community'] = thisUserCommunity
							payload['username'] = thisUsername
							thisUserDict = self.postToAuthSvc("/getuser", payload)

							cvDict = self.createCVListEntry(thisUserCommunity, thisUsername, thisUserDict.get('first_name',''), thisUserDict.get('last_name',''), False)
							tmpList.append(cvDict)
			cvList.extend(sorted(tmpList, key=operator.itemgetter('username')))

			cvProxyRequests = []
			cvAssignedProxies = []
			if allowProxyRequests or allowProxyAssignments:
				rawProxiedUsers = cvService.getProxiedCVsForGrantor(connection, loggedInCommunity, loggedInUsername)
				if allowProxyRequests:
					cvProxyRequests = self.getProxiedUsersDict(rawProxiedUsers, True)
				cvAssignedProxies = self.getProxiedUsersDict(rawProxiedUsers, False)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['canOwnCV'] = canOwnCV
			context['cvList'] = cvList
			context['cvProxyRequests'] = cvProxyRequests
			context['cvAssignedProxies'] = cvAssignedProxies
			context['roles'] = self.getRoles()
			context['username'] = myUserPreferences.get('full_name','')
			context['allowProxyRequests'] = allowProxyRequests
			context['allowProxyAssignments'] = allowProxyAssignments

			context['community'] = loggedInCommunity
			communityList = self.getSiteCommunityList()
			if len(communityList) > 1:
				context['promptCommunity'] = True
				context['communityList'] = communityList

			self.render("home.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def createCVListEntry(self, _community, _userid, _firstName, _lastName, _isMe):
		cvDict = {}
		cvDict['community'] = _community
		cvDict['userid'] = _userid
		cvDict['username'] = stringUtils.constructLastCommaFirstName(_firstName, _lastName)
		cvDict['isMe'] = _isMe
		return cvDict

	def getSelectedRole(self,canWrite):
		if canWrite:
			return self.kRoleProxyWrite
		return self.kRoleProxyRead

	def getProxiedUsersDict(self, rawUsers, isOutstandingRequest=False):
		proxyUsers = []
		for each in rawUsers:
			doAppend = False
			if isOutstandingRequest:
				if each.get('accepted_when',None) == None or each.get('accepted_when','') == '':
					doAppend = True
			else:
				if each.get('accepted_when',None) <> None and len(each.get('accepted_when','').strip()) > 0:
					doAppend = True
			if doAppend:
				pUserDict = {}
				pUserDict['id'] = each.get('id',-1)
				pUserDict['requesteddate'] = dateUtilities.parseDate(self.localizeDate(each.get('requested_when','')),self.getSiteYearMonthDayFormat())
				pUserDict['accepteddate'] = dateUtilities.parseDate(self.localizeDate(each.get('accepted_when')),self.getSiteYearMonthDayFormat())
				pUserDict['selected_role'] = self.getSelectedRole(each.get('can_write'))

				payload = self.getInitialPayload()
				payload['community'] = each.get('grantee_community')
				payload['username'] = each.get('grantee')
				userDict = self.postToAuthSvc("/getuser", payload)

				pUserDict['username'] = stringUtils.constructLastCommaFirstName(userDict.get('first_name',''), userDict.get('last_name',''))
				proxyUsers.append((pUserDict))
		return proxyUsers


class LogoutHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):

		#   Try to log out, no biggie if we can't.
		#   Redirect to Login page.
		try:
			payload = { 'mpsid': self.getCookie('mpsid') }
			self.postToAuthSvc("/logout", payload)
		except Exception:
			pass

		self.handleGetException(None, None)


#   All URL mappings for this module.
urlMappings = [
	(r'/cv', MainHandler),
	(r'/cv/logout', LogoutHandler),
]
