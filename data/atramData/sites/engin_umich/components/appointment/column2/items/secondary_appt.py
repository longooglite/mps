# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

secondary_appt = {
	"code": "secondary_appt",
	"comment":"",
	"descr": '''Manage Secondary Appointments''',
	"header": '''Manage Secondary Appointments''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Manage Secondary Appointments Complete",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Manage Secondary Appointments",
		},
	},
}
