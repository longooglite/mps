# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_upload_image_id = {
	"code": "cred_upload_image_id",
	"comment":"",
	"descr": "Upload Representative Personal Image",
	"header": "Upload Representative Personal Image",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","apptCandidate"],
	"viewPermissions": ["dept_task","apptCandidate","mss_task","ofa_task"],
	"isProtectedCandidateItem":True,
	"blockers": ["cred_application_submit"],
	"containers": [],
	"statusMsg": "",
	"className": "FileUpload",
	"config": {
		"fileType":"image",
		"min": "1",
		"max": "1",
	},
}
