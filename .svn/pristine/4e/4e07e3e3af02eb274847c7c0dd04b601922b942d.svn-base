# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAuthSvc.handlers.abstractHandler as absHandler
import MPSAuthSvc.utilities.messageCache as msgCache

class PutMessageHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._putMessageHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _putMessageHandlerImpl(self):
		self.writePostResponseHeaders()
		messageDict = tornado.escape.json_decode(self.request.body)
		message = messageDict.get('message', "")

		msgid = msgCache.getMessageCache().addMessage(message)
		msgResponse = { 'msgid': msgid }
		self.write(tornado.escape.json_encode(msgResponse))


class GetMessageHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._getMessageHandlerImpl()
		except Exception, e:
			self.handleException(e, self.logger)

	def _getMessageHandlerImpl(self):
		self.writePostResponseHeaders()
		msgDict = tornado.escape.json_decode(self.request.body)
		msgid = msgDict.get('msgid', None)

		message = ""
		if msgid:
			message = msgCache.getMessageCache().popMessage(msgid)
		messageResponse = { 'message': message }
		self.write(tornado.escape.json_encode(messageResponse))


#   All URL mappings for this module.
urlMappings = [
	(r'/putMessage', PutMessageHandler),
	(r'/getMessage', GetMessageHandler),
]
