# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc_provost_approval = {
	"code": "tc_provost_approval",
	"descr": "Record Provost Results",
	"header": "Record Provost Results",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["tc_dean_approval_section"],
	"statusMsg": "Provost Review Complete",
	"successMsgApprove": "Provost votes submitted",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":["vpapproved","provostapproved","evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"regentsapproved",
			"sortOrder":"w1",
			"eventDescription":"Provost Review Complete",
			"eventType":"create",
			"permission":["ofa_task"]
		},],
			"denyDashboardEvents": [{
			"code":["vpapproved","provostapproved","evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"ofapacketrevisions",
			"sortOrder":"w2",
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
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": ["regents_vote","approveOFA"],
			"activityLogText": "Regents Revisions Required",
		},

		"revisionsRequired": False,
		"activityLog": {
			"enabled": True,
			"activityLogText": "Provost Approval",
			"comments": [
				{
					"commentCode": "regentsapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": True,
	},
}
