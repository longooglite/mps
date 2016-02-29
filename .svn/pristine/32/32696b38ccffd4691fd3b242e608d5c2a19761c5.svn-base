# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import json

import MPSCV.core.cvImporter as imputer
import MPSCV.handlers.abstractHandler as absHandler
import MPSCV.utilities.environmentUtils as envUtils

class ImportHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	#   GET presents the HTML form.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)


	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyPermission('cvExport')

		community = kwargs.get('community', '')
		username = kwargs.get('username', '')
		if (not community) or (not username):
			self.redirect("/cv")
			return

		#   Render the page.
		context = self.getInitialTemplateContext(envUtils.getEnvironment())
		context['cvCommunity'] = community
		context['cvOwner'] = username
		self.render("import.html", context=context, skin=context['skin'])


	#   POST processes the HTML form.

	def post(self):

		#   This POST handler is different from the 'normal' POST handlers for this application.
		#   It is submitted by the browser via a 'submit' button.
		#   It does not go through our normal jquery submission process.
		#   Therefore, some of the processing paradigms are different.

		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)
			self.doRedirect("An error occurred")

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.verifyPermission('cvExport')

		community = 'default'
		communityList = self.request.arguments.get('community',[])
		if communityList:
			community = communityList[0]
		if not community:
			self.doRedirect('Community not found')
			return

		username = ''
		usernameList = self.request.arguments.get('username',[])
		if usernameList:
			username = usernameList[0]
		if not username:
			self.doRedirect('User not found')
			return

		try:
			connection = self.getConnection()
			proxyDict = self.verifyProxyAccess(connection, community, username)

			fileData = self.request.files.get('file_data', [])
			if not fileData:
				self.doRedirect('No file provided')
				return

			fileObject = fileData[0]
			filename = fileObject.filename
			fileContents = fileObject.body

			try:
				cvDict = json.loads(fileContents)
			except Exception, e:
				self.doRedirect("File '%s' not a recognized CV file format" % filename)
				return

			importer = imputer.CVImporter()
			importer.doImport(connection, cvDict, _overrideCommunity=community, _overrideUsername=username)

			self.doRedirect("CV data imported", _url='/cv/view/%s/%s' % (community, username))

		finally:
			self.closeConnection()

	def doRedirect(self, _message, _url="/cv"):
		try:
			msgDict = self.postToAuthSvc("/putMessage", { 'message': _message})
			msgid = msgDict.get('msgid', '')
			if msgid:
				self.set_cookie('msgid', msgid)
		except Exception as e:
			pass

		self.redirect(_url)


#   All URL mappings for this module.
urlMappings = [
	(r"/cv/import/(?P<community>[^/]*)/(?P<username>[^/]*)", ImportHandler),
	(r'/cv/import', ImportHandler),
]
