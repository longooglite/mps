# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.dashboardService as dashBoardSvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.jobActionCacheService as jaCacheSvc

class DashboardHandler(absHandler.AbstractHandler):
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

			if (mode == 'json'):
				self.set_header('Content-Type','application/json')
				departmentList = deptSvc.DepartmentService(self.dbConnection).getDepartmentsForUser(community, username)
				dashboardSvc = dashBoardSvc.DashboardService(connection)
				cacheService = jaCacheSvc.JobActionCacheService(departmentList)
				dashboardData = dashboardSvc.populateDashboard(self.getSitePreferences(), self.getUserPermissions(), departmentList)

				for eventType in dashboardData:
					eventCode = eventType.get('code','')
					for item in eventType.get('items',{}):
						item['deleteURL'] = '/appt/page/dashboard/delete/%s/%i' % (eventCode,item.get('job_action',{}).get('id',-1))

				cacheService.buildDashboardDisplayLists(dashboardData)

				rJSON = {}
				rJSON['rows'] = []
				rJSON['dashboard'] = dashboardData
				rJSON['department_list'] = cacheService.getDepartmentList()
				rJSON['track_list'] = cacheService.getTrackList()
				rJSON['title_list'] = cacheService.getTitleList()
				rJSON['job_action_type_list'] = cacheService.getJobActionTypeList()
				rJSON['job_action_status_list'] = cacheService.getJobActionStatusList()
				rJSON['position_status_list'] = cacheService.getPositionStatusList()
				rJSON['primality_list'] = cacheService.getPrimalityList()
				rJSON['workflow_list'] = cacheService.getWorkflowList()
				rJSON['event_list'] = cacheService.getEventList()

				self.write(tornado.escape.json_encode(rJSON))
				return

			#   'html' mode returns the page frame.

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			self.render("dashboard.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

class DeleteDashboardHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


	def post(self, **kwargs):
		try:
			self._postHandlerImpl( **kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return
		code = kwargs.get('code', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			dashBoardSvc.DashboardService(connection).manualRemoveDashboardEvent(code,jobactionid)
			responseDict = self.getPostResponseDict('')
			responseDict['redirect'] = '/appt/page/dashboard'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/page/dashboard/delete/(?P<code>[^/]*)/(?P<jobactionid>[^/]*)", DeleteDashboardHandler),
	(r'/appt/page/dashboard', DashboardHandler),
]
