# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

doc_serv_comm_eval = {
	"code": "doc_serv_comm_eval",
	"comment":"",
	"descr": '''Committee Evaluation of Service''',
	"header": '''Committee Evaluation of Service''',
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
	"successMsg":"Committee Evaluation of Service Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Committee Evaluation of Service",
		},
		"min": "1",
		"max": "1",
	},
}
