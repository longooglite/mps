# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

submitOFA = {
	"code": "submitOFA",
	"descr": "Submit for Approval",
	"header": "Submit for Approval Here",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"overviewOnly":True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","ofa_task","mss_task"],
	"blockers": ["appt_blocking_container","promo_blocking_container","secondaries_section","tc2_appt_section","tc_appt_section","recruitment_container"],
	"statusMsg": "Packet submitted",
	"successMsg": "Packet submitted",
	"className": "Submit",
	"config": {
		"data-confirm-msg":"Please confirm. You cannot undo this action.",
		"dashboardEvents": [{
			"code":"ofapacketsubmit",
			"sortOrder":"o1",
			"eventDescription":"Packet Awaiting Review",
			"eventType":"create",
			"permission":["ofa_task"]
		},{
			"code":"ofapacketrevisions",
			"eventType":"remove",
		},{
			"code":"cbccomplete",
			"eventType":"remove",
		}],

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
		"activityLog": {
			"enabled": True,
			"activityLogText": "Packet Submitted for Approval",
			"comments": [
				{
					"commentCode": "submitComment",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
	},
}
