# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cbc = {
	"code": "cbc",
	"comment":"",
	"descr": "Background and Education Check Approval",
	"header": "Background and Education Check Approval",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["cbcView","cbcAdmin","cbcStatus"],
	"viewPermissions": ["dept_task","cbcView","cbcAdmin","cbcStatus","mss_task"],
	"overviewOnly": True,
	"isProtectedCandidateItem": False,
	"blockers": ["candidatesubmit"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
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
		"personalInfoTaskCode": "personalinfo",
		"personalInfoSummaryConfig": [
			{ 'section': 'piNameSection', 'title': 'Name Information' },
			{ 'section': 'piHighDegreeSection', 'title': 'Highest Degree Obtained' },
			{ 'section': 'piOtherSection', 'title': 'Other Information' },
			{ 'section': 'piContactSection', 'title': 'Current Contact Information' },
		],
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
		"parentCode": "cbc",

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
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "",
		},

		"errorAlert": {
			"alwaysSend": True,
			"sendToDepartment": True,
			"emailTextComplete": "Background and Education Check Submission Error",
		},
		"findingsAlert": {
			"alwaysSend": True,
			"sendToAddresses": ["greg.poth@gomountainpass.com"],
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

		"emails": [{
			"workflow_dependency":"CREDENTIAL",
			"sendToCandidate":True,
			"sendToUser":False,
			"sendToDepartment":False,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"subject":"Welcome to the University of Michigan Medical School Credentialing Process",
			"bodyTemplateName":"credentialing_start.html",
		}],

		"submitDashboardEvents": [
			{
				"code":"cbccomplete",
				"eventType": "remove",
			},
			{
				"code":"awaitingbackgroundcheck",
				"eventType": "remove",
			},
		],
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
			{
				"code":"candidatesubmission",
				"eventType": "remove",
			},
			{
				"code":"awaitingbackgroundcheck",
				"eventType": "remove",
			},
		],
		"completeDashboardEvents": [
			{
				"code": "cbccomplete",
				"sortOrder": "h2",
				"eventDescription": "Background and Education Check Approval Complete",
				"eventType": "create",
				"permission": ["dept_task"]
			},
			{
				"code":"cbcfindings",
				"eventType": "remove",
			},
			{
				"code":"candidatesubmission",
				"eventType": "remove",
			},
			{
				"code":"awaitingbackgroundcheck",
				"eventType": "remove",
			},
		],
	},
}
