# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils

def getAllTitles(_dbConnection, _includeInactive=True, _joinTrack=True,_orderByDescr = False):
	sql = []
	if _joinTrack:
		sql.append("SELECT TITLE.*, TRK.id AS track_id, TRK.code AS track_code, TRK.descr AS track_descr, TRK.active as track_active, TRK.metatrack_id as track_metatrack_id, TRK.tags as track_tags")
		sql.append("FROM wf_title AS TITLE")
		sql.append("LEFT OUTER JOIN wf_track AS TRK ON TITLE.track_id = TRK.id")
	else:
		sql.append("SELECT TITLE.* FROM wf_title AS TITLE")
	if not _includeInactive:
		sql.append("WHERE TITLE.active = 't'")
	if _orderByDescr:
		sql.append("ORDER BY UPPER(TITLE.descr)")
	else:
		sql.append("ORDER BY TITLE.code")
	return _dbConnection.executeSQLQuery(' '.join(sql))

def getTitle(_connection,_titleId):
	sql = "SELECT * FROM wf_title WHERE id = %s"
	args = (_titleId,)
	qry = _connection.executeSQLQuery(sql,args)
	return None if not qry else qry[0]

def getTitleByCode(_connection, _titleCode):
	sql = "SELECT * FROM wf_title WHERE code = %s"
	args = (_titleCode,)
	qry = _connection.executeSQLQuery(sql, args)
	return None if not qry else qry[0]

def getTitlesOnMetaTrack(_connection, metaTrackIds):
	inClause = stringUtils.getSQLInClause(metaTrackIds,False)
	sql = '''SELECT track.id as track_id,track.code as track_code, track.descr as track_descr,title.id as title_id,title.isactionable as isactionable,
	title.code as title_code, title.descr as title_descr, rank_order
	FROM wf_track track,wf_title title
	WHERE title.active = 't' AND title.track_id = track.id and track.id in%s ORDER BY track.id,rank_order,title_id;''' % (inClause)
	return _connection.executeSQLQuery(sql,())

def getTitlesOnTrack(_connection, _trackId):
	sql = "SELECT * FROM wf_title WHERE active = 't' AND track_id = %s ORDER BY rank_order,id ASC"
	args = (_trackId,)
	return _connection.executeSQLQuery(sql,args)

def createTitle(_dbConnection, _titleDict, doCommit=True):
	sql = '''INSERT INTO wf_title (code,descr,active,isactionable,job_code,track_id,position_criteria,rank_order,tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	args = (_titleDict.get('code', None),
			_titleDict.get('descr', None),
			_titleDict.get('active', None),
			_titleDict.get('isactionable', None),
			_titleDict.get('job_code', None),
			_titleDict.get('track_id', None),
			_titleDict.get('position_criteria', None),
			_titleDict.get('rank_order', None),
			_titleDict.get('tags', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def updateTitle(_dbConnection, _titleDict, doCommit=True):
	sql = '''UPDATE wf_title SET code=%s,descr=%s,active=%s,isactionable=%s,job_code=%s,track_id=%s,position_criteria=%s,rank_order=%s,tags=%s WHERE id=%s'''
	args = (_titleDict.get('code', None),
			_titleDict.get('descr', None),
			_titleDict.get('active', None),
			_titleDict.get('isactionable', None),
			_titleDict.get('job_code', None),
			_titleDict.get('track_id', None),
			_titleDict.get('position_criteria', None),
			_titleDict.get('rank_order', None),
			_titleDict.get('tags', None),
			_titleDict.get('id', None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)
