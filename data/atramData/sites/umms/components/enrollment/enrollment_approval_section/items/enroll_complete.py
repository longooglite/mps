# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_complete = {
	"code": "enroll_complete",
	"descr": "All Requirements Met",
	"header": "All Requirements Met",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":True,
	"accessPermissions": ['ofa_task','dept_task',"enroll_task"],
	"viewPermissions": ['ofa_task','dept_task',"enroll_task"],
	"blockers": [],
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
