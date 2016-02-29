# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

extend_offer = {
	"code": "extend_offer",
	"comment":"",
	"descr": '''Extend Offer''',
	"header": '''Extend Offer''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["approve_offer"],
	"containers": [],
	"statusMsg": "Offer extended to candidate",
	"successMsg":"Extend Offer Complete",
	"className": "Submit",
	"config": {
		"dashboardEvents": [],

		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": False,
		},

		"date": True,
		"dateText": "Date Extended",
		"dateRequired": True,
		"prompts": [
			{
				"code": "approval_date",
				"label": "Date Extended",
				"enabled": True,
				"required": True,
				"data_type": "date",
				"date_format":"M/D/Y"
		}],
	},
}
