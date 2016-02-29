# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

backgroundcheckplaceholder = {
	"code": "backgroundcheckplaceholder",
	"comment":"",
	"descr": "Background and Education Check Authorization (placeholder)",
	"header": "Background and Education Check Authorization (placeholder)",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"isProtectedCandidateItem":True,
	"blockers": ["startappointment"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Background check consent was saved",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Background Check Placeholder",
		},
	},
}
