# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_status_med_school_diploma = {
	"code": "enroll_status_med_school_diploma",
	"comment":"",
	"descr": "Medical School Diploma",
	"header": "Medical School Diploma",
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
			"activityLogText": "Medical School Diploma Status",
		},
	},
}
