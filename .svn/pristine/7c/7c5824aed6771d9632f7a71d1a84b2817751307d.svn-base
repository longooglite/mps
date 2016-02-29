# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_int_submit_rfp = {
	"code": "sec_int_submit_rfp",
	"descr": "Submit RFP",
	"header": "Submit RFP",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ['dept_task'],
	"viewPermissions": ['dept_task','ofa_task'],
	"overviewOnly":False,
	"blockers": ["sec_int_rfp"],
	"statusMsg": "RFP Submitted",
	"successMsg": "RFP submitted",
	"className": "Submit",
	"config": {
		"noPrimaryDeptMsg":"Secondary appointments can only be created for faculty members that already have a primary appointment.",
		"departmentIdentifier":"personsprimary",
		"blacklist":{"departmentType":"primary","containers":["sec_int_dept_approve_rfp"]},
		"whitelist":{"departmentType":"secondary","containers":["sec_int_dept_approve_rfp"]},
		"dashboardEvents": [{
			"code":"sec_int_submit_rfp",
			"sortOrder":"d1",
			"eventDescription":"Secondary RFP Awaiting Approval",
			"eventType":"create",
			"permission":["dept_task"]
		},{
			"code":"sec_rfp1_revisions",
			"eventType":"remove",
		}],
		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": False,
			"freezeTasks": ["sec_confirm_title1","sec_rfp1"],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "RFP Submitted for Approval",
			"comments": [
				{
					"commentCode": "submitsecRFP1",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task"],
					"viewPermissions": ["dept_task","ofa_task"],
				},
			],
		},
	},
}
