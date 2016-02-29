# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.utilities.environmentUtils as envUtils

#   Global Message Cache.

class MessageCache():

	def __init__(self):
		self.initMessageCache()

	#   (private) Accessors.

	def _getMessageCache(self): return self.messageCache

	#   Public methods.

	def initMessageCache(self): self.messageCache = dict()

	def addMessage(self, _message):
		msgid = envUtils.getEnvironment().generateUniqueId()
		self._getMessageCache()[msgid] = _message
		return msgid

	def getMessage(self, _msgid):
		if _msgid in self._getMessageCache():
			return self._getMessageCache()[_msgid]
		return ''

	def removeMessage(self, _msgid):
		if _msgid in self._getMessageCache():
			del self._getMessageCache()[_msgid]

	def popMessage(self, _msgid):
		message = self.getMessage(_msgid)
		self.removeMessage(_msgid)
		return message


#	Create a default global Message Cache instance,
#   and provide methods to retrieve it.

gMessageCache = MessageCache()

def getMessageCache():
	global gMessageCache
	return gMessageCache
