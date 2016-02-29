# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

confirmtitle = {
	"code": "confirmtitle",
	"comment":"",
	"descr": "Confirm Title",
	"header": "Confirm Title",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"overviewOnly":False,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["identifycandidate","sas_rfp_section","sec_int_rfp_section","sec_ext_rfp_section"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Title confirmed",
	"className": "ConfirmTitle",
	"config": {
		"dashboardEvents": [{
			"code":["sec_rfp_ofa_approved"],
			"eventType":"remove",
		},],
		"activityLog": {
			"enabled": True,
			"activityLogText": "Title Confirmed",
		},
	},
}
