# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

submit_faculty_affairs = {
	"code": "submit_faculty_affairs",
	"comment":"",
	"descr": '''Submit Appointment Casebook to Faculty Affairs''',
	"header": '''Submit Appointment Casebook to Faculty Affairs''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["dcapt_recommend"],
	"containers": [],
	"statusMsg": "Appointment Casebook submitted to Faculty Affairs",
	"successMsg":"Submission Complete",
	"className": "Submit",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Submit Appointment Casebook to Faculty Affairs",
			"comments": [
				{
					"commentCode": "submitFacultyAffairsComment",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task","ofa_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
		"data-confirm-msg":"Please confirm. You cannot undo this action.",

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
	},
}
