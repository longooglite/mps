# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

candidatesubmit = {
	"code": "candidatesubmit",
	"descr": "Submit Candidate Items",
	"header": "Submit Candidate Items",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":False,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"blockers": ["personalinfo","ari","cbcGeneral","cbcConsent","cbcDisclosure","cbcConditional","cbcRights","cbcPersonalInfoRedux","npi"],
	"statusMsg": "Offer submitted",
	"successMsg":"Candidate information submitted",
	"className": "SubmitBackgroundCheck",
	"config": {
		"instructional":"Please make sure everything you have entered is accurate then press submit to finalize your entries.",
		"alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"Candidate Submissions Complete",
		},
		"dashboardEvents": [{
			"code":"candidatesubmission",
			"sortOrder":"g1",
			"eventDescription":"Candidate Submission Complete",
			"eventType":"create",
			"permission":["dept_task"]
		},
		{
			"code":"awaitingbackgroundcheck",
			"sortOrder":"g1",
			"eventDescription":"Awaiting Background Check",
			"eventType":"create",
			"permission":["ofa_task"]
		},{
			"code":"awaitingCandidate",
			"eventType":"remove",
		}],
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
			"clearJobActionRevisionsRequired": False,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Candidate Information Submitted",
			"comments": [
				{
					"commentCode": "candidateSubmitRFP",
					"commentLabel": "Comments",
					"accessPermissions": ["apptCandidate"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},

		"cbcTaskName": "cbc",
	},
}
