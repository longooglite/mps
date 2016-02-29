# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

provost_vote = {
	"code": "provost_vote",
	"descr": "Provost Approval",
	"header": "Provost Approval",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["provost_submit_date"],
	"statusMsg": "Provost Appointment Approved",
	"successMsgApprove": "Provost Appointment Approved",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":["evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"provostapproved",
			"sortOrder":"u1",
			"eventDescription":"Provost Review Complete",
			"eventType":"create",
			"permission":["ofa_task"]
		},],
		"denyDashboardEvents": [{
			"code":["evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"ofapacketrevisions",
			"sortOrder":"u2",
			"eventDescription":"Packet Revisions Required",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"approveText": "Approved",
		"approveStatusMsg": "Provost Review Complete",
		"deny": True,
		"confirmDeny":False,
		"denyText": "Revisions Required",
		"denyStatusMsg": "Provost Revisions Required",
		"denyFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["approveOFA"],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": ["provost_vote","approveOFA"],
			"activityLogText": "Provost Revisions Required",
		},
		"revisionsRequired": False,
		"activityLog": {
			"enabled": True,
			"activityLogText": "Advisory Approval",
			"comments": [
				{
					"commentCode": "provostapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": False,
	},
}
