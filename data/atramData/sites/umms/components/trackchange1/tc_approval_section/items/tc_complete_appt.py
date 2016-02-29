# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc_complete_appt = {
	"code": "tc_complete_appt",
	"descr": "Complete Track Change",
	"header": "Complete Track Change",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["tc_approval_blocking_container"],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Track Change Complete",
	"className": "Completion",
	"config": {
		"alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"Track Change Complete",
		},
		"completeDashboardEvents": [{
			"eventType":"removeAll",
		},],
		"buttonText": "Complete Track Change",
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
