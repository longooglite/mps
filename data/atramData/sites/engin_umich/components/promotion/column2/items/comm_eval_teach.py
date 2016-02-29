# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

comm_eval_teach = {
	"code": "comm_eval_teach",
	"comment":"",
	"descr": '''Committee Evaluation of Teaching''',
	"header": '''Committee Evaluation of Teaching''',
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
	"successMsg":"Committee Evaluation of Teaching Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Committee Evaluation of Teaching",
		},
		"min": "1",
		"max": "1",
	},
}
