# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

revise_offer = {
	"code": "revise_offer",
	"comment":"",
	"descr": '''Revise Offer''',
	"header": '''Revise Offer''',
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
	"successMsg":"Revise Offer Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Revise Offer",
		},
		"fileType": "PDF",
		"min": "1",
		"max": "1",
	},
}
