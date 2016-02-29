# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.utilities.databaseUtils as dbUtils

class abstractService():

	def __init__(self, _dbaseUtils=None):
		self.dbaseUtils = _dbaseUtils

	def getDbaseUtils(self):
		if not self.dbaseUtils:
			self.dbaseUtils = dbUtils.DatabaseUtils();
		return self.dbaseUtils

	pass
