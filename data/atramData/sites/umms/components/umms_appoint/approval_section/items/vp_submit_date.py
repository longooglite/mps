# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

vp_submit_date = {
	"code": "vp_submit_date",
	"descr": "Record Date Submitted",
	"header": "Record Date Submitted",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":False,
	"accessPermissions": ['ofa_task'],
	"viewPermissions": ['ofa_task'],
	"blockers": ["approveOFA","provost_vote","evpma_vote","exec_com_vote","approveOFA","promo_provost_vote","promo_evpma_vote","promo_exec_com_vote"],
	"statusMsg": "",
	"successMsg": "Vice President of Research date recorded",
	"className": "Submit",
	"config": {
		"date": True,
		"dateText": "Date Submitted",
		"dateRequired": True,
		"prompts": [
			{
				"code": "approval_date",
				"label": "Date Submitted",
				"enabled": True,
				"required": True,
			    "data_type": "date",
				"date_format":"M/D/Y"
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
			"clearJobActionRevisionsRequired": True,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Record Date Submitted to Vice President for Research",
			"comments": [
				{
					"commentCode": "evpma_submit_date",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
	},
}
