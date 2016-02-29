# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_background_check = {
	"code": "cred_background_check",
	"comment":"",
	"descr": "Background and Education Check",
	"header": "Background and Education Check",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task","ofa_task",'mss_task'],
	"isProtectedCandidateItem":True,
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "",
		},
	},
}
