# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

teaching_eval_expl = {
	"code": "teaching_eval_expl",
	"comment":"",
	"descr": '''Teaching Evaluation Explanation''',
	"header": '''Teaching Evaluation Explanation''',
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
	"successMsg":"Teaching Evaluation Explanation Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Teaching Evaluation Explanation",
		},
		"min": "1",
		"max": "1",
	},
}
