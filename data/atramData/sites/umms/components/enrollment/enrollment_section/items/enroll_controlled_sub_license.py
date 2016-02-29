# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_controlled_sub_license = {
	"code": "enroll_controlled_sub_license",
	"comment":"",
	"descr": "MI Controlled Substance License",
	"header": "MI Controlled Substance License",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task","apptCandidate"],
	"viewPermissions": ["dept_task","enroll_task","ofa_task","apptCandidate"],
	"isProtectedCandidateItem":True,
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"className": "FileUpload",
	"config": {
		"min": "1",
		"max": "1",
	},
}
