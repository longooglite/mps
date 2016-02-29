# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

exec_com_vote = {
	"code": "exec_com_vote",
	"descr": "Record Executive Committee Results",
	"header": "Record Executive Committee Results",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task"],
	"blockers": ["assist_dean_approval","advisory_vote","adv_meeting_minutes","promo_assist_dean_approval"],
	"statusMsg": "",
	"successMsgApprove": "Executive Committee votes submitted",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":["assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"execcomapproved",
			"sortOrder":"s1",
			"eventDescription":"Executive Committee Review Complete",
			"eventType":"create",
			"permission":["ofa_task","adv_meeting_minutes"]
		},],
		"denyDashboardEvents": [{
			"code":["assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"ofapacketrevisions",
			"sortOrder":"s2",
			"eventDescription":"Packet Revisions Required",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"approveText": "Approved",
		"approveStatusMsg": "Executive Committee Complete",
		"revisionsRequired": False,
		"deny": True,
		"confirmDeny":False,
		"denyText": "Revisions Required",
		"denyStatusMsg": "Executive Committee Revisions Required",
		"denyFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["approveOFA"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": ["exec_com_vote","approveOFA"],
			"activityLogText": "Executive Committee Revisions Required",
		},

		"activityLog": {
			"enabled": True,
			"activityLogText": "Executive Committee Approval",
			"comments": [
				{
					"commentCode": "execcomapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": True,
	},
}
