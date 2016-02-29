# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   Exception utilities intended for use across all MPS applications.

class MPSValidationException(Exception):
	pass


class MPSException(Exception):
	def __init__(self, _originalException=None, _userMessage=''):
		self.userMessage = _userMessage
		self.originalException = _originalException

	def getOriginalException(self): return self.originalException
	def getUserMessage(self): return self.userMessage

	def getDetailMessage(self):
		msg = self.getUserMessage()
		if self.getOriginalException():
			if msg: msg += '\n'
			for each in self.getOriginalException().args:
				msg += str(each) + '\n'
		return msg


def wrapMPSException(_originalException, _message=''):
	if isinstance(_originalException, MPSValidationException):
		return _originalException
	if isinstance(_originalException, MPSException):
		return _originalException
	return MPSException(_originalException, _message)