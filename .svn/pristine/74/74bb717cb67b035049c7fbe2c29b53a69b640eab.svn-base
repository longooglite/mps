# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_regents_vote = {
	"code": "promo_regents_vote",
	"descr": "Record Regents Results",
	"header": "Record Regents Results",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["approveOFA","promo_vp_research_vote"],
	"statusMsg": "Regent Review Complete",
	"successMsgApprove": "Regents votes submitted",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":["vpapproved","provostapproved","evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"regentsapproved",
			"sortOrder":"w1",
			"eventDescription":"Regents Review Complete",
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
		"approveStatusMsg": "Regent Review Complete",
		"deny": True,
		"confirmDeny":False,
		"denyText": "Revisions Required",
		"denyStatusMsg": "Regents Revisions Required",
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
			"activityLogText": "Advisory Approval",
			"comments": [
				{
					"commentCode": "regentsapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": False,
	},
}
