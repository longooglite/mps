# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_adaa_approval = {
	"code": "promo_adaa_approval",
	"comment":"",
	"descr": '''ADAA Approval''',
	"header": '''ADAA Approval''',
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
	"statusMsg": "Promotion approved by ADAA",
	"successMsg":"ADAA Approval Complete",
	"className": "Approval",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "ADAA Approval",
			"comments": [
				{
					"commentCode": "promoAdaaApprovalComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task","dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
		"approve": True,
		"approveDashboardEvents": [],
		"denyDashboardEvents": [],
		"revisionsDashboardEvents": [],

		"approveText": "Approve",
		"approveStatusMsg": "",
		"approveFreeze": {
			"freezeJobAction": False,
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
			"unfreezeTasks": ["promo_submit_adaa"],
			"unfreezeOptions": ["promocv","journal_ranking","rec_sig_pubs","ref_list","req_participate","manage_evals","comm_eval_teach","comparison_report","impact_eval","promo_journal_rank","doc_serv_comm_eval","promo_chair_letter","letters_from_comm","memorandum_from_review","joint_letter","promo_rec","promo_approv_chair_letter","comm_eval_teach"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "promo_submit_adaa",
			"activityLogText": "Revisions Required",
		},
		"vote": False,
	},
}