# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbcConsent = {
	"code": "cbcConsent",
	"comment":"",
	"descr": "Consent",
	"header": "Consent",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task"],
	"isProtectedCandidateItem":False,
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"CBC Consent was saved",
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
		"form":"ummscbcconsent.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check Consent Placeholder",
		},
	},
}
