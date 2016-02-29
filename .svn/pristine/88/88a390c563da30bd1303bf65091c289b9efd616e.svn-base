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
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task"],
	"blockers": [],
	"statusMsg": "",
	"successMsg":"Candidate information submitted",
	"className": "SubmitBackgroundCheck",
	"config": {
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
		},{
			"code":"awaitingCandidate",
			"eventType":"remove",
		}],
		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Candidate Information Submitted",
			"comments": [
				{
					"commentCode": "candidateSubmitRFP",
					"commentLabel": "Comments",
					"accessPermissions": ["apptCandidate","ofa_task","dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},

		"cbcTaskName": "cbc",
	},
}
