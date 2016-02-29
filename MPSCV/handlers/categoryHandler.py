# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import tornado.httpclient
import tornado.web

import MPSCV.handlers.abstractHandler as absHandler
import MPSCV.services.cvService as cvSvc
import MPSCore.utilities.exceptionUtils as excUtils
import MPSCore.utilities.stringUtilities as stringUtils
from MPSCV.services import cvRendererService


class CategoryHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['cvView','cvEdit'])

		community = kwargs.get('community', 'default')
		username = kwargs.get('username', '')
		categoryCode = kwargs.get('categoryCode', '')
		tabCode = kwargs.get('tabCode', '')
		if (not username) or (not community):
			self.redirect("/cv")
			return

		try:
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)

			#   Determine if a CV exists for the specified person.
			#   If not, create one.

			personList = cvSvc.getPerson(connection, community, username)
			if not personList:
				cvSvc.createPerson(connection, community, username)
				personList = cvSvc.getPerson(connection, community, username)
				if not personList:
					raise excUtils.MPSException(_userMessage="Could not create CV for '%s'" % username)

				#   Seed the CV with the User's name.
				#   Not a killer if this doesn't work, so ignore errors.
				try:
					cvNameCode = self.getProfile().get('siteProfile', {}).get('sitePreferences', {}).get('cvnamecode', '')
					if cvNameCode:
						loggedInCommunity = self.getUserProfileCommunity()
						loggedInUser = self.getUserProfileUsername()
						if (loggedInCommunity == community) and (loggedInUser == username):
							userPrefs = self.getUserProfile().get('userPreferences', {})
						else:
							userPrefs = self.getCVSubject(community, username)

						fullName = stringUtils.constructFullName(userPrefs.get('first_name',''), userPrefs.get('last_name',''))
						cvSvc.initializeCV(connection, community, username, cvNameCode, fullName)
				except Exception, e:
					pass

			#   Determine editability.
			disabled = True
			if self.hasPermission('cvEdit'):
				if not proxyDict:
					disabled = False
				else:
					disabled = not proxyDict.get('can_write', False)

			#   Select the 1st Category if none is specified.
			if not categoryCode:
				categoryCode = self.getFirstCategory(connection)

			#   Get data to drive the CV-specific vertical menu of Categories.
			cvMenuList, newlySelectedChild = self.buildCVMenues(connection, categoryCode, community, username)
			if newlySelectedChild:
				categoryCode = newlySelectedChild

			cvSubject = self.getCVSubject(community, username)
			sitePrefs = self.getProfile().get('siteProfile', {}).get('sitePreferences', {})
			initialContext = self.getInitialTemplateContext()
			renderService = cvRendererService.CVPrintService(connection,initialContext,cvSubject,sitePrefs,None,self.getEnvironment())
			context = renderService.getCategoryViewContext(connection,categoryCode, community, username)

			self.enableMenus(context.get('menuList',[]),['print','manageexternaldata'], community, username, categoryCode)
			context['cvCommunity'] = community
			context['cvOwner'] = username
			context['categoryCode'] = categoryCode
			context['path'] = self.request.path
			context['addURL'] = '/'.join(['','cv','add',community,username,categoryCode])

			context['cvMenuList'] = cvMenuList
			context['isEditor'] = self.hasPermission('cvEdit')
			context['disabled'] = "disabled" if disabled else ""
			context['categoryPrintMenu'] = self.getCategoryPrintMenu(context.get('menuList',{}))
			self.render("category.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

class RowSequenceHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('cvEdit')

		formData = tornado.escape.json_decode(self.request.body)
		sequenceList = formData.get('sequence', [])
		if sequenceList:
			try:
				connection = self.getConnection()
				cvSvc.resequence(connection, sequenceList)
			finally:
				self.closeConnection()

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/cv/category'
		self.write(tornado.escape.json_encode(responseDict))


class RowDeleteHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('cvEdit')

		message = ''
		formData = tornado.escape.json_decode(self.request.body)
		cvCommunity = formData.get('community', 'default')
		cvOwner = formData.get('username', '')
		originPath = formData.get('origin_path', 0)
		rowId = formData.get('row_id', 0)
		if rowId:
			try:
				#   Verify that this row belongs to the CV being edited.
				connection = self.getConnection()
				personList = cvSvc.getRowPerson(connection, rowId)
				if personList and\
					len(personList) == 1 and\
					'user_id' in personList[0] and\
					cvCommunity and\
					str(personList[0]['community']) == str(cvCommunity) and\
					cvOwner and\
					str(personList[0]['user_id']).lower() == str(cvOwner).lower():

					#   Delete the row and attached attributes.
					cvSvc.deleteRow(connection, rowId)
					message = 'Entry deleted'
				else:
					message = 'Entry not found on this CV'
			finally:
				self.closeConnection()
		else:
			message = 'Entry not found'

		responseDict = self.getPostResponseDict(message)
		responseDict['redirect'] = originPath
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/cv/view/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<categoryCode>[^/]*)/(?P<tabCode>[^/]*)', CategoryHandler),
	(r"/cv/view/(?P<community>[^/]*)/(?P<username>[^/]*)/(?P<categoryCode>[^/]*)", CategoryHandler),
	(r"/cv/view/(?P<community>[^/]*)/(?P<username>[^/]*)", CategoryHandler),
	(r'/cv/sequence', RowSequenceHandler),
	(r'/cv/delete', RowDeleteHandler),
]
