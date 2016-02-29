# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

submit_promo_app = {
	"code": "submit_promo_app",
	"comment":"",
	"descr": '''Submit Promotion Casebook for Review''',
	"header": '''Submit Promotion Casebook for Review''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["promo_app_block"],
	"containers": [],
	"statusMsg": "Promotion Application Submitted",
	"successMsg":"Submission Complete",
	"className": "Submit",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Submit Promotion Casebook for Review",
			"comments": [
				{
					"commentCode": "submitPromoAppComment",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task","ofa_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
		"data-confirm-msg":"Please confirm. You cannot undo this action.",

		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
		},
	},
}
