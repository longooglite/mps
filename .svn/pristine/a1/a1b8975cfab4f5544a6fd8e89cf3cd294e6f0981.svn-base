# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getAllTracks(_dbConnection, _includeInactive=False, _joinMetatrack=False):
	sql = []
	if _joinMetatrack:
		sql.append("SELECT TRK.*, MT.id AS metatrack_id, MT.code AS metatrack_code, MT.descr AS metatrack_descr, MT.supplemental as metatrack_supplemental, MT.active as metatrack_active, MT.tags as metatrack_tags")
		sql.append("FROM wf_track AS TRK")
		sql.append("LEFT OUTER JOIN wf_metatrack AS MT ON TRK.metatrack_id = MT.id")
	else:
		sql.append("SELECT TRK.* FROM wf_track AS TRK")
	if not _includeInactive:
		sql.append("WHERE TRK.active = 't'")
	sql.append("ORDER BY TRK.code")
	return _dbConnection.executeSQLQuery(' '.join(sql))

def getTrackForTrackId(_dbConnection, _trackId, _includeInactive=False):
	sql = []
	sql.append("SELECT * FROM wf_track WHERE")
	if not _includeInactive:
		sql.append("active = 't' AND")
	sql.append("id = %s")
	qry = _dbConnection.executeSQLQuery(' '.join(sql), (_trackId,))
	return qry[0] if qry else None

def getTrackForTrackCode(_dbConnection, _trackCode, _includeInactive=False):
	sql = []
	sql.append("SELECT * FROM wf_track WHERE")
	if not _includeInactive:
		sql.append("active = 't' AND")
	sql.append("code = %s")
	qry = _dbConnection.executeSQLQuery(' '.join(sql), (_trackCode,))
	return qry[0] if qry else None

def getTracksForMetaTrackId(_dbConnection, _meta_track_id):
	sql = "SELECT * FROM wf_track WHERE active = 't' AND metatrack_id = %s"
	return _dbConnection.executeSQLQuery(sql, (_meta_track_id,))

def createTrack(_dbConnection, _trackDict, doCommit=True):
	sql = '''INSERT INTO wf_track (code,descr,active,metatrack_id,tags) VALUES (%s,%s,%s,%s,%s)'''
	args = (_trackDict.get('code', None),
			_trackDict.get('descr', None),
			_trackDict.get('active', None),
			_trackDict.get('metatrack_id', None),
			_trackDict.get('tags', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateTrack(_dbConnection, _trackDict, doCommit=True):
	sql = '''UPDATE wf_track SET code=%s,descr=%s,active=%s,metatrack_id=%s,tags=%s WHERE id=%s'''
	args = (_trackDict.get('code', None),
			_trackDict.get('descr', None),
			_trackDict.get('active', None),
			_trackDict.get('metatrack_id', None),
			_trackDict.get('tags', None),
			_trackDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getRawTrackChangeMaps(_dbConnection):
	sql = "SELECT tc.id AS tc_id,tc.code AS tc_code,tc.descr AS tc_descr,tc.workflow_code as tc_workflow_code," \
	      "from_track_id,to_track_id,from_title_id,to_title_id " \
	      "FROM wf_track_change tc,wf_track_change_map tcm where tcm.track_change_id = tc.id order by tc_code;"
	return _dbConnection.executeSQLQuery(sql,())