# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_complete_appt = {
	"code": "promo_complete_appt",
	"descr": "Complete Promotion",
	"header": "Complete Promotion",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["promo_approval_blocking_container"],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Promotion Complete",
	"className": "Completion",
	"config": {
		"secondaryPromoItem":"manage_joint_promotions",
		"alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"Promotion Complete",
		},
		"completeDashboardEvents": [{
			"eventType":"removeAll",
		},],
		"buttonText": "Complete Promotion",
		"activityLogText": "Scheduled",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Scheduled for Completion",
			"comments": [
				{
					"commentCode": "completionComment",
					"commentLabel": "Comments",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
	},
}
