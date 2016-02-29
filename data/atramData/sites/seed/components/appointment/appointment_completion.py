# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

appointment_completion = {
	"code": "appointment_completion",
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
	"blockers": [],
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
