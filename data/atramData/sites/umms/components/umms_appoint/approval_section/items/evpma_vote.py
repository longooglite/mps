# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

evpma_vote = {
	"code": "evpma_vote",
	"descr": "EVPMA Approval",
	"header": "EVPMA Approval",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["evpma_submit_date"],
	"statusMsg": "EVPMA Appointment Approved",
	"successMsgApprove": "EVPMA Appointment Approved",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":["execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"evpmaapproved",
			"sortOrder":"t1",
			"eventDescription":"EVPMA Review Complete",
			"eventType":"create",
			"permission":["ofa_task"]
		},],
		"denyDashboardEvents": [{
			"code":["execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"ofapacketrevisions",
			"sortOrder":"t2",
			"eventDescription":"Packet Revisions Required",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"approveText": "Approved",
		"approveStatusMsg": "EVPMA Review Complete",
		"deny": True,
		"confirmDeny":False,
		"denyText": "Revisions Required",
		"denyStatusMsg": "EVPMA Revisions Required",
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
			"clearSubmitStatus": ["evpma_vote","approveOFA"],
			"activityLogText": "EVPMA Revisions Required",
		},

		"revisionsRequired": False,
		"activityLog": {
			"enabled": True,
			"activityLogText": "EVPMA Approval",
			"comments": [
				{
					"commentCode": "evpmaapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": False,
	},
}
