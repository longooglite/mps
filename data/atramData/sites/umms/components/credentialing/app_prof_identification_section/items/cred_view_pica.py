# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_view_pica = {
	"code": "cred_view_pica",
	"comment":"",
	"descr": "View Professional Competency Evaluation",
	"header": "View Professional Competency Evaluation",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task","mss_task"],
	"viewPermissions": ["dept_task","mss_task","ofa_task"],
	"isProtectedCandidateItem":True,
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "View Professional Competency Evaluation Placeholder",
		},
	},
}
