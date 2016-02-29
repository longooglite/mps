# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

bot_record_result = {
	"code": "bot_record_result",
	"comment":"",
	"descr": '''Complete Personnel Action/Record Date Submitted''',
	"header": '''Complete Personnel Action/Record Date Submitted''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "Submitted to BOT",
	"successMsg":"Complete Personnel Action/Record Date Submitted Complete",
	"className": "Submit",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Complete Personnel Action/Record Date Submitted Submitted",
			"comments": [
				{
					"commentCode": "botRecordResultComment",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task","ofa_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
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
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
		},
	},
}
