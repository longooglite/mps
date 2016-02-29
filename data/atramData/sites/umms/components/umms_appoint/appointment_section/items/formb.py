# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

formb = {
	"code": "formb",
	"descr": "Form B",
	"header": "Form B",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": False,
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
