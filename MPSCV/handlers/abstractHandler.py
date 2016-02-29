# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

import MPSCore.handlers.coreApplicationHandler as coreAppHandler
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.stringUtilities as strUtilities
import MPSCV.utilities.environmentUtils as envUtils
import MPSCV.services.metaService as metaSvc
import MPSCV.services.cvService as cvService

from MPSCV.core.cvMenues import MENUES

class AbstractHandler(coreAppHandler.CoreApplicationHandler):
	kRoleProxyRead = 'Read'
	kRoleProxyWrite = 'Read / Write'

	#   Assorted Housekeeping methods..

	def getEnvironment(self):
		return envUtils.getEnvironment()

	def getMenues(self):
		return self.buildMenuList(MENUES)

	def getAppMenues(self):
		return [self.buildApplicationMenu(self.getUserProfile().get('userApplications',[]))]

	def getInitialTemplateContext(self, _environment=None):
		context = super(AbstractHandler, self).getInitialTemplateContext(_environment)
		context['windowTitle'] = 'Curriculum Vitae'
		context['pageHeaderTitle'] = 'Curriculum Vitae'
		return context

	def getPostResponseDict(self, _message=None):
		responseDict = {}
		if _message:
			try:
				msgDict = self.postToAuthSvc("/putMessage", { 'message': _message })
				responseDict['msgid'] = msgDict.get('msgid', '')
			except Exception as e:
					pass
		return responseDict

	def handleGetException(self, _exception, _logger, _optionalOverrideRedirect=None):
		super(AbstractHandler, self).handleGetException(_exception, _logger, _optionalOverrideRedirect)
		if not _optionalOverrideRedirect:
			self.redirect(envUtils.getEnvironment().getToastUri())


	#   Build data to drive the CV-specific vertical menu of Categories.

	def buildCVMenues(self, _dbConnection, categoryCode='', community='', username=''):
		selectedChild = None
		selectedMenuCode = categoryCode
		menues = metaSvc.getAllCategories(_dbConnection)
		selectedParentCode = self.getSelectedParentCode(menues,selectedMenuCode)
		index = 0
		selectFirstChild = False
		for menu in menues:
			code = menu.get('code','no menu selected').strip()
			parentcode = menu.get('parent_code','no menu selected').strip()

			menu['show'] = "true"
			menu['selected'] = "false"
			menu['is_submenu'] = "false"
			if len(parentcode.strip()) > 0:
				menu['is_submenu'] = "true"
			menu['community'] = community
			menu['username'] = username

			if selectFirstChild:
				menu['selected'] = "true"
				selectFirstChild = False
				selectedChild = code

			if code == selectedMenuCode:
				if parentcode == '':
					if len(menues) - 1 > index:
						if menues[index +1].get('parent_code') == selectedMenuCode:
							selectFirstChild = True
						else:
							menu['selected'] = "true"
					else:
						menu['selected'] = "true"
				else:
					menu['selected'] = "true"
			if menu.get('is_submenu','') == "true":
				menu['show'] = 'false'
				if parentcode == selectedParentCode:
					menu['show'] = 'true'
			index += 1
		return menues, selectedChild

	def getSelectedParentCode(self,menues,selectedMenuCode):
		for menu in menues:
			code = menu.get('code','')
			if code == selectedMenuCode:
				parent_code = menu.get('parent_code','')
				if len(parent_code) > 0:
					if code == selectedMenuCode:
						return parent_code
		return selectedMenuCode

	def getCategoryPrintMenu(self,_menuList):
		menuList = []
		printMenu = None
		for menu in _menuList:
			if menu.get('rootid','') == 'print':
				printMenu = menu
				break
		if printMenu:
			for item in printMenu.get('itemList',[]):
				if item.get('isSectionPrint',False):
					descr = item.get('altdescr','')
					url = item.get('url')
					menuDict = {"descr":descr,"url":url}
					menuList.append(menuDict)
			return menuList
		return []


	#   Get the profile of the CV Subject (i.e. the person who's CV is being edited).
	#   If the logged-in person is editing their own CV, then we can steal their
	#   profile, which was obtained when we validated their request. Otherwise, ask
	#   the Authorization Service for their information.

	def getCVSubject(self, _cvSubjectCommunity, _cvSubjectUsername):
		myUserProfile = self.getUserProfile()
		myCommunity = myUserProfile.get('community', 'default')
		myUsername = myUserProfile.get('username', '')
		if (myCommunity == _cvSubjectCommunity) and (myUsername == _cvSubjectUsername):
			return myUserProfile

		payload = self.getInitialPayload()
		payload['community'] = _cvSubjectCommunity
		payload['username'] = _cvSubjectUsername
		return self.postToAuthSvc("/getuser", payload)

	def getRoleCanReadWrite(self,roleStr):
		return False if roleStr == 'Read' else True

	def getRoles(self):
		return [self.kRoleProxyRead,self.kRoleProxyWrite]

	def validateUser(self,payload,community,username):
		payload['community'] = community
		payload['username'] = username
		try:
			userDict = self.postToAuthSvc("/getuser", payload)
		except Exception,e:
			userDict = []

		if userDict == []:
			return False
		return True

	def getProxyUserIsValid(self,connection,payload,grantor_community,grantor,grantee_community,grantee, isProxyRequest = True):
		message = ''
		if (grantor_community == grantee_community) and (grantee == grantor):
			return "Proxy holder cannot be the same as CV creator"

		if not self.validateUser(payload,grantee_community,grantee):
			return "%s was not found" % (grantee)
		if not self.validateUser(payload,grantor_community,grantor):
			return "%s was not found" % (grantor)

		proxiedCV = cvService.getProxiedCVForGrantorAndGrantee(connection,grantor_community,grantor,grantee_community,grantee)
		if proxiedCV <> []:
			if isProxyRequest:
				return 'You have already requested to serve as a proxy holder for %s' % (grantee)
			else:
				return '%s is already serving as a proxy holder for %s' % (grantee,grantor)

		return message

	def verifyProxyAccess(self, _dbConnection, _cvOwnerCommunity, _cvOwnerUsername):
		loggedInCommunity = self.getUserProfileCommunity()
		loggedInUser = self.getUserProfileUsername()
		if (loggedInCommunity == _cvOwnerCommunity) and (loggedInUser == _cvOwnerUsername):
			return None

		proxyDict = {}
		if self.hasPermission("cvProxyAll"):
			proxyDict['accepted_when'] = dateUtils.formatUTCDate()
			proxyDict['can_write'] = True
			proxyDict['deleted'] = False
			proxyDict['deleted_when'] = ''
			proxyDict['grantee_community'] = loggedInCommunity
			proxyDict['grantee'] = loggedInUser
			proxyDict['grantor_community'] = loggedInCommunity
			proxyDict['grantor'] = loggedInUser
			proxyDict['requested_when'] = proxyDict['accepted_when']
		else:
			proxyList = cvService.getProxiedCVForGrantorAndGrantee(_dbConnection, _cvOwnerCommunity, _cvOwnerUsername, loggedInCommunity, loggedInUser)
			if proxyList:
				proxyDict = proxyList[0]

		if proxyDict.get('accepted_when', ''):
			return proxyDict

		raise excUtils.MPSValidationException("Operation not permitted")

	def getFirstCategory(self, _connection):
		categories = metaSvc.getAllCategories(_connection)
		if categories:
			firstCategory = categories[0]
			firstCode = firstCategory.get('code', None)
			if firstCode:
				return firstCode
		return None

	def enableMenus(self, menuList, menuids, cvCommunity, cvOwner, categoryCode):
		for menu in menuList:
			if menu.get('rootid','') in menuids:
				menu['enabled'] = "true"
				for item in menu.get('itemList',[]):
					item['enabled'] = "true"
					if 'url' in item:
						url = item['url'].replace('{cvCommunity}', cvCommunity)
						url = url.replace('{cvOwner}', cvOwner)
						url = url.replace('{categoryCode}', categoryCode)
						item['url'] = url

	def getPubMedMapping(self):
		rootpath = envUtils.getEnvironment().getSrcRootFolderPath()
		filePart = self.getProfile().get('siteProfile', {}).get('sitePreferences', {}).get('pubmedmappingfile', '')
		f = open(rootpath+filePart,"rU")
		pubMedMappings = json.loads(f.read())
		f.close()
		return pubMedMappings

	def getPubMedBookCategories(self,pubMedService,showBooks = True):
		categoryCodes = []
		for cat in self.getPubMedMapping():
			if showBooks or not strUtilities.interpretAsTrueFalse(cat.get('dataElements',{}).get("isBook","false")):
				categoryCodes.append(cat.get('categoryCode',''))
		return pubMedService.getCategories(categoryCodes)

	def getParentCategories(self,connection):
		parentCategories = {}
		rawParentCategories = metaSvc.getParentCategories(connection)
		for each in rawParentCategories:
			parentCategories[each.get('code','')] = each.get('descr','')
		return parentCategories

