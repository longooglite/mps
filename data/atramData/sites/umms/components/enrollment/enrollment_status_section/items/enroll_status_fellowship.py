# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_status_fellowship = {
	"code": "enroll_status_fellowship",
	"comment":"",
	"descr": "Fellowship Certificate",
	"header": "Fellowship Certificate",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","enroll_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Status Saved",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Fellowship Certificate Status",
		},
	},
}
