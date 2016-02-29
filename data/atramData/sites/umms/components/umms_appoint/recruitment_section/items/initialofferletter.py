# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

initialofferletter = {
	"code": "initialofferletter",
	"descr": "Offer Letter",
	"header": "Offer Letter",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"overviewOnly":False,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["confirmtitle","secondary_one","secondary_two","secondary_three"],
	"containers": [],
    "statusMsg": "",
	"className": "FileUpload",
	"config": {
		"dashboardEvents": [{
			"code":"offerstarted",
			"sortOrder":"b30",
			"eventDescription":"Offer Started",
			"eventType":"create",
			"permission":["dept_task"]
		},{
			"code":["sec_rfp1_ofa_approved","sec_rfp2_ofa_approved","sec_rfp3_ofa_approved"],
			"eventType":"remove",
		},],
		"min": "1",
		"max": "1",
	},
}
