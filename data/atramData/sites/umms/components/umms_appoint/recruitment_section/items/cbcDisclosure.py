# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbcDisclosure = {
	"code": "cbcDisclosure",
	"comment":"",
	"descr": "Disclosures",
	"header": "Disclosures",
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
	"successMsg":"Disclosures saved",
	"className": "Disclosure",
	"config": {
		"disclosureGroup":{"code":"CBC","descr":"Background and Education Check Authorization"},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check Disclosures Edited",
		},

		"templateName": "ummscbcdisclosure.html",
		"prompts": [
			{
				"code": "offense",
				"label": "Offense",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "date",
				"label": "Date",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "type",
				"label": "Type of Conviction/Pleas/Disposition",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "location",
				"label": "Location (City, State, Zip)",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "sentence",
				"label": "Sentence / Sanction",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "discharge",
				"label": "Date of Discharge",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
		],
	},
}
