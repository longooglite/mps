# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_attestation = {
	"code": "cred_attestation",
	"comment":"",
	"descr": "Attestation",
	"header": "Attestation",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"freezable": True,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"blockers": ["app_blocking_container"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Attestation was saved",
	"className": "Attest",
	"config":
	{
		"dashboardEvents": [{
			"code":"credattest",
			"sortOrder":"a1",
			"eventDescription":"Attestation Complete",
			"eventType":"create",
			"permission":["mss_task"]
		},],

		"clearFieldLevelRevisions":True,
		"clearFieldLevelContainers":["cred_personalinfo","cred_edu_training","cred_work_experience","cred_board_cert","cred_licensure","cred_prof_liability","cred_suppl_questions"],
		"parentCode": "ari",
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
		"form":"umms_cred_attest.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Attest Edited",
		},
		"freezeText": "Attest",
		"freezeStatusMsg": "Candidate Attested",
		"freeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": False,
			"freezeTasks": ["cred_personalinfo","cred_edu_training","cred_work_experience","cred_board_cert","cred_licensure","cred_prof_liability","cred_suppl_questions"],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "",
			"activityLogText": "Attested",
		},

		"uberGapsConfig": [
			{
				"enabled": True,
				"taskList": [
					{
						"taskCode": "cred_edu_training",
						"startDateIdentifierCode": "start_date",
						"endDateIdentifierCode": "end_date",
					},
					{
						"taskCode": "cred_work_experience",
						"startDateIdentifierCode": "start_date",
						"endDateIdentifierCode": "end_date",
					},
				],
				"nbrDays": 60,
				"descr": "Education/Training and Work Experience",
			},
			{
				"enabled": True,
				"taskList": [
					{
						"taskCode": "cred_prof_liability",
						"startDateIdentifierCode": "start_date",
						"endDateIdentifierCode": "end_date",
					},
				],
				"nbrDays": 60,
				"descr": "Professional Liability Insurance",
			},
		],
		"uberGapsEnforced": True,
		"uberGapsEnforcedText": "The Credentialing Application may not be submitted until the following gaps are resolved:",
		"uberGapsPrintIntroText": "The following gaps were identified in the Credentialing Application:",
	},
}
