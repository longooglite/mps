# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import shutil

import MPSAuthSvc.utilities.environmentUtils as envUtils


gWiperTaskLogger = logging.getLogger(__name__)

#   Wipe out the generated file work area.
#   This function is call once per day by the tornado web framework.

def WorkAreaWiperTask():
	global gWiperTaskLogger

	gWiperTaskLogger.info("WorkAreaWiperTask initiated")
	WorkAreaWiper().run()
	gWiperTaskLogger.info("WorkAreaWiperTask completed")

class WorkAreaWiper(object):

	def run(self):
		try:
			workAreaPath = envUtils.getEnvironment().getGeneratedOutputFolderPath()
			shutil.rmtree(workAreaPath, True)
		except Exception, e:
			pass
