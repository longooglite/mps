# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

appoint_approval_container = {
	"code": "appoint_approval_container",
	"descr": "Approvals",
	"header": "Approvals",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ['recruitment_container','appointment_container'],
	"statusMsg": "",
	"className": "Container",
	"containers": ["approval_blocking_container","complete_section"]
}
