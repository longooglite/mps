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
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"isProtectedCandidateItem":False,
	"blockers": ["startappointment"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
	"className": "Attest",
	"config": {
		"disclosureGroup":{"code":"CBC","descr":"Background and Education Check Authorization"},
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
