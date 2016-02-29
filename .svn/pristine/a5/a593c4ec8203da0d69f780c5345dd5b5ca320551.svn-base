# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

submit_offer_adaa = {
	"code": "submit_offer_adaa",
	"comment":"",
	"descr": '''Submit to ADAA''',
	"header": '''Submit to ADAA''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["cover_letter_chair","appt_activity"],
	"containers": [],
	"statusMsg": "Appointment casebook submitted",
	"successMsg":"Submit to ADAA Complete",
	"className": "Submit",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Submit to ADAA",
			"comments": [
				{
					"commentCode": "submitOfferAdaaComment",
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
