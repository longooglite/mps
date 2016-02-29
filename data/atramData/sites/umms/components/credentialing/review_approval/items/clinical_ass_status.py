# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

clinical_ass_status = {
	"code": "clinical_ass_status",
	"comment":"",
	"descr": "Clinical Assessments",
	"header": "Clinical Assessments",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["mss_task"],
	"viewPermissions": ["dept_task","mss_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Clinical Assessments Status was saved",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Clinical Assessments Status",
		},
	},
}
