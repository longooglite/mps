# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

provost_approval = {
	"code": "provost_approval",
	"comment":"",
	"descr": '''Provost Approval''',
	"header": '''Provost Approval''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Provost Approval Complete",
	"className": "Approval",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Provost Approval",
			"comments": [
				{
					"commentCode": "provostApprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
		"approve": True,
		"approveDashboardEvents": [],
		"denyDashboardEvents": [],
		"revisionsDashboardEvents": [],

		"approveText": "Approve",
		"approveStatusMsg": "Approved by Provost",
		"approveFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Approved",
		},
		"deny": True,

		"denyText": "Deny",
		"denyStatusMsg": "TBD",
		"denyFreeze": {
			"confirmDeny":True,
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
			"activityLogText": "Denied",
		},
		"revisionsRequired": True,
		"revisionsRequiredText": "Revisions Required",
		"revisionsRequiredStatusMsg": "Revisions Required",
		"revisionsRequiredFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["submit_offer_adaa"],
			"unfreezeOptions": ["posting_waiver","job_posting_info","identify_candidate","confirm_title","cv","significant_pubs","pre_approval","acad_eval","research_statement","teaching_statement","teaching_eval","teaching_eval_expl","college_rep_eval","cover_search_comm","appt_activity","cover_letter_chair","draft_offer1","deans_cover"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "submit_offer_adaa",
			"activityLogText": "Revisions Required",
		},
		"vote": False,
	},
}
