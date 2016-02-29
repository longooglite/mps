# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

bib_notes = {
	"code": "bib_notes",
	"descr": "Bibliographic Notes",
	"header": "Bibliographic Notes",
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
		"min": "1",
		"max": "1",
	},

}
