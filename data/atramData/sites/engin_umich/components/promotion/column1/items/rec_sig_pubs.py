# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

rec_sig_pubs = {
	"code": "rec_sig_pubs",
	"comment":"",
	"descr": '''Recent Significant Publications''',
	"header": '''Recent Significant Publications''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task","appt_candidate"],
	"viewPermissions": ["dept_task","ofa_task","appt_candidate"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Recent Significant Publications Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Recent Significant Publications",
		},
		"min": "1",
		"max": "1",
	},
}
