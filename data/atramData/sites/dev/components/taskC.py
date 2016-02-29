# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

taskC = {
	"code": "taskC",
	"descr": "Task C",
	"header": "Task C",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": [],
	"viewPermissions": ["viewC"],
	"blockers": [],
	"statusMsg": "C is Done",
	"className": "FileUpload",
	"config": {
		"min": "1",
		"max": "1",
		"alert": {
			"sendToUser":False,
			"sendToDepartment":False,
			"sendToSitePref":["facultyaffairsemail"],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[]
		},
		"createDashboardEvents": [{
			"code":"taskA",
			"eventType":"remove",
		}]
	},
}
