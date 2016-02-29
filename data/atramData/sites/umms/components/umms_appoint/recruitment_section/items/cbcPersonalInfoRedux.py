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
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"isProtectedCandidateItem":False,
	"blockers": ["startappointment","personalinfo","cbcGeneral","cbcConsent","cbcDisclosure","cbcConditional","cbcRights"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Personal and Education Summary was saved",
	"className": "PersonalInfoSummary",
	"config": {
		"disclosureGroup":{"code":"CBC","descr":"Background and Education Check Authorization"},
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

		"personalInfoTaskCode": "personalinfo",
		"personalInfoSummaryConfig": [
			{ 'section': 'piNameSection', 'title': 'Name Information' },
			{ 'section': 'piHighDegreeSection', 'title': 'Highest Degree Obtained' },
			{ 'section': 'piOtherSection', 'title': 'Other Information' },
			{ 'section': 'piContactSection', 'title': 'Current Contact Information' },
		],
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check PE Redux Confirmed",
		},
	},
}
