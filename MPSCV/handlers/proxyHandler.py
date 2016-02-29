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
import MPSCV.services.cvService as cvService

class ProxySaveNewProxyHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.writePostResponseHeaders()
		self.verifyAnyPermission(['cvView','cvEdit'])

		try:
			connection = self.getConnection()
			payload = self.getInitialPayload()

			formData = tornado.escape.json_decode(self.request.body)
			newcommunity = formData.get('search_community', 'default')
			newusername = formData.get('search_criteria','')
			canReadWrite = self.getRoleCanReadWrite(formData.get('role',''))
			cvuserCommunity = self.getUserProfileCommunity()
			cvuserName = self.getUserProfileUsername()
			newProxyuserIsValidMessage = self.getProxyUserIsValid(connection,payload,cvuserCommunity,cvuserName,newcommunity,newusername,False)
			responseDict = self.getPostResponseDict()

			if newProxyuserIsValidMessage == '':
				cvService.saveNewProxy(connection,cvuserCommunity,cvuserName,newcommunity,newusername,canReadWrite)
				responseDict['redirect'] = '/cv'
			else:
				responseDict['message'] = newProxyuserIsValidMessage
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


class ProxyRequestSaveHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.writePostResponseHeaders()
		self.verifyAnyPermission(['cvView','cvEdit'])

		try:
			formData = tornado.escape.json_decode(self.request.body)
			id = int(formData.get('pk',-1))
			canWrite = self.getRoleCanReadWrite(formData.get('role'))
			approved = formData.get('approved')

			responseDict = self.getPostResponseDict()
			responseDict['redirect'] = '/cv'

			connection = self.getConnection()
			cvService.updateProxyApproval(connection,id,canWrite,approved)
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


class ProxyRequestProxyAccessHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.writePostResponseHeaders()
		self.verifyAnyPermission(['cvView','cvEdit'])

		try:
			connection = self.getConnection()
			payload = self.getInitialPayload()

			formData = tornado.escape.json_decode(self.request.body)
			cvCommunity = formData.get('search_community','default')
			cvHolder = formData.get('search_criteria','')
			canReadWrite = self.getRoleCanReadWrite(formData.get('role',''))
			proxyCommunity = self.getUserProfileCommunity()
			proxyRequestor = self.getUserProfileUsername()
			newProxyuserIsValidMessage = self.getProxyUserIsValid(connection,payload,cvCommunity,cvHolder,proxyCommunity,proxyRequestor)
			responseDict = self.getPostResponseDict()

			if newProxyuserIsValidMessage == '':
				cvService.saveRequestForProxyAccess(connection,cvCommunity,cvHolder,proxyCommunity,proxyRequestor,canReadWrite)
				responseDict['message'] = 'Your proxy request has been sent.'
				responseDict['redirect'] = '/cv'
			else:
				responseDict['message'] = newProxyuserIsValidMessage
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


class ProxyRequestModifyHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.writePostResponseHeaders()
		self.verifyAnyPermission(['cvView','cvEdit'])
		try:
			connection = self.getConnection()
			formData = tornado.escape.json_decode(self.request.body)
			responseDict = self.getPostResponseDict()
			responseDict['redirect'] = '/cv'
			id = int(formData.get('pk',-1))
			canWrite = self.getRoleCanReadWrite(formData.get('role'))
			cvService.updateProxyRole(connection,id,canWrite)
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


class ProxyRequestDeleteHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.writePostResponseHeaders()
		self.verifyAnyPermission(['cvView','cvEdit'])
		try:
			connection = self.getConnection()
			formData = tornado.escape.json_decode(self.request.body)
			responseDict = self.getPostResponseDict()
			responseDict['redirect'] = '/cv'
			id = int(formData.get('pk',-1))
			cvService.updateProxyDenied(connection,id)
			self.write(tornado.escape.json_encode(responseDict))
		finally:
			self.closeConnection()


class ProxySearchHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.verifyRequest()
		self.writePostResponseHeaders()
		self.verifyAnyPermission(['cvView','cvEdit'])
		payload = self.getInitialPayload()
		formData = tornado.escape.json_decode(self.request.body)
		payload['search_community'] = formData.get('search_community', None)
		payload['search_criteria'] = formData.get('search_criteria','')
		usersList = self.postToAuthSvc("/proxyusersearch", payload)
		responseDict = self.getPostResponseDict()
		matches = []
		for each in usersList:
			person = {}
			person['value'] = each.get('username','')
			person['firstname'] = each.get('first_name','')
			person['lastname'] = each.get('last_name','')
			matches.append(person)
		self.write(tornado.escape.json_encode(matches))


#   All URL mappings for this module.
urlMappings = [
	(r'/cv/proxy/request', ProxySaveNewProxyHandler),
	(r'/cv/proxy/decision', ProxyRequestSaveHandler),
	(r'/cv/proxy/assign', ProxyRequestProxyAccessHandler),
	(r'/cv/proxy/save', ProxyRequestModifyHandler),
	(r'/cv/proxy/delete', ProxyRequestDeleteHandler),
	(r'/cv/proxy/search', ProxySearchHandler),
]
