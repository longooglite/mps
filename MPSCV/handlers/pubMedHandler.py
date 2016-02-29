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
import MPSCV.utilities.environmentUtils as envUtils
import MPSCV.services.pubMedService as pubMedSVC
import MPSCV.services.cvService as cvSVC
import MPSCore.utilities.stringUtilities as strUtilities

class PubMedHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)
	cvList = []

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['cvEdit','cvCreate'])

		community = kwargs.get('community', 'default')
		username = kwargs.get('username', '')
		if (not community) or (not username):
			self.redirect("/cv")
			return

		try:
			connection = self.getConnection()
			person = cvSVC.getPerson(connection, community, username)
			firstname,lastname,affiliation = '','',''
			searchKey = ''
			searchDict = {}
			cv_id = -1
			if len(person) > 0:
				cv_id = person[0].get('id',-1)
				searchKey = person[0].get('pubmedsearchkey','')
				if len(searchKey) > 0:
					try:
						searchDict = eval(searchKey)
					except:
						searchDict = {}
						pass
					firstname = searchDict.get('first_name','')
					lastname = searchDict.get('last_name','')
					affiliation = searchDict.get('affiliation','')

			retrieved = ''
			available = ''
			importBooks = strUtilities.interpretAsTrueFalse(self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmedimportbooks','true'))
			pubmeddb = self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmeddb','')
			pubmedUIDReturnMax = self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmeduidretmax','')
			pubmedPubReturnMax = self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmedpubretmax','')
			pubMedService = pubMedSVC.PubMedService(connection,cv_id,pubmeddb,pubmedUIDReturnMax,pubmedPubReturnMax)
			mine,notmine,notreviewed,retrieved = pubMedService.prepopulatePubMedData()
			if len(searchKey) > 0:
				available = pubMedService.getNbrPubsAvailable(searchDict)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['cvCommunity'] = community
			context['cvOwner'] = username
			context['pubcategories'] = self.getPubMedBookCategories(pubMedService,importBooks)
			context['authorlastname'] = lastname
			context['authorfirstname'] = firstname
			context['affiliation'] = affiliation
			context['authorsearchkey'] = "%s %s" % (lastname,firstname)
			context['mine'] = mine
			context['notmine'] = notmine
			context['notreviewed'] = notreviewed
			context['nbrShown'] = retrieved
			context['nbrAvailable'] = available

			self.render("pubmed.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()


class PubMedPublicationSearchHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)
	cvList = []

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['cvEdit','cvCreate'])

		formData = tornado.escape.json_decode(self.request.body)
		community = formData.get('community', 'default')
		username = formData.get('username', '')
		authorfirstname = formData.get('authorfirstname','')
		authorlastname = formData.get('authorlastname','')
		affiliation = formData.get('affiliation','')

		try:
			connection = self.getConnection()
			person = cvSVC.getPerson(connection, community, username)
			cv_id = -1
			if len(person) > 0:
				cv_id = person[0].get('id',-1)
			importBooks = strUtilities.interpretAsTrueFalse(self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmedimportbooks','true'))
			pubmeddb = self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmeddb','')
			pubmedUIDReturnMax = self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmeduidretmax','')
			pubmedPubReturnMax = self.profile.get('siteProfile',{}).get('sitePreferences',{}).get('pubmedpubretmax','')
			searchKey = '''{"first_name":"%s","last_name":"%s","affiliation":"%s"}''' % (authorfirstname,authorlastname,affiliation)
			pubMedService = pubMedSVC.PubMedService(connection,cv_id,pubmeddb,pubmedUIDReturnMax,pubmedPubReturnMax,searchKey=searchKey)
			pubMedService.updatePubMedSearchKey(connection, person, searchKey)

			mine,notmine,notreviewed,retrieved,available = pubMedService.getPubMedData(eval(searchKey))

			responseDict = self.getPostResponseDict()
			responseDict['redirect'] = '/cv/pubmed/view/%s/%s' % (community, username)
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()

class PubMedSaveHandler(absHandler.AbstractHandler):
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

		try:
			connection = self.getConnection()

			#   Get form data.
			formData = tornado.escape.json_decode(self.request.body)
			community = formData.get('community', 'default')
			username = formData.get('username', '')
			person = cvSVC.getPerson(connection, community, username)
			cv_id = -1
			if len(person) > 0:
				cv_id = person[0].get('id',-1)

			self.persistPubs(connection,formData,cv_id,username)

			responseDict = self.getPostResponseDict()
			responseDict['redirect'] = '/cv/pubmed/view/%s/%s' % (community, username)
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def persistPubs(self,connection,formData, cv_id,user_id):
		categories = self.getPubCategories(formData)
		mine,notmine,notreviewed = self.getPubBuckets(formData,categories)
		pubMedService = pubMedSVC.PubMedService(connection,cv_id)
		pubMedService.persistPubOwnership(connection,cv_id,mine,notmine,notreviewed)
		loggedInUser = self.profile.get('userProfile').get('username')
		pubMedService.persistPubsToCV(connection,self.getPubMedMapping(),cv_id,mine,notmine,user_id,loggedInUser)

	def getPubBuckets(self,formData,pubCategories):
		mine,notmine,notreviewed = [],[],[]
		for key in formData:
			if key.startswith('cv_publicationstatus_'):
				keyparts = key.split("_")
				if len(keyparts) == 3:
					bucket = formData.get(key,'')
					uid = keyparts[2]
					pubcat = pubCategories.get(uid)
					updateDict = {"uid":uid,"pubcat":pubcat}
					if bucket == "notreviewed":
						notreviewed.append(uid)
					elif bucket == "mine":
						mine.append(updateDict)
					elif bucket == "notmine":
						notmine.append(updateDict)
		return mine,notmine,notreviewed

	def getPubCategories(self, formData):
		returnDict = {}
		for key in formData:
			if key.startswith('cv_publicationtype_'):
				keyparts = key.split("_")
				uid = keyparts[2]
				value = formData.get(key,'')
				returnDict[uid] = value
		return returnDict


#   All URL mappings for this module.
urlMappings = [
	(r"/cv/pubmed/view/(?P<community>[^/]*)/(?P<username>[^/]*)", PubMedHandler),
	(r'/cv/pubmed/search', PubMedPublicationSearchHandler),
	(r'/cv/pubmed/save', PubMedSaveHandler),
]
