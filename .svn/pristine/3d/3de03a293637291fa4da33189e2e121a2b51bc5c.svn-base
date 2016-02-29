# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

approverfp = {
	"code": "approverfp",
	"descr": "Approve RFP",
	"header": "Approve RFP",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ['ofa_task'],
	"viewPermissions": ['ofa_task',"mss_task"],
	"overviewOnly":True,
	"blockers": ["submitrfp"],
	"statusMsg": "",
	"successMsgApprove":"RFP approved",
	"successMsgDeny":"RFP denied",
	"successMsgRevisions":"RFP revisions required",
	"className": "Approval",
	"config": {
		"alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"RFP Approved",
			"emailTextRevisions":"RFP Revisions Required",
		},
		"approveDashboardEvents": [{
			"code":"rfpsubmit",
			"eventType":"remove",
		},{
			"code":"rfprevisions",
			"eventType":"remove",
		},{
			"code":"rfpapproved",
			"sortOrder":"a1",
			"eventDescription":"RFP Approved",
			"eventType":"create",
			"permission":["dept_task"]
		},{
			"code":"readyforjobposting",
			"sortOrder":"b10",
			"eventDescription":"Awaiting Job Posting",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"approve": True,
		"approveText": "Approve",
		"approveStatusMsg": "RFP Approved",
		"approveFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "RFP Approved",
		},
		"deny": True,
		"confirmDeny":True,
		"denyText": "Deny",
		"denyStatusMsg": "RFP Denied",
		"denyDashboardEvents": [{
			"code":"rfpsubmit",
			"eventType":"remove",
		},{
			"code":"rfpdenied",
			"sortOrder":"a3",
			"eventDescription":"RFP Denied",
			"eventType":"create",
			"permission":["dept_task"]
		}],
		"denyFreeze": {
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
			"activityLogText": "RFP Denied",
		},
		"revisionsRequired": True,
		"revisionsRequiredText": "RFP Revisions Required",
		"revisionsRequiredStatusMsg": "RFP Revisions Required",
		"revisionsDashboardEvents": [{
			"code":"rfpsubmit",
			"eventType":"remove",
		},{
			"code":"rfprevisions",
			"sortOrder":"a2",
			"eventDescription":"RFP Revisions Required",
			"eventType":"create",
			"permission":["dept_task"]
		}],
		"revisionsRequiredFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["submitrfp"],
			"unfreezeOptions": ["rfp"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "submitrfp",
			"activityLogText": "RFP Revisions Required",
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "RFP Approved",
			"comments": [
				{
					"commentCode": "rfpCommentEverybody",
					"commentLabel": "Comment",
					"accessPermissions": ["approverfp_edit"],
					"viewPermissions": ["approverfp_view","approverfp_edit"],
				},
			],
		},
		"activityLogTaskCodes": ["approverfp","submitrfp"],
		"vote": False,
	},
}
