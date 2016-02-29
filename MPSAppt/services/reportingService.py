# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json
from datetime import datetime
from datetime import timedelta

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.trackService as trackSvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.core.sql.reportingSQL as reportingSQL


class ReportingService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getReportingFilterForKey(self,entity,community = None,user = None, restrictToUserPermission = False):
		if entity == "wf_department":
			departmentSvc = deptSvc.DepartmentService(self.connection)
			if restrictToUserPermission:
				departments = departmentSvc.getDepartmentsForUser(community, user)
				return departmentSvc.getDepartmentHierarchy(departments,False,True)
			else:
				return departmentSvc.getDepartmentHierarchy(['NoUserRestriction'],False,True)
		elif entity == "wf_title":
			titleServ = titleSvc.TitleService(self.connection)
			return titleServ.getTitleHierarchy()
		elif entity == "wf_track":
			trackServ = trackSvc.TrackService(self.connection)
			return trackServ.getAllTracks()

	def persistReport(self,context,_content):
		community = context.get('profile',{}).get('userProfile',{}).get('community', 'default')
		username = context.get('profile',{}).get('userProfile',{}).get('username','')
		reportname = context.get('config',{}).get('reportName','')
		srcFile = context.get('config',{}).get('srcFile','')
		parameters = json.dumps(context.get('formData',{}))
		content = _content
		date_created = dateUtils.formatUTCDate()
		fileType = context.get('formData',{}).get('file_type','PDF')
		reportingSQL.persistReport(self.connection, community,username,reportname,srcFile,parameters,content,date_created,fileType)

	def getReportsForUser(self, _community, _username):
		userreports = reportingSQL.getReportsForUser(self.connection, _community, _username)
		for report in userreports:
			report['delete_url'] = '/appt/reporting/delete/%i' % (report.get('id',-1))
		return userreports

	def getNbrUnreadReportsForUser(self, _community, _username):
		return reportingSQL.getNbrUnreadReportsForUser(self.connection, _community, _username)

	def getReportForUser(self, _community, _username, _reportId, _now):
		content = reportingSQL.getReportContentForUser(self.connection, _community, _username, _reportId)
		self.markAsRead(_reportId,_now)
		return content

	def markAsRead(self,_reportId,_now):
		reportingSQL.markAsRead(self.connection,_reportId,_now)

	def getReportsCreatedBefore(self, _daysPrior, _utcNowStr):
		try:
			now = dateUtils.parseUTCDateOnly(_utcNowStr)
		except Exception, e:
			now = datetime.utcnow()

		beforeDate = now - timedelta(days=_daysPrior)
		beforeDateStr = dateUtils.formatUTCDateOnly(beforeDate)
		return reportingSQL.getReportsCreatedBefore(self.connection, beforeDateStr)

	def deleteReport(self, _reportId, doCommit=True):
		reportingSQL.deleteReport(self.connection, _reportId, doCommit=doCommit)

#   Reporting Data

	def getEvalItemData(self,itemCodes,beginDate,endDate,itemTableName):
		#look for items on completed job actions where the actions were completed between the begin and end date
		beginDateStr = dateUtils.formatUTCDate(beginDate)
		endDateStr = dateUtils.formatUTCDate(endDate)
		itemData = reportingSQL.getItemData(self.connection,itemCodes,beginDateStr,endDateStr,itemTableName)
		return itemData
