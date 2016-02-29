# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

external_solicit = {
	"code": "external_solicit",
	"descr": "External Solicitation Letter Copy",
	"header": "External Solicitation Letter Copy",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"accessPermissions": ["ofa_task","dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": [],
	"containers": [],
    "statusMsg": "",
	"className": "FileUpload",
	"config": {"dashboardEvents": [{
			"code":"arisubmit",
			"eventType":"remove",
		}],
		"min": "1",
		"max": "1",
	},

}
