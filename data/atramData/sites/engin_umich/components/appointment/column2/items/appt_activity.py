# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

appt_activity = {
	"code": "appt_activity",
	"comment":"",
	"descr": '''Appointment Activity Record (AAR)''',
	"header": '''Appointment Activity Record (AAR)''',
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
	"successMsg":"Appointment Activity Record (AAR) Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Appointment Activity Record (AAR)",
		},
		"min": "1",
		"max": "1",
	},
}
