# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_deans_letter = {
	"code": "promo_deans_letter",
	"comment":"",
	"descr": '''Dean's Letter of Support''',
	"header": '''Dean's Letter of Support''',
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
	"successMsg":"Dean's Letter of Support Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Dean's Letter of Support",
		},
		"min": "1",
		"max": "1",
	},
}
