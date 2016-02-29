# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json
import logging
import logging.config

def initLogging(_loggingConfigFilepath):
	logging.config.fileConfig(_loggingConfigFilepath)

def getDefaultLogger():
	return logging.getLogger(__name__)

def isEnabledForDebug():
	return getDefaultLogger().isEnabledFor(logging.DEBUG)
