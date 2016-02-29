# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

adaa_waiver_approval = {
	"code": "adaa_waiver_approval",
	"comment":"",
	"descr": '''Posting Waiver Approval''',
	"header": '''Draft Offer Letter''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Posting Waiver Approval Complete",
	"className": "Approval",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Posting Waiver Approval",
			"comments": [
				{
					"commentCode": "adaaWaiverApprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
		"approve": True,
		"approveDashboardEvents": [],
		"denyDashboardEvents": [],
		"revisionsDashboardEvents": [],

		"approveText": "Approve",
		"approveStatusMsg": "",
		"approveFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Approved",
		},

		"deny": True,
		"denyText": "Deny",
		"denyStatusMsg": "",
		"denyFreeze": {
			"confirmDeny":True,
			"freezeJobAction": True,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Denied",
		},

		"revisionsRequired": False,
		"vote": False,
	},
}
