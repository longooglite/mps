# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

teaching_activity_form = {
	"code": "teaching_activity_form",
	"descr": "Teaching Activity Form",
	"header": "Teaching Activity Form",
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
	"config": {
		"min": "1",
		"max": "1",
	},

}
