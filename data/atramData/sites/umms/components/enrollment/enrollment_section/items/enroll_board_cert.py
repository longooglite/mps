# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_board_cert = {
	"code": "enroll_board_cert",
	"comment":"",
	"descr": "Board Certificate or Eligibility Letter or Residency Certificate",
	"header": "Board Certificate or Eligibility Letter or Residency Certificate",
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
