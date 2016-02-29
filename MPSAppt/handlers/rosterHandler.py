# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.rosterService as rosterSvc
import MPSAppt.services.jobActionCacheService as jaCacheSvc
import MPSAppt.services.departmentService as deptSvc

class RosterHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._getHandlerImpl('json', **kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptRosterView'])

		connection = self.getConnection()
		try:
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()

			#   'json' mode returns the actual Roster data.
			if (mode == 'json'):
				self.set_header('Content-Type','application/json')
				departmentList = deptSvc.DepartmentService(self.dbConnection).getDepartmentsForUser(community, username)
				roosterService = rosterSvc.RosterService(connection, self.getProfile())
				cacheService = jaCacheSvc.JobActionCacheService(departmentList)
				roster = roosterService.getRoster(community, username)
				cacheService.buildRosterDisplayLists(roster)

				rJSON = {}
				rJSON['rows'] = roosterService.trimRoster(roster)
				rJSON['department_list'] = cacheService.getDepartmentList()
				rJSON['track_list'] = cacheService.getTrackList()
				rJSON['title_list'] = cacheService.getTitleList()
				rJSON['job_action_type_list'] = cacheService.getJobActionTypeList()
				rJSON['job_action_status_list'] = cacheService.getJobActionStatusList()
				rJSON['position_status_list'] = cacheService.getPositionStatusList()
				rJSON['primality_list'] = cacheService.getPrimalityList()

				self.write(tornado.escape.json_encode(rJSON))
				return

			#   'html' mode returns the page frame.
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['canCreatePosition'] = self.hasPermission('apptCreatePosition')
			self.render("roster.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/page/roster', RosterHandler),
	(r'/appt/page/grid', RosterHandler),
]
