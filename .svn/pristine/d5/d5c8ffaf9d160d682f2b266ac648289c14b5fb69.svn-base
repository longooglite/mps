# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.sql.activitySQL as activitySQL


class ActivityService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getActivityLogsForJobAction(self, _jobActionId):
		return activitySQL.getActivityLogsForJobAction(self.connection, _jobActionId)

	def writeActivityLog(self, _jobTaskDict, _container, _formData, _activityLogConfigKeyName, _now, _username, doCommit=True):

		activityLogDict = _container.getConfigDict().get(_activityLogConfigKeyName,{})
		if not activityLogDict.get('enabled', False):
			return

		#   Write the Activity Log entry.

		logDict = {}
		logDict['job_action_id'] = _jobTaskDict.get('job_action_id', 0)
		logDict['job_task_id'] = _jobTaskDict.get('id', 0)
		logDict['activity'] = activityLogDict.get('activityLogText', '')
		logDict['created'] = _now
		logDict['lastuser'] = _username
		activitySQL.createActivityLog(self.connection, logDict, doCommit)
		activityLogId = self.connection.getLastSequenceNbr('wf_activity_log')

		#   Write associated Comments.

		for commentDict in activityLogDict.get('comments', []):
			if _container.hasAnyPermission(commentDict.get('accessPermissions',[])):
				commentCode = commentDict.get('commentCode','')
				commentText = _formData.get(commentCode,'')
				if commentText:
					commentDict = {}
					commentDict['activity_log_id'] = activityLogId
					commentDict['comment_code'] = commentCode
					commentDict['comment'] = commentText
					commentDict['created'] = _now
					commentDict['lastuser'] = _username
					activitySQL.createCommentLog(self.connection, commentDict, doCommit)

	def getActivityLogCache(self, _jobActionId):

		#   Returns a gross List of all activity.
		#   Each List entry is a Dictionary that consolidates multiple comments for an
		#       activity into a List on the Activity Entry dictionary.
		#   Suitable for displaying the entire activity log as one big gob of goo.
		#
		#   If we want activity by Task, then this should process the list and
		#       return a dictionary keyed by task_code.

		logList = []

		lastTaskCode = None
		lastActivity = None
		lastCreated = None
		lastDict = None
		rawList = self.getActivityLogsForJobAction(_jobActionId)
		for rawDict in rawList:
			thistaskCode = rawDict.get('task_code', '')
			thisActivity = rawDict.get('activity', '')
			thisCreated = rawDict.get('log_created', '')
			if (thisCreated != lastCreated) or \
				(thistaskCode != lastTaskCode) or \
				(thisActivity != lastActivity):
				lastDict = {}
				lastDict['task_code'] = thistaskCode
				lastDict['activity'] = thisActivity
				lastDict['created'] = thisCreated
				lastDict['username'] = rawDict.get('log_lastuser', '')
				lastDict['comments'] = []
				logList.append(lastDict)

				lastTaskCode = thistaskCode
				lastActivity = thisActivity
				lastCreated = thisCreated

			thisCommentCode = rawDict.get('comment_code', '')
			if thisCommentCode:
				commentDict = {}
				commentDict['comment_code'] = thisCommentCode
				commentDict['comment'] = rawDict.get('comment', '')
				lastDict['comments'].append(commentDict)

		return logList

	def getActivityLogByTaskCodeCache(self, _logList):

		#   Reorganizes the list created by getActivityLogCache() above into a dictionary keyed by task_code.
		#
		#   key = task_code
		#   value = list of activity log entries

		cache = {}
		for logDict in _logList:
			taskCode = logDict.get('task_code', '')
			if taskCode:
				if taskCode not in cache:
					cache[taskCode] = []
				cache[taskCode].append(logDict)
		return cache
