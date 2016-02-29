# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

complete_appt = {
	"code": "complete_appt",
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
	"blockers": ["approval_blocking_container"],
	"statusMsg": "Scheduled for Completion",
	"successMsg":"Appointment Complete",
	"className": "Completion",
	"config": {
		"secondaryActionContainers":[{"determineActiveContainer":"secondary_one","deptTitleContainer":"sec_confirm_title1","approvalContainer":"sec_ofa_approve_rfp1"},
		                             {"determineActiveContainer":"secondary_two","deptTitleContainer":"sec_confirm_title2","approvalContainer":"sec_ofa_approve_rfp2"},
		                             {"determineActiveContainer":"secondary_three","deptTitleContainer":"sec_confirm_title3","approvalContainer":"sec_ofa_approve_rfp3"}],
		"alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"Appointment Complete",
		},
		"completeDashboardEvents": [{
			"eventType":"removeAll",
		},],
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
