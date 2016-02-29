# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

regent_record_date = {
	"code": "regent_record_date",
	"comment":"",
	"descr": '''Record Date Submitted''',
	"header": '''Record Date Submitted''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["revise_grid_dept_approval","revise_grid_adaa_approval"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Date Submitted",
	"className": "Submit",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Record Date Submitted",
			"comments": [
				{
					"commentCode": "regentRecordDateComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
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
	},
}
