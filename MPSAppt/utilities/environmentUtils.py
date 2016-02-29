# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.coreEnvironmentUtils as superEnvironment
import MPSCore.utilities.stringUtilities as stringUtils

#   Global Environment settings.

class Environment(superEnvironment.CoreEnvironment):

	def __init__(self):
		superEnvironment.CoreEnvironment.__init__(self)
		self.setAppCode('APPT')
		self.setAppUriPrefix('appt')
		self.jobActionCompletionOn = False
		self.reportingCleanupOn = False


	#   Job Action Completion service

	def getJobActionCompletionOn(self): return self.jobActionCompletionOn
	def setJobActionCompletionOn(self, _jobActionCompletionOn): self.jobActionCompletionOn = stringUtils.interpretAsTrueFalse(_jobActionCompletionOn)


	#   Reporting Cleanup service

	def getReportingCleanupOn(self): return self.reportingCleanupOn
	def setReportingCleanupOn(self, _reportingCleanupOn): self.reportingCleanupOn = stringUtils.interpretAsTrueFalse(_reportingCleanupOn)


	#   Background Check Completion service

	def getBackgroundCheckCompletionOn(self): return self.backgroundCheckCompletionOn
	def setBackgroundCheckCompletionOn(self, _backgroundCheckCompletionOn): self.backgroundCheckCompletionOn = stringUtils.interpretAsTrueFalse(_backgroundCheckCompletionOn)

	def getBackgroundCheckIntervalMinutes(self): return self.backgroundCheckIntervalMinutes
	def setBackgroundCheckIntervalMinutes(self, _backgroundCheckIntervalMinutes): self.backgroundCheckIntervalMinutes = int(_backgroundCheckIntervalMinutes)


#	Create a default global CoreEnvironment instance,
#   and provide methods to retrieve it.

gEnvironment = Environment()

def getEnvironment():
	global gEnvironment
	return gEnvironment
