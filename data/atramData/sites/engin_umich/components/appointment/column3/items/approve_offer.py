# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

approve_offer = {
	"code": "approve_offer",
	"comment":"",
	"descr": '''Approve Offer''',
	"header": '''Approve Offer''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["submit_final_adaa"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Approve Offer Complete",
	"className": "Approval",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Approve Offer",
			"comments": [
				{
					"commentCode": "adaaOfferApprovalComment",
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
		"approveStatusMsg": "Offer approved by ADAA",
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
		"revisionsRequiredStatusMsg": "Draft Offer Revisions Required",
		"revisionsRequiredFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"unfreezeOptions": ["revise_offer","revise_grid","revise_addendum"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "",
			"activityLogText": "Draft Offer Revisions Required",
		},
		"vote": False,
	},
}
