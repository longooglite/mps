# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc2_approval_container = {
	"code": "tc2_approval_container",
	"descr": "Approvals",
	"header": "Approvals",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ['tc2_appt_container'],
	"statusMsg": "",
	"className": "Container",
	"containers": ["tc2_approval_blocking_container","tc2_complete_section"]
}
