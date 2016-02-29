# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_confirm_title1 = {
	"code": "sec_confirm_title1",
	"comment":"",
	"descr": "Confirm Department and Title",
	"header": "Confirm Department and Title",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"overviewOnly":False,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Title confirmed",
	"className": "ConfirmTitle",
	"config": {
		"secondaryAppointmentMode":True,
		"disclosureGroup":{"code":"sec1","descr":"1st Secondary Appointment"},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Title Confirmed",
		},
	},
}
