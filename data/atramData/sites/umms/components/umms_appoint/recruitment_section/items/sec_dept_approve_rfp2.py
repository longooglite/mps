# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_dept_approve_rfp2 = {
	"code": "sec_dept_approve_rfp2",
	"descr": "Department Approval for Secondary RFP",
	"header": "Department Approval for Secondary RFP",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ['dept_task'],
	"viewPermissions": ['ofa_task','dept_task',"mss_task"],
	"overviewOnly":True,
	"blockers": ["sec_submit_rfp2"],
	"statusMsg": "",
	"successMsgApprove":"Secondary RFP approved",
	"successMsgDeny":"Secondary RFP denied",
	"successMsgRevisions":"Secondary RFP revisions required",
	"className": "Approval",
	"config": {
		"approveDashboardEvents": [{
			"code":["sec_submit_rfp2"],
			"eventType":"remove",
		},{
			"code":"sec_rfp_ofa_approve2",
			"sortOrder":"d1",
			"eventDescription":"Secondary RFP Awaiting Approval",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"denyDashboardEvents": [{
			"code":"sec_submit_rfp2",
			"eventType":"remove",
		},{
			"code":"sec_rfp2_denied",
			"sortOrder":"d3",
			"eventDescription":"Secondary RFP Denied",
			"eventType":"create",
			"department":"primary",
			"permission":["dept_task"]
		}],
		"revisionsDashboardEvents": [{
			"code":["sec_submit_rfp2"],
			"eventType":"remove",
		},{
			"code":"sec_rfp2_revisions",
			"sortOrder":"d2",
			"eventDescription":"Secondary RFP Revisions Required",
			"eventType":"create",
			"department":"primary",
			"permission":["dept_task"]
		}],

		"disclosureGroup":{"code":"sec2","descr":"2nd Secondary Appointment"},
		"approve": True,
		"approveText": "Approve",
		"approveStatusMsg": "Secondary RFP Approved",
		"approveFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": False,
			"freezeTasks": ["sec_rfp2","sec_confirm_title2","sec_submit_rfp2"],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Secondary RFP Approved",
		},
		"deny": True,
		"denyIsNotDone":"True",
		"confirmDeny":True,
		"denyText": "Deny",
		"denyStatusMsg": "Secondary RFP Denied",
		"denyFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": ["sec_rfp2","sec_confirm_title2","sec_submit_rfp2","sec_dept_approve_rfp2"],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Secondary RFP Denied",
		},
		"revisionsRequired": True,
		"revisionsRequiredText": "Secondary RFP Revisions Required",
		"revisionsRequiredStatusMsg": "Secondary RFP Revisions Required",
		"revisionsRequiredFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["sec_submit_rfp2"],
			"unfreezeOptions": ["sec_confirm_title2","sec_rfp2"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "sec_submit_rfp2",
			"activityLogText": "Secondary RFP Revisions Required",
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Secondary RFP Approved",
			"comments": [
				{
					"commentCode": "sec2rfpCommentEverybody",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task"],
					"viewPermissions": ["dept_task","ofa_task"],
				},
			],
		},
		"activityLogTaskCodes": ["sec_dept_approve_rfp2","sec_submit_rfp2"],
		"vote": False,
	},
}
