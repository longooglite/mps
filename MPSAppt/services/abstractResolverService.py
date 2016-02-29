# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSCore.utilities.dateUtilities as dateUtils

#   Helper functions for Resolver Services.

class AbstractResolverService(AbstractTaskService):
	def __init__(self, _connection, _sitePreferences):
		AbstractTaskService.__init__(self, _connection)
		self.sitePreferences = _sitePreferences
		self.yFormat = self._getSitePreference('yformat', '%%Y')
		self.ymFormat = self._getSitePreference('ymformat', '%m/%Y')
		self.ymdFormat = self._getSitePreference('ymdformat', '%m/%d/%Y')
		self.ymdhmFormat = self._getSitePreference('ymdhmformat', '%m/%d/%Y %H:%M')
		self.tzname = self._getSitePreference('timezone', 'US/Eastern')

	#   Random stuff.

	def convertMDYToDisplayFormat(self, _dateInDbFormat):
		#   Convert a YYYY-MM-DD from the database to the Site's display format.
		if not _dateInDbFormat: return ''
		return dateUtils.parseDate(_dateInDbFormat, self.ymdFormat)

	def convertMYToDisplayFormat(self, _dateInDbFormat):
		#   Convert a YYYY-MM-DD from the database to the Site's display format.
		if not _dateInDbFormat: return ''
		return dateUtils.parseDate(_dateInDbFormat, self.ymFormat)

	def convertYToDisplayFormat(self, _dateInDbFormat):
		#   Convert a YYYY-MM-DD from the database to the Site's display format.
		if not _dateInDbFormat: return ''
		return dateUtils.parseDate(_dateInDbFormat, self.yFormat)

	def convertTimestampToDisplayFormat(self, _timestampInDbFormat):
		#   Convert a full timestamp from the database to the Site's display format.
		if not _timestampInDbFormat: return ''
		return dateUtils.parseDate(_timestampInDbFormat, self.ymdhmFormat)

	def localizeAndConvertTimestampToDisplayFormat(self, _timestampInDbFormat):
		#   Convert a full timestamp from the database to the Site's display format.
		if not _timestampInDbFormat: return ''
		localizedDate = dateUtils.localizeUTCDate(_timestampInDbFormat, _tzname=self.tzname)
		return dateUtils.parseDate(localizedDate, self.ymdhmFormat)

	def getSitePreferences(self):
		return self.sitePreferences

	def _getSitePreference(self, _key, _defaultValue):
		return self.sitePreferences.get(_key, _defaultValue)
