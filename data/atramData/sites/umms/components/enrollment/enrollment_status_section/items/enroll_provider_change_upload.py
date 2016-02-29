# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_provider_change_upload = {
	"code": "enroll_provider_change_upload",
	"comment":"",
	"descr": "Provider Change Form",
	"header": "Provider Change Form",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task","enroll_task"],
	"viewPermissions": ["dept_task","enroll_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Status Saved",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Enrollment Status Pending",
		},
	},
}
