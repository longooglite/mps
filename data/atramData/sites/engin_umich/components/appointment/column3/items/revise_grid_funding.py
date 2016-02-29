# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

revise_grid_funding = {
	"code": "revise_grid_funding",
	"comment":"",
	"descr": '''Update Grid with Provost Funding''',
	"header": '''Update Grid with Provost Funding''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["adaa_approve_grid"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Update Grid with Provost Funding Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Update Grid with Provost Funding",
		},
		"min": "1",
		"max": "1",
	},
}
