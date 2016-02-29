# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.core.constants as constants
import MPSAppt.services.gapService as gapSvc


class UberGapService(AbstractTaskService):
	logger = logging.getLogger(__name__)

	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	#   Return a list of time intervals that are not covered by entries in specified UberForm Tables.
	#   Input:
	#       _container          a task container with an uberGapsConfig that supplies definitions of desired gaps
	#
	#   Item configuration looks like this:
	#
	#       e.g. [  {
	#                   "enabled": True,
	#           		"taskList": [
	#           		    {
	#          			        "taskCode": "cred_edu_training",
	#          			        "startDateIdentifierCode": "start_date",
	#          			        "endDateIdentifierCode": "end_date",
	#                       },
	#                       {
	#           			    "taskCode": "cred_work_experience",
	#           			    "startDateIdentifierCode": "start_date",
	#           			    "endDateIdentifierCode": "end_date",
	#                       },
	#                   ],
	#                   "nbrDays": 60,
	#                   "descr": "Education/Training and Work Experience",
	#               },
	#               {
	#                   "enabled": True,
	#                   "taskList": [
	#                       {
	#           			    "taskCode": "cred_prof_liability",
	#           			    "startDateIdentifierCode": "start_date",
	#           			    "endDateIdentifierCode": "end_date",
	#                       },
	#                   ],
	#                   "nbrDays": 60,
	#                   "descr": "Professional Liability Insurance",
	#               },
	#           ]
	#
	#
	#   Output:
	#       a list of dictionaries, one for each configuration specified in _container that has gaps.
	#       Each dictionary contains:
	#           'descr':        human-readable text string describing the nature of the gap
	#           'gapList':      a list of dictionaries with start/end dates and actual number of days in the interval
	#               'startDate'
	#               'endDate'
	#               'nbrDays'
	#               'prior'
	#               'subsequent'
	#
	#       e.g. [      {'descr': u'Education/Training and Work Experience',
	#                   'gapList': [{'endDate': '09/30/2015',
	#                               'nbrDays': 183,
	#                               'startDate': '04/01/2015'},
	#                               'prior': {'endDate': '03/31/2015',
	#                                          'name': 'Joe Schmoe Fly-by-Night Solutions',
	#                                          'startDate': '01/01/2015'}]},
	#                   {'descr': u'Professional Liability Insurance',
	#                   'gapList': [{'endDate': '06/30/2015',
	#                               'nbrDays': 149,
	#                               'startDate': '02/02/2015'},
	#                               {'endDate': '11/09/2015',
	#                               'nbrDays': 126,
	#                               'startDate': '07/07/2015'}]}
	#           ]

	def processContainer(self, _container, _sitePreferences, _configKeyName='uberGapsConfig', _returnLocalizedDates=True):
		allGapsList = []

		uberGapsConfig = _container.getConfigDict().get(_configKeyName, [])
		for gapConfigDict in uberGapsConfig:
			oneGapList = self._processOneGapConfig(_container, gapConfigDict)
			if oneGapList:
				gapDict = {}
				gapDict['descr'] = gapConfigDict.get('descr', '')
				gapDict['gapList'] = oneGapList
				allGapsList.append(gapDict)

		if _returnLocalizedDates:
			self._localizeDates(allGapsList, _sitePreferences)

		return allGapsList

	def _processOneGapConfig(self, _container, _gapConfigDict):
		if not _gapConfigDict.get('enabled', False):
			return None

		taskList = _gapConfigDict.get('taskList', [])
		if not taskList:
			return None

		subContainerList = []
		wf = _container.getWorkflow()
		for taskDict in taskList:
			taskCode = taskDict.get('taskCode', '')
			if taskCode:
				taskContainer = wf.getContainer(taskCode)
				if (taskContainer) and (taskContainer.getClassName() == constants.kContainerClassUberForm):
					taskDict['taskContainer'] = taskContainer
					subContainerList.append(taskDict)

		if not subContainerList:
			return None

		dateList = self._getDateList(subContainerList)
		nbrDays = _gapConfigDict.get('nbrDays', 60)
		startDate = _gapConfigDict.get('startDate', None)
		endDate = _gapConfigDict.get('endDate', None)
		gapList = gapSvc.GapService().identifyGaps(dateList, nbrDays, _startDate=startDate, _endDate=endDate)
		self._findGapNeighbors(gapList, dateList)
		return gapList

	def _getDateList(self, _subContainerList):
		dateList = []
		for subContainerDict in _subContainerList:
			oneDateList = self._getOneDateList(subContainerDict)
			if oneDateList:
				dateList.extend(oneDateList)
		return dateList

	def _getOneDateList(self, _subContainerDict):
		taskContainer = _subContainerDict.get('taskContainer', None)
		if not taskContainer:
			return None

		responseCache = taskContainer.getResponseCacheByIdentifierCode(_raw=True)
		startDateIdentifierCode = _subContainerDict.get('startDateIdentifierCode', 'start_date')
		endDateIdentifierCode = _subContainerDict.get('endDateIdentifierCode', 'end_date')
		institutionNameIdentifierCode = _subContainerDict.get('institutionNameIdentifierCode', 'institution_name')
		startDateList = responseCache.get(startDateIdentifierCode, [])
		endDateList = responseCache.get(endDateIdentifierCode, [])
		nameList = responseCache.get(institutionNameIdentifierCode, [])

		startLen = len(startDateList)
		endLen = len(endDateList)
		if startLen < endLen:
			for i in range(0,endLen - startLen):
				startDateList.append('')
		elif endLen > startLen:
			for i in range(0,startLen - endLen):
				endDateList.append('')
		endLen = len(endDateList)
		nameLen = len(nameList)
		if nameLen < endLen:
			for i in range(0,endLen - nameLen):
				nameList.append('')

		dateList = []
		for i in range(0, len(startDateList)):
			dateDict = {}
			dateDict['startDate'] = startDateList[i]
			dateDict['endDate'] = endDateList[i]
			dateDict['name'] = nameList[i]
			if (dateDict['startDate']) and (dateDict['endDate']):
				dateList.append(dateDict)
		return dateList

	def _findGapNeighbors(self, _gapList, _dateList):
		for gapDict in _gapList:
			self._findPriorGapEntry(gapDict, _dateList)
			self._findSubsequentGapEntry(gapDict, _dateList)

	def _findPriorGapEntry(self, _gapDict, _dateList):
		gapStartDate = _gapDict.get('startDate', '')
		if gapStartDate:
			latestPriorDict = None
			for dateDict in _dateList:
				endDate = dateDict.get('endDate', '')
				if (endDate) and (endDate < gapStartDate):
					if not latestPriorDict:
						latestPriorDict = dateDict
					else:
						if endDate > latestPriorDict.get('endDate', ''):
							latestPriorDict = dateDict

			if latestPriorDict:
				_gapDict['prior'] = latestPriorDict

	def _findSubsequentGapEntry(self, _gapDict, _dateList):
		gapEndDate = _gapDict.get('endDate', '')
		if gapEndDate:
			earliestSubsequentDict = None
			for dateDict in _dateList:
				startDate = dateDict.get('startDate', '')
				if (startDate) and (startDate > gapEndDate):
					if not earliestSubsequentDict:
						earliestSubsequentDict = dateDict
					else:
						if startDate < earliestSubsequentDict.get('startDate', ''):
							earliestSubsequentDict = dateDict

			if earliestSubsequentDict:
				_gapDict['subsequent'] = earliestSubsequentDict

	def _localizeDates(self, _gapsList, _sitePreferences):
		format = _sitePreferences.get('ymdformat', '%m/%d/%Y')
		for each in _gapsList:
			for dateDict in each.get('gapList', []):
				dateDict['startDate'] = dateUtils.parseUTCDateOnly(dateDict.get('startDate', '')).strftime(format)
				dateDict['endDate'] = dateUtils.parseUTCDateOnly(dateDict.get('endDate', '')).strftime(format)
				
				priorDateDict = dateDict.get('prior', {})
				if priorDateDict:
					newDict = {}
					newDict['startDate'] = dateUtils.parseUTCDateOnly(priorDateDict.get('startDate', '')).strftime(format)
					newDict['endDate'] = dateUtils.parseUTCDateOnly(priorDateDict.get('endDate', '')).strftime(format)
					newDict['name'] = priorDateDict.get('name', '')
					dateDict['prior'] = newDict
				
				subsequentDateDict = dateDict.get('subsequent', {})
				if subsequentDateDict:
					newDict = {}
					newDict['startDate'] = dateUtils.parseUTCDateOnly(subsequentDateDict.get('startDate', '')).strftime(format)
					newDict['endDate'] = dateUtils.parseUTCDateOnly(subsequentDateDict.get('endDate', '')).strftime(format)
					newDict['name'] = subsequentDateDict.get('name', '')
					dateDict['subsequent'] = newDict
