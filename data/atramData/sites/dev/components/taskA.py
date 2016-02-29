# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

taskA = {
	"code": "taskA",
	"descr": "Task A",
	"header": "Task A",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": [],
	"viewPermissions": ["viewA"],
	"blockers": [],
	"statusMsg": "'A' is done",
	"className": "FileUpload",
	"config": {
		"min": "1",
		"max": "1",
		"alert": {
			"sendToUser":True,
			"sendToDepartment":False,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":["your.name.here@google.com"],
			"sendToBCCAddresses":[]
		},
		"createDashboardEvents": [{
			"code":"taskA",
			"sortOrder":"a1",
			"eventDescription":"Task A File uploaded",
			"eventType":"create",
			"permission":["taskA_dashboard"]
		}],
		"deleteDashboardEvents": [{
			"code":"taskA",
			"eventType":"remove",
		}],
		"activityLog": {
			"enabled": False,
			"activityLogText": "FileUpload",
		},
		"emails": [{
			"sendToUser":True,
			"sendToDepartment":False,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"subject":"Hey There",
			"bodyTemplateName":"candidate.html",
		}],
	},
}
