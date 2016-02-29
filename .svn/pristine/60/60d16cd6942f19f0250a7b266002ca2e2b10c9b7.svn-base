# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from datetime import datetime
from datetime import timedelta
import pytz

kUTCDateFormat = '%Y-%m-%d %H:%M:%S.%f'
kUTCDateOnlyFormat = '%Y-%m-%d'

def parseDate(timestampStr, formatStr):
	ts = normalizeTimestamp(timestampStr)
	strResult = ''
	try:
		dtobj = datetime.strptime(ts,kUTCDateFormat)
		strResult = dtobj.strftime(formatStr)
	except Exception,e:
		return timestampStr
	return strResult

def mungeDatePatternForDisplay(_pattern):
	pattern = _pattern.replace('%m', 'MM')
	pattern = pattern.replace('%d', 'DD')
	pattern = pattern.replace('%Y', 'YYYY')
	return pattern

def normalizeTimestamp(ts):
	hours, minutes, seconds = "00","00","00"
	milliseconds = "000000"
	month, day = "01","01"
	year = ""

	millisecondPortion = ts.split(".")
	if len(millisecondPortion) == 2:
		milliseconds = millisecondPortion[1]

	datetimePortion = ts.split(" ")
	if len(datetimePortion) == 2:
		timePortion = datetimePortion[1]
		timeParts = timePortion.split(":")
		if len(timeParts) > 0:
			hours = timeParts[0]
		if len(timeParts) > 1:
			minutes = timeParts[1]
		if len(timeParts) > 2:
			seconds = timeParts[2].split(".")[0]

	datePortion = datetimePortion[0]
	dateParts = datePortion.split("-")
	year = dateParts[0]
	if len(dateParts) > 1:
		month = dateParts[1]
	if len(dateParts) > 2:
		day = dateParts[2]

	return "%s-%s-%s %s:%s:%s.%s" % (year,month,day,hours,minutes,seconds,milliseconds)

#   Format the given datetime using the global date format.

def formatUTCDate(_datetime=None):
	dt = _datetime
	if not dt:
		dt = datetime.utcnow()
	return dt.strftime(kUTCDateFormat)

def formatUTCDateOnly(_datetime=None):
	dt = _datetime
	if not dt:
		dt = datetime.now()
	return dt.strftime(kUTCDateOnlyFormat)


#   Parses the given date string using the global date format.

def parseUTCDate(_datestring):
	return datetime.strptime(_datestring, kUTCDateFormat)

def parseUTCDateOnly(_datestring):
	return datetime.strptime(_datestring, kUTCDateOnlyFormat)

#   Convert a given datetime string to a localized datetime string.
#   The given date is assumed to be in utcDateFormat, and is assumed
#   to be a UTC time. The timezone name (i.e. 'US/Eastern') is used
#   to convert the UTC time to the indicated timezone.
#
#   Errors simply return to original _utcDateString and note the
#   problem by logging an error.

def localizeUTCDate(_utcDateString, _tzname='US/Eastern'):
	if not _utcDateString: return ''
	try:
		naiveUTCDate = datetime.strptime(_utcDateString, kUTCDateFormat)
		awareUTCDate = pytz.utc.localize(naiveUTCDate)

		dstTimezone = pytz.timezone(_tzname)
		awareDstDate = dstTimezone.normalize(awareUTCDate.astimezone(dstTimezone))
		return formatUTCDate(awareDstDate)
	except Exception, e:
		return _utcDateString


#   Convert a given local datetime string to a UTC datetime string.
#   The given date is assumed to be in utcDateFormat, and is assumed
#   to be a time in the given timezone name (i.e. 'US/Eastern').
#
#   Errors simply return to original _localDateString and note the
#   problem by logging an error.

def utcizeLocalDate(_localDateString, _tzname='US/Eastern'):
	if not _localDateString: return ''
	try:
		naiveLocalDate = datetime.strptime(_localDateString, kUTCDateFormat)
		awareLocalDate = pytz.timezone(_tzname).localize(naiveLocalDate)

		dstTimezone = pytz.timezone(_tzname)
		awareUTCDate = pytz.utc.normalize(awareLocalDate.astimezone(pytz.utc))
		return formatUTCDate(awareUTCDate)
	except Exception, e:
		return _localDateString


#   Flexible Date Parsing.

def flexibleDateMatch(_srcDateString, _pattern):
	#   Tries to parse the given _srcDateString against the given _pattern.
	#   Slashes or hyphens are matched.
	#   Throws an objection if the _srcDateString can't be matched.
	#   Returns a datetime object on success.

	#   Try the pattern straight out of the box.

	try:
		return datetime.strptime(_srcDateString, _pattern)
	except Exception, e:
		pass

	#   Replace hyphens in the pattern with slashes and try again.

	try:
		slashyPattern = _pattern.replace('-', '/')
		return datetime.strptime(_srcDateString, slashyPattern)
	except Exception, e:
		pass

	#   Replace slashes in the pattern with hyphens and try again.

	dashyyPattern = _pattern.replace('/', '-')
	return datetime.strptime(_srcDateString, dashyyPattern)


# Date Calculations

def datePlusDaysExceedsNow(beginDateStr,timeInDaysInt):
	now = parseUTCDateOnly(formatUTCDateOnly())
	targetDate = parseUTCDateOnly(beginDateStr) + timedelta(days=timeInDaysInt)
	if targetDate > now:
		return False,(targetDate-now).days
	return True,0
