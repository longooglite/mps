# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

revise_grid = {
	"code": "revise_grid",
	"comment":"",
	"descr": '''Revise Startup Grid''',
	"header": '''Revise Startup Grid''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["cand_response"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Revise Startup Grid Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Revise Startup Grid",
		},
		"fileType": "PDF",
		"min": "1",
		"max": "1",
	},
}
