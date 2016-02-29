# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbc = {
	"code": "cbc",
	"comment":"",
	"descr": "Background and Education Check",
	"header": "Background and Education Check",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["cbcAdmin","cbcStatus"],
	"viewPermissions": ["cbcView","cbcAdmin","cbcStatus"],
	"isProtectedCandidateItem": False,
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Nothing to see here, move along",
	"className": "BackgroundCheck",
	"config": {
		"backgroundCheckClassName": "UMMSBackgroundCheck",
		"backgroundCheckConfig": {
			"fake": True,
		},

		"activityLog": {
			"enabled": True,
			"activityLogText": "not used, overridden by BackgroundCheck item",
			"comments": [
				{
					"commentCode": "cbcDecisionComment",
					"commentLabel": "Notes on Decision",
					"accessPermissions": ["cbcAdmin","cbcStatus"],
					"viewPermissions": ["cbcAdmin","cbcStatus"],
				},
			],
		},
		"personalInfoTaskCode": "taskF",
		"disclosureTaskCode": "cbcDisclosure",

		"resubmitPermissions": ["cbcView","cbcAdmin","cbcStatus"],
		"resubmitText": "Resubmit to Credential Check",

		"currentReportPermissions": ["cbcAdmin","cbcStatus"],
		"currentReportText": "View Report",

		"storedReportPermissions": ["cbcAdmin","cbcStatus"],
		"storedReportText": "Stored copy of Completed CBC report",

		"decisionPermissions": ["cbcAdmin","cbcStatus"],
		"decisionText": "Decision",
		"acceptText": "Accept",
		"acceptFindingsText": "Accept Findings and Proceed",
		"rejectText": "Reject Hiring",

		"statusPermissions": ["cbcStatus"],

		"rejectFreeze": {
			"freezeJobAction": True,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
		},

		"errorAlert": {
			"alwaysSend": True,
			"sendToDepartment": True,
			"emailTextComplete": "Background and Education Check Submission Error",
		},
		"findingsAlert": {
			"alwaysSend": True,
			"sendToAddresses": ["greg.poth@mountainpasssolutions.com"],
			"emailTextComplete": "Background and Education Check Returned with Findings",
		},
		"completeAlert": {
			"sendToDepartment": True,
			"emailTextComplete": "Background and Education Check Complete",
		},
		"waivedAlert": {
			"sendToDepartment": True,
			"emailTextComplete": "Background and Education Check Waived",
		},

		"findingsDashboardEvents": [
			{
				"code": "cbcfindings",
				"sortOrder": "h1",
				"eventDescription": "Background and Education Check Returned with Findings",
				"eventType": "create",
				"permission": ["cbcAdmin","cbcStatus"]
			},
			{
				"code":"cbccomplete",
				"eventType": "remove",
			},
		],
		"completeDashboardEvents": [
			{
				"code": "cbccomplete",
				"sortOrder": "h2",
				"eventDescription": "Background and Education Check Complete",
				"eventType": "create",
				"permission": ["dept_task"]
			},
			{
				"code":"cbcfindings",
				"eventType": "remove",
			},
		],
	},
}
