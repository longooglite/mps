# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

extendoffer = {
	"code": "extendoffer",
	"descr": "Extend Offer",
	"header": "Extend Offer",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ['approveoffer'],
	"overviewOnly":False,
	"statusMsg": "Offer Extended",
	"successMsg": "Offer extended",
	"className": "Submit",
	"config": {
		"dashboardEvents": [{
			"code":"offerextended",
			"sortOrder":"d1",
			"eventDescription":"Offer Extended",
			"eventType":"create",
			"permission":["dept_task"]
		},{
			"code":"offerapproved",
			"eventType":"remove",
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
			"clearJobActionRevisionsRequired": False,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Offer Extended",
			"comments": [],
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
