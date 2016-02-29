# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import datetime

import MPSCore.utilities.dateUtilities as dateUtils

#   This service provides a single public method, identifyGaps.
#   Given a list of start/end dates, the service returns a list of time intervals that are
#   not covered by the list of start/end dates, with a user-specified number of days tolerance.


class GapService:
	logger = logging.getLogger(__name__)

	def __init__(self):
		self.oneDay = datetime.timedelta(days=1)

	#   Return a list of time intervals that are not covered by the list of given start/end dates.
	#   Input:
	#       _dateList
	#           a list of dictionaries with start/end dates
	#           e.g. [ { 'startDate': '2012-01-14', 'endDate': '2014-05-30' }, { 'startDate': '1972-07-07', 'endDate': '1988-12-25' } ]
	#
	#       _nbrDays
	#           an integer number of days. Time lapses less than or equal to this number will not be reported.
	#
	#       _startDate
	#           date string on which interval measuring begins
	#           e.g. '1925-04-01'
	#           normally passed as None
	#           the earliest date in _dateList is used when _startDate is None
	#
	#       _endDate
	#           date string on which interval measuring ends
	#           e.g. '1944-09-11'
	#           normally passed as None
	#           the current date is used when _endDate is None
	#
	#   Output:
	#           a list of dictionaries with start/end dates and actual number of days in the interval
	#           e.g. [ { 'startDate': '2014-01-01', 'endDate': '2014-04-01', 'nbrDays': 90 } ]
	#
	#
	#   If you pass in junk that doesn't parse as dates or integers, this puppy just tosses an exception.
	#   Deal with it.
	#

	def identifyGaps(self, _dateList, _nbrDays, _startDate=None, _endDate=None):
		#   Convert all inputs to integers/dates as appropriate.
		normalizedDateList = self._normalizeDateList(_dateList)
		normalizedStartDate = self._normalizeStartDate(_startDate, normalizedDateList)
		normalizedEndDate = self._normalizeEndDate(_endDate)
		normalizedNbrDays = int(_nbrDays)

		#   If no startDate, then no dates ranges were given, and therefore, no gaps.
		if not normalizedStartDate:
			return []

		#   If we have a startDate, but no date list, then
		#   the entire start/end is potentially a gap, and we are done.
		if not normalizedDateList:
			if self._isGap(normalizedStartDate, normalizedEndDate, normalizedNbrDays):
				return self._stringifyDateList([ self._makeDateDict(normalizedStartDate + self.oneDay, normalizedEndDate - self.oneDay) ])
			return []

		#   Process the date list.
		gapList = []
		latestEndDate = normalizedStartDate

		while normalizedDateList:
			earliestDate, earliestDict = self._findEarliestDate(normalizedDateList)

			#   Make a gap if there's too many days between this date and the last end date.
			if self._isGap(latestEndDate, earliestDate, normalizedNbrDays):
				gapStart = latestEndDate + self.oneDay
				gapEnd = earliestDate - self.oneDay
				gapList.append(self._makeDateDict(gapStart, gapEnd))

			#   Housekeeping.
			thisEndDate = earliestDict['endDate']
			if thisEndDate > latestEndDate:
				latestEndDate = thisEndDate
			normalizedDateList.remove(earliestDict)

		#   Watch for a gap at the end.
		if self._isGap(latestEndDate, normalizedEndDate, normalizedNbrDays):
			gapStart = latestEndDate + self.oneDay
			gapEnd = normalizedEndDate - self.oneDay
			gapList.append(self._makeDateDict(gapStart, gapEnd))

		return self._stringifyDateList(gapList)


	#   Workers.

	def _findEarliestDate(self, _normalizedDateList):
		earliestDate = None
		earliestDict = None

		for each in _normalizedDateList:
			startDate = each['startDate']
			if not earliestDate:
				earliestDate = startDate
				earliestDict = each
			else:
				if startDate < earliestDate:
					earliestDate = startDate
					earliestDict = each

		return earliestDate, earliestDict

	def _isGap(self, _normalizedStartDate, _normalizedEndDate, _normalizedNbrDays):
		if self._daysBetween(_normalizedStartDate, _normalizedEndDate) > _normalizedNbrDays:
			return True
		return False

	def _daysBetween(self, _normalizedStartDate, _normalizedEndDate):
		return (_normalizedEndDate - _normalizedStartDate).days - 1

	def _makeDateDict(self, _start, _end):
		dateDict = {}
		dateDict['startDate'] = _start
		dateDict['endDate'] = _end
		return dateDict


	#   Date normalization.

	def _normalizeDateList(self, _dateList):
		newList = []
		for each in _dateList:
			newList.append(self._makeDateDict(self._normalizeDate(each.get('startDate', None)), self._normalizeDate(each.get('endDate', None))))
		return newList

	def _normalizeStartDate(self, _startDate, _normalizedDateList):
		if _startDate:
			return self._normalizeDate(_startDate) - self.oneDay
		start, ignored = self._findEarliestDate(_normalizedDateList)
		if start:
			return start - self.oneDay
		return None

	def _normalizeEndDate(self, _endDate):
		if _endDate:
			return self._normalizeDate(_endDate) + self.oneDay

		now = datetime.datetime.now()
		return datetime.date(now.year, now.month, now.day) + self.oneDay

	def _normalizeDate(self, _arg):
		if isinstance(_arg, datetime.datetime):
			return datetime.date(_arg.year, _arg.month, _arg.day)

		if isinstance(_arg, datetime.date):
			return _arg

		if isinstance(_arg, (str, unicode)):
			datePlusTime = dateUtils.parseUTCDateOnly(_arg)
			return datetime.date(datePlusTime.year, datePlusTime.month, datePlusTime.day)

		raise TypeError('%s cannot be evaluated as a date' % str(_arg))


	#   Date stringification.

	def _stringifyDateList(self, _normalizedDateList):
		newList = []
		for each in _normalizedDateList:
			start = each.get('startDate', None)
			end = each.get('endDate', None)

			newDict = self._makeDateDict(self._stringifyDate(start), self._stringifyDate(end))
			newDict['nbrDays'] = (end - start).days + 1
			newList.append(newDict)
		return newList

	def _stringifyDate(self, _arg):
		return dateUtils.formatUTCDateOnly(_arg)
