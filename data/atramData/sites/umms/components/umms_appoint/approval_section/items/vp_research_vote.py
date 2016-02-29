# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

vp_research_vote = {
	"code": "vp_research_vote",
	"descr": "Vice President of Research Approval",
	"header": "Vice President of Research Approval",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["vp_submit_date"],
	"statusMsg": "Vice-President for Research Appointment Approved",
	"successMsgApprove": "Vice-President for Research Appointment Approved",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveDashboardEvents": [{
			"code":["provostapproved","evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"vpapproved",
			"sortOrder":"v1",
			"eventDescription":"Vice President of Research Review Complete",
			"eventType":"create",
			"permission":["ofa_task"]
		},],
		"denyDashboardEvents": [{
			"code":["provostapproved","evpmaapproved","execcomapproved","assistdeanapproved","advisoryapproved","ofapacketapproved"],
			"eventType":"remove",
		},{
			"code":"ofapacketrevisions",
			"sortOrder":"v2",
			"eventDescription":"Packet Revisions Required",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"approveText": "Approved",
		"approveStatusMsg": "Vice-President for Research Review Complete",
		"deny": True,
		"confirmDeny":False,
		"denyText": "Revisions Required",
		"denyStatusMsg": "VP Research Revisions Required",
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
			"clearSubmitStatus": ["vp_research_vote","approveOFA"],
			"activityLogText": "VP Research Revisions Required",
		},

		"revisionsRequired": False,
		"activityLog": {
			"enabled": True,
			"activityLogText": "Advisory Approval",
			"comments": [
				{
					"commentCode": "vprsrchapprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"vote": False,
	},
}
