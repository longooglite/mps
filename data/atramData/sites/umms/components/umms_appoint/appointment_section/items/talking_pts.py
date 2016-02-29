# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

talking_pts = {
	"code": "talking_pts",
	"descr": "Talking Points",
	"header": "Talking Points",
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
