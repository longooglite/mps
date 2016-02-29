# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

rccomplete = {
	"code": "rccomplete",
	"descr": "Complete",
	"header": "Complete",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":True,
	"accessPermissions": ['ofa_task','dept_task'],
	"viewPermissions": ['ofa_task','dept_task'],
	"blockers": [],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Re-Credentialing Complete",
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
