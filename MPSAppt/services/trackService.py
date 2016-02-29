# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.trackSQL as trackSQL

class TrackService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getAllTracks(self, _includeInactive=False, _joinMetatrack=False):
		return trackSQL.getAllTracks(self.connection, _includeInactive=_includeInactive, _joinMetatrack=_joinMetatrack)

	def getTrackForTrackId(self, _trackId, _includeInactive=False):
		return trackSQL.getTrackForTrackId(self.connection, _trackId, _includeInactive=_includeInactive)

	def getTrackForTrackCode(self, _trackCode, _includeInactive=False):
		return trackSQL.getTrackForTrackCode(self.connection, _trackCode, _includeInactive=_includeInactive)

	def getTracksForMetaTrackId(self, _metatrack_id):
		return trackSQL.getTracksForMetaTrackId(self.connection, _metatrack_id)

	def saveTrack(self, _trackDict, _isEdit, doCommit=True):
		try:
			if _isEdit:
				trackSQL.updateTrack(self.connection, _trackDict, doCommit=False)
			else:
				trackSQL.createTrack(self.connection, _trackDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def getTrackChangeMapsRaw(self):
		return trackSQL.getRawTrackChangeMaps(self.connection)
