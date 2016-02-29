# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractHandler as absHandler

#   An abstract class that all Evaluations-related handlers inherit from.

class AbstractEvalHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def executeCustomUberHook(self,container,context,evaluatorid):
		customHook = container.getConfigDict().get('customUberHook','')
		if customHook:
			try:
				importString = "import MPSAppt.modules.%s as mangler" % (customHook)
				exec importString
				manglerInstance = eval('mangler.UberContentMangler()')
				manglerInstance.mangleContent(self.dbConnection,context,container,evaluatorid)
			except:
				pass

