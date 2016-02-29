# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

upload_tricare = {
	"code": "upload_tricare",
	"descr": "Upload Signed TriCare Form",
	"header": "Upload Signed TriCare Form",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task","apptCandidate"],
	"viewPermissions": ["dept_task","mss_task""ofa_task","apptCandidate"],
	"blockers": [],
	"containers": [],
    "statusMsg": "",
	"className": "FileUpload",
	"config": {
		"min": "1",
		"max": "1",
	},

}
