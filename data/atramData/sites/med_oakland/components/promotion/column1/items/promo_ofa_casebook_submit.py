# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_ofa_casebook_submit = {
	"code": "promo_ofa_casebook_submit",
	"comment":"",
	"descr": '''Submit Full Promotion Application Casebook''',
	"header": '''Submit Full Promotion Application Casebook''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["dcapt_recommend"],
	"containers": [],
	"statusMsg": "Promotion Application Submitted",
	"successMsg":"Submission Complete",
	"className": "Submit",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Submit Full Promotion Application Casebook",
			"comments": [
				{
					"commentCode": "promoOfaCasebookSubmitComment",
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
