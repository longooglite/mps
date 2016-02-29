# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAuthSvc.services.abstractService as absService

class CommunityService(absService.abstractService):
	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)

	def getAllCommunities(self):
		return self.getDbaseUtils().getAllCommunities()

	def addCommunity(self, _communityDict):
		self._persistCommunity(_communityDict, True)

	def saveCommunity(self, _communityDict):
		self._persistCommunity(_communityDict, False)

	def _persistCommunity(self, _communityDict, _isAdd):
		try:
			#   Update Community table data
			if _isAdd:
				self.getDbaseUtils().addCommunity(_communityDict, _shouldCloseConnection=False, _doCommit=False)
			else:
				self.getDbaseUtils().saveCommunity(_communityDict, _shouldCloseConnection=False, _doCommit=False)

			#   Commit transaction
			self.getDbaseUtils().performCommit()
			self.getDbaseUtils().closeConnection()

		except Exception, e:
			try: self.getDbaseUtils().performRollback()
			except Exception, e1: pass
			raise e
