# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbcPersonalInfoRedux = {
	"code": "cbcPersonalInfoRedux",
	"comment":"",
	"descr": "Personal and Education Summary",
	"header": "Personal and Education Summary",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task",],
	"isProtectedCandidateItem":False,
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"CBC Redux was saved",
	"className": "PersonalInfoSummary",
	"config": {
		"prompts": [
			{
				"code": "attest",
				"label": "I agree to all of the terms of this Authorization and have completed it to the best of my knowledge.",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},
		],
		"form": "not used",
		"submitText": "I agree to all of the terms of this Authorization and have completed it to the best of my knowledge.",
		"personalInfoTaskCode": "taskF",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check PE Redux Confirmed",
		},
	},
}
