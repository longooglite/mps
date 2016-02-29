# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cand_response = {
	"code": "cand_response",
	"comment":"",
	"descr": '''Candidate Response''',
	"header": '''Candidate Response''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["extend_offer"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Candidate Response Complete",
	"className": "Approval",
	"config": {
		"prompts": [
		{
			"code": "approval_date",
			"label": "Date of Response",
			"enabled": True,
			"required": True,
			"data_type": "date",
			"date_format":"M/D/Y"
		}],
		"approve": True,
		"approveDashboardEvents": [],

		"approveText": "Accept",
		"approveStatusMsg": "Offer Accepted",
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
			"activityLogText": "Offer Accepted",
		},
		"deny": True,
		"denyDashboardEvents": [],

		"denyText": "Decline",
		"denyStatusMsg": "Offer Declined",
		"denyFreeze": {
			"freezeJobAction": True,
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
			"activityLogText": "Offer Declined",
		},
		"revisionsRequired": False,
		"activityLog": {
			"enabled": True,
			"activityLogText": "Candidate Response",
			"comments": [],
		},
		"vote": False,
		"date": True,
		"dateText": "Date of Response",
		"dateRequired": True,
	},
}
