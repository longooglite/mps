# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

dept_approve_grid = {
	"code": "dept_approve_grid",
	"comment":"",
	"descr": '''Department Approve Grid''',
	"header": '''Department Approve Grid''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["signed_offer"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Department Approve Grid Complete",
	"className": "Approval",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Department Approve Grid",
			"comments": [
				{
					"commentCode": "deptApproveGridComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task","dept_task"],
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
			"freezeAllPredecessors": False,
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
		"denyStatusMsg": "TBD",
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

		"revisionsRequired": True,
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
			"unfreezeOptions": ["revise_grid"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "",
			"activityLogText": "Grid Revisions Required",
		},
		"vote": False,
	},
}
