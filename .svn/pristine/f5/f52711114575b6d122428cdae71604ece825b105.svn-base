# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import time
import datetime
import logging
import tornado.ioloop

'''
Variant of tornado.ioloop.PeriodicCallback that schedules a task to be run once daily
(i.e. once within a 24-hour period) at a specified time.

We subclass PeriodicCallback and re-purpose the 'callback_time'. Instead of a time interval
specified in thousandths of seconds, the 'callback_time' is interpreted as 'minutes past midnight'.
The caller indicates the number of minutes past midnight when the daily task is to be run.
For example:
	120 = 2:00 AM
	210 = 3:30 AM
	998 = 4:38 PM

The only method that needs to be overridden is _schedule_next, which uses 'callback_time' to
tell the I/O loop when to call the task. We also add an optional description for logging purposes.
'''

class MPSDailyCallback(tornado.ioloop.PeriodicCallback):
	logger = logging.getLogger(__name__)

	def __init__(self, callback, callback_time, io_loop=None, _descr='MPSDailyCallback'):
		super(MPSDailyCallback, self).__init__(callback, callback_time, io_loop)
		self.descr = _descr

	def _schedule_next(self):
		if self._running:
			futureTime = self._determineNextRunTime(self.callback_time)
			self._next_timeout = time.mktime(futureTime.timetuple())
			self._timeout = self.io_loop.add_timeout(self._next_timeout, self._run)
			self.logger.info("%s scheduled for %s" % (self.descr, futureTime.strftime('%m/%d/%Y %H:%M')))

	def _determineNextRunTime(self, _minutesPastMidnight):

		#   Schedule for later today if the specified wall clock time has not passed.
		#   Otherwise, bump to tomorrow.
		#   All computations are based on local server time.

		now = datetime.datetime.now()
		then = datetime.datetime(now.year, now.month, now.day)
		then = then + datetime.timedelta(minutes=_minutesPastMidnight)
		if then < now:
			then = then + datetime.timedelta(days=1)
		return then
