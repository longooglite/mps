# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_int_mou = {
	"code": "sec_int_mou",
	"descr": "Memorandum of Understanding (MOU)",
	"header": "Memorandum of Understanding (MOU)",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task"],
	"blockers": ["confirmtitle","secondary_one","secondary_two","secondary_three"],
	"containers": [],
    "statusMsg": "",
	"className": "FileUpload",
	"config": {
		"min": "1",
		"max": "1",
	},

}
