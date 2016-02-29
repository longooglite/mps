# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

advisory_vote = {
	"code": "advisory_vote",
	"descr": "Record Advisory Results",
	"header": "Record Results",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task"],
	"blockers": ["approveOFA"],
	"statusMsg": "",
	"successMsgApprove": "Advisory votes submitted",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":"ofapacketapproved",
			"eventType":"remove",
		},{
			"code":"advisoryapproved",
			"sortOrder":"q1",
			"eventDescription":"Advisory Review Complete",
			"eventType":"create",
			"permission":["ofa_task"]
		},],
		"denyDashboardEvents": [{
			"code":"ofapacketapproved",
			"eventType":"remove",
		},{
			"code":"ofapacketrevisions",
			"sortOrder":"q2",
			"eventDescription":"Packet Revisions Required",
			"eventType":"create",
			"permission":["ofa_task"]
		}],

		"approveText": "Approve",
		"approveStatusMsg": "Advisory Review Complete",
		"deny": True,
		"confirmDeny":False,
		"denyText": "Revisions Required",
		"denyStatusMsg": "Advisory Committee Revisions Required",
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
			"clearSubmitStatus": ["advisory_vote","approveOFA"],
			"activityLogText": "Advisory Revisions Required",
		},
		"revisionsRequired": False,
		"revisionsRequiredText": "Revisions Required",
		"revisionsRequiredStatusMsg": "Revisions Required",
		"revisionsRequiredFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"unfreezeOptions": ["approveOFA"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "approveOFA",
			"activityLogText": "Revisions Required",
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Advisory Approval",
			"comments": [
				{
					"commentCode": "advisoryapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": True,
	},
}
