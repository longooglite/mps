# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_release_statement = {
	"code": "cred_release_statement",
	"comment":"",
	"descr": "Release Statement",
	"header": "Release Statement",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"blockers": ["cred_upload_image_id",],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Release statement was saved",
	"className": "Attest",
	"config":
	{
		"prompts": [
			{
				"code": "attest",
				"label": "",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},
		],
		"submitText":"CLICKING SUBMIT MEANS THAT I, %s, UNDERSTAND AND AGREE TO ALL OF THE ABOVE TERMS",
		"form":"umms_pica_release.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Attest Edited",
		},

	},
}