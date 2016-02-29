# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.trackService as trackSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.core.sql.titleSQL as titleSQL
import MPSAppt.core.constants as constants

class TitleService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getAllTitles(self, _includeInactive=True, _joinTrack=True, _orderByDescr = False):
		return titleSQL.getAllTitles(self.connection, _includeInactive=_includeInactive, _joinTrack=_joinTrack,_orderByDescr=_orderByDescr)

	def getTitle(self,_title_id):
		return titleSQL.getTitle(self.connection,_title_id)

	def getTitleByCode(self, _titleCode):
		return titleSQL.getTitleByCode(self.connection, _titleCode)

	def getTitlesOnEquivalentMetaTrack(self,titleDict):
		titleList = []
		metatrackId = 0
		trackService = trackSvc.TrackService(self.connection)
		track = trackService.getTrackForTrackId(titleDict.get('track_id',0))
		if track:
			metatrackId = track.get('metatrack_id',0)
			tracks = trackService.getTracksForMetaTrackId(metatrackId)
			if tracks:
				titleList = self.getTitlesForMetaTrack(tracks)
		titleTrackDict = self.createTitleTrackDict(titleList)
		return titleTrackDict,metatrackId

	def getTitleHierarchy(self, _includeInactive=False):
		#   Currently only used by the reporting and workflow admin services.
		#   Puts tracks titles into same format as Department/Divisions so the same code can be used to render.
		returnValue = []
		allTitles = self.getAllTitles(_includeInactive=_includeInactive)
		currentTrackCode = ''
		currentTrackDict = {}
		for tracktitle in allTitles:
			if currentTrackCode <> tracktitle.get('track_code',''):
				currentTrackCode = tracktitle.get('track_code','')
				currentTrackDict = {"id":tracktitle.get('track_id',-1),"code":currentTrackCode,"descr":tracktitle.get('track_descr',''),"children":[]}
				returnValue.append(currentTrackDict)
			currentTrackDict['children'].append({"id":tracktitle.get('id',-1),"code":tracktitle.get('code',-1),"descr":tracktitle.get('descr',-1)})
		return returnValue

	def getTitlesByTrack(self):
		tracks = trackSvc.TrackService(self.connection).getAllTracks()
		titleList = []
		if tracks:
			titleList = self.getTitlesForMetaTrack(tracks)
		titleTrackDict = self.createTitleTrackDict(titleList)
		return titleTrackDict

	def getTitlesForTrackAboveRankOrder(self,trackDict,titleDict):
		returnTitles = []
		titles = titleSQL.getTitlesOnTrack(self.connection,trackDict.get('id',-1))
		for title in titles:
			if title.get('rank_order') > titleDict.get('rank_order'):
				returnTitles.append(title)
		return returnTitles

	def createTitleTrackDict(self,titleList):
		titleTrackDict = {"track":[]}
		thisTrack = '---'
		currentTrackDict = {"placehoder":[]}
		for trackTitleEntry in titleList:
			if thisTrack <> trackTitleEntry.get('track_descr',''):
				thisTrack = trackTitleEntry.get('track_descr','')
				currentTrackDict = {}
				currentTrackDict[thisTrack] = []
				titleTrackDict['track'].append(currentTrackDict)
			titleDict = {"title_descr":trackTitleEntry.get('title_descr',''),"title_id":trackTitleEntry.get('title_id',0),"title_code":trackTitleEntry.get('title_code',''),"isactionable":trackTitleEntry.get('isactionable',True)}
			currentTrackDict[thisTrack].append(titleDict)
		return titleTrackDict

	def getTitlesForMetaTrack(self,metaTracks):
		metaTrackIds = []
		for each in metaTracks:
			metaTrackIds.append(each.get('id',0))
		return titleSQL.getTitlesOnMetaTrack(self.connection,metaTrackIds)

	def saveTitle(self, _titleDict, _isEdit, doCommit=True):
		try:
			if _isEdit:
				titleSQL.updateTitle(self.connection, _titleDict, doCommit=False)
			else:
				titleSQL.createTitle(self.connection, _titleDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def appointmentIsEligibleForTrackChange(self,appointment):
		if appointment and appointment.get('apptstatus_code','') == constants.kAppointStatusFilled:
			title = self.getTitle(appointment.get('title_id',-1))
			if title:
				trackMaps = trackSvc.TrackService(self.connection).getTrackChangeMapsRaw()
				for map in trackMaps:
					if title.get('id',-1) == map.get('from_title_id',-1) and title.get('track_id') == map.get('from_track_id',-1):
						return True
		return False

	def getApplicableTrackChangesForCurrentAppointment(self,appointment):
		applicableTrackChanges = []
		if appointment and appointment.get('apptstatus_code','') == constants.kAppointStatusFilled:
			title = self.getTitle(appointment.get('title_id',-1))
			if title:
				rawMapping = trackSvc.TrackService(self.connection).getTrackChangeMapsRaw()
				for tcmap in rawMapping:
					if title.get('id',-1) == tcmap.get('from_title_id',-1) and title.get('track_id') == tcmap.get('from_track_id',-1):
						applicableTrackChanges.append(tcmap)
		return applicableTrackChanges

	def getTrackChangeMapForAppointment(self,appointment):
		returnValue = []
		titleMap = lookupTableSvc.getLookupTable(self.connection,'wf_title')
		trackMap = lookupTableSvc.getLookupTable(self.connection,'wf_track')
		title = self.getTitle(appointment.get('title_id',-1))
		rawtrackMaps = trackSvc.TrackService(self.connection).getTrackChangeMapsRaw()
		currentCode = ''
		currentMap = {}
		appendedMap = False
		for map in rawtrackMaps:
			if currentCode <> map.get('tc_code',''):
				currentCode = map.get('tc_code','')
				workflow = lookupTableSvc.getEntityByKey(self.connection,'wf_workflow',map.get('tc_workflow_code',''))
				if not workflow:
					workflow = {}
				currentMap = {"workflowid":workflow.get('id',-1),"code":map.get('tc_code',''),"descr":map.get('tc_descr',''),"workflow_code":map.get('tc_workflow_code',''),"mapping":[]}
				appendedMap = False
			if title.get('id',-1) == map.get('from_title_id',-1) and title.get('track_id') == map.get('from_track_id',-1):
				if not appendedMap:
					appendedMap = True
					returnValue.append(currentMap)
				trackTitleMap = {}
				trackTitleMap['fromTrackId'] = map.get('from_track_id',0)
				trackTitleMap['toTrackId'] = map.get('to_track_id',0)
				trackTitleMap['fromTitleId'] = map.get('from_title_id',0)
				trackTitleMap['toTitleId'] = map.get('to_title_id',0)
				trackTitleMap['fromTrackDescr'] = trackMap.get(map.get('from_track_id',{})).get('descr','')
				trackTitleMap['toTrackDescr'] = trackMap.get(map.get('to_track_id',{})).get('descr','')
				trackTitleMap['fromTitleDescr'] = titleMap.get(map.get('from_title_id',{})).get('descr','')
				trackTitleMap['toTitleDescr'] = titleMap.get(map.get('to_title_id',{})).get('descr','')
				currentMap['mapping'].append(trackTitleMap)
		return returnValue


