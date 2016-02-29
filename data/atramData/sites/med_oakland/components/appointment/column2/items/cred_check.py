# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_check = {
	"code": "cred_check",
	"comment":"",
	"descr": '''Check Credentialing''',
	"header": '''Check Credentialing''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["dcapt_approval_section"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Check Credentialing Complete",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Check Credentialing",
		},
	},
}
