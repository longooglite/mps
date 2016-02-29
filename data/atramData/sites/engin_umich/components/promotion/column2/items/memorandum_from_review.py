# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

memorandum_from_review = {
	"code": "memorandum_from_review",
	"comment":"",
	"descr": '''Memorandum from Review Committee to the Candidate''',
	"header": '''Memorandum from Review Committee to the Candidate''',
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
	"successMsg":"Memorandum from Review Committee to the Candidate Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Memorandum from Review Committee to the Candidate",
		},
		"min": "1",
		"max": "1",
	},
}
