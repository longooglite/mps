# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

recent_sig_pubs = {
	"code": "recent_sig_pubs",
	"descr": "Recent Significant Publications",
	"header": "Recent Significant Publications",
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
	"config": {
		"dashboardEvents": [{
			"code":"candidatesubmission",
			"eventType":"remove",
		},{
			"code":"arisubmit",
			"eventType":"remove",
		}],
		"min": "5",
		"max": "5",
	},

}
