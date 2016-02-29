# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.coreEnvironmentUtils as superEnvironment

#   Global Environment settings.

class Environment(superEnvironment.CoreEnvironment):

	def __init__(self):
		superEnvironment.CoreEnvironment.__init__(self)
		self.setAppCode('LOGIN')
		self.setAppUriPrefix('login')


#	Create a default global CoreEnvironment instance,
#   and provide methods to retrieve it.

gEnvironment = Environment()

def getEnvironment():
	global gEnvironment
	return gEnvironment

