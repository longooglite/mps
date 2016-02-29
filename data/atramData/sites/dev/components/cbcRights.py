# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbcRights = {
	"code": "cbcRights",
	"comment":"",
	"descr": "Applicant Rights",
	"header": "Applicant Rights",
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
	"successMsg":"",
	"className": "Attest",
	"config": {
		"prompts": [
			{
				"code": "attest",
				"label": "",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},
		],
		"submitText":"Yes, I do agree to the above.",
		"form":"ummscbcrights.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check Applicant Rights Placeholder",
		},
	},
}
