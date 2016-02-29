# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

termination_item = {
	"code": "termination_item",
	"descr": "Complete Termination",
	"header": "Complete Termination",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task","dept_task"],
	"viewPermissions": ["ofa_task","dept_task"],
	"blockers": [],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Termination Complete",
	"className": "Completion",
	"config": {
		"termination":True,
		"buttonText": "Complete Termination",
		"activityLogText": "Scheduled",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Scheduled for Completion",
			"comments": [
				{
					"commentCode": "terminationComment",
					"commentLabel": "Comments",
					"accessPermissions": ["ofa_task","dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
	},
}
