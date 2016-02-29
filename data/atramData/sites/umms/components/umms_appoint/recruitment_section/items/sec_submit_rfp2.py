# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_submit_rfp2 = {
	"code": "sec_submit_rfp2",
	"descr": "Submit RFP",
	"header": "Submit RFP",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ['dept_task'],
	"viewPermissions": ['dept_task','ofa_task',"mss_task"],
	"overviewOnly":False,
	"blockers": ["sec_rfp2"],
	"statusMsg": "RFP Submitted",
	"successMsg": "RFP submitted",
	"className": "Submit",
	"config": {
		"departmentContainer":"sec_confirm_title2",
		"blacklist":{"departmentType":"primary","containers":["sec_dept_approve_rfp2"]},
		"whitelist":{"departmentType":"secondary","containers":["sec_dept_approve_rfp2"]},
		"disclosureGroup":{"code":"sec2","descr":"2nd Secondary Appointment"},
		"dashboardEvents": [{
			"code":"sec_submit_rfp2",
			"sortOrder":"d1",
			"eventDescription":"Secondary RFP Awaiting Approval",
			"eventType":"create",
			"permission":["dept_task"]
		},{
			"code":"sec_rfp2_revisions",
			"eventType":"remove",
		}],
		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": False,
			"freezeTasks": ["sec_confirm_title2","sec_rfp2"],
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
					"commentCode": "submitsecRFP2",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task"],
					"viewPermissions": ["dept_task","ofa_task"],
				},
			],
		},
	},
}
