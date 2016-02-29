# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

complete_ppap_forms = {
	"code": "complete_ppap_forms",
	"comment":"",
	"descr": '''Submit PPAP Form(s)''',
	"header": '''Submit PPAP Form(s)''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["send_ppap_forms"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Submit PPAP Form(s) Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Submit PPAP Form(s)",
		},
		"min": "1",
		"max": "1",
	},
}
