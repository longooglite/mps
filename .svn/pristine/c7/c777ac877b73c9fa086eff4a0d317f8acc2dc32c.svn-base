# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

complete_appointment = {
	"code": "complete_appointment",
	"descr": "Complete Appointment",
	"header": "Complete Appointment",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["complete_ppap_forms","send_ppap_forms"],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Appointment Complete",
	"className": "Completion",
	"config": {
		"buttonText": "Complete New Appointment",
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
