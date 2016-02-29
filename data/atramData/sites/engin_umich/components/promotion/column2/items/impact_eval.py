# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

impact_eval = {
	"code": "impact_eval",
	"comment":"",
	"descr": '''Evaluation of Research and Impact''',
	"header": '''Evaluation of Research and Impact''',
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
	"statusMsg": "",
	"successMsg":"Evaluation of Research and Impact Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Evaluation of Research and Impact",
		},
		"min": "1",
		"max": "1",
	},
}
