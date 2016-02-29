# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promocv = {
	"code": "promocv",
	"comment":"",
	"descr": '''Curriculum Vitae''',
	"header": '''Curriculum Vitae''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task","appt_candidate"],
	"viewPermissions": ["dept_task","ofa_task","appt_candidate"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Curriculum Vitae Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Curriculum Vitae",
		},
		"min": "1",
		"max": "1",
	},
}
