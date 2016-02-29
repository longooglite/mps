# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.exceptionUtils as excUtils

#   Exception utilities intended for use across all MPS applications.

def application_exception_decorator(decorator):
	def new_decorator(f):
		g = decorator(f)
		g.__name__ = f.__name__
		g.__doc__ = f.__doc__
		g.__dict__.update(f.__dict__)
		return g

	new_decorator.__name__ = decorator.__name__
	new_decorator.__doc__ = decorator.__doc__
	new_decorator.__dict__.update(decorator.__dict__)
	return new_decorator

def mpsExceptionWrapper(message=''):
	@application_exception_decorator
	def wrapper(func):
		def hiddenFunctionName(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception, e:
				raise excUtils.wrapMPSException(e, _message=message)
		return hiddenFunctionName
	return wrapper
