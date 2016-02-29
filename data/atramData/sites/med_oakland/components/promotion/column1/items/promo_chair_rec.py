# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_chair_rec = {
	"code": "promo_chair_rec",
	"comment":"",
	"descr": '''Department Chair Recommendation Letter''',
	"header": '''Department Chair Recommendation Letter''',
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
	"successMsg":"Department Chair Recommendation Letter Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Department Chair Recommendation Letter",
		},
		"min": "1",
		"max": "1",
	},
}
