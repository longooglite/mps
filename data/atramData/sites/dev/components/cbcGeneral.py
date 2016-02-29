# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbcGeneral = {
	"code": "cbcGeneral",
	"comment":"",
	"descr": "General",
	"header": "General",
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
				"enabled": False,
				"required": False,
				"data_type": "checkbox",
			},
		],
		"submitText":"",
		"form":"ummscbcgeneral.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check General Edited",
		},
	},
}
