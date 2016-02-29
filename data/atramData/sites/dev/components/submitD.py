# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

submitD = {
	"code": "submitD",
	"descr": "Submit for Approval",
	"header": "Submit for Approval Here",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Packet submitted",
	"className": "Submit",
	"config": {
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
			"activityLogText": "Submitted for Approval",
			"comments": [
				{
					"commentCode": "submitComment",
					"commentLabel": "Comment",
					"accessPermissions": ["submitD_edit"],
					"viewPermissions": ["submitD_view","submitD_edit"],
				},
			],
		},
		"date": True,
		"dateText": "Submit date prompt",
		"dateRequired": True,
	},
}
