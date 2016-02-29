# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_complete = {
	"code": "cred_complete",
	"descr": "Complete Credentialing",
	"header": "Complete Credentialing",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":True,
	"accessPermissions": ["mss_task"],
	"viewPermissions": ['dept_task',"mss_task","ofa_task"],
	"blockers": ["credential_approval_section"],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Appointment Complete",
	"className": "Completion",
	"config": {
		"completeDashboardEvents": [{
			"eventType":"removeAll",
		},],
		"buttonText": "Complete",
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
