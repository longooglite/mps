# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_doc_status_section = {
	"code": "enroll_doc_status_section",
	"descr": "Enrollment Document Status",
	"header": "Enrollment Document Status",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": ["enroll_status_mi_license","enroll_status_controlled_substance","enroll_status_dea_license",
	               "enroll_status_board_cert","enroll_status_fellowship","enroll_status_med_school_diploma"]
}
