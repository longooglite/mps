# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc_approval_section = {
	"code": "tc_approval_section",
	"descr": "OFA Approval",
	"header": "OFA Approval",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": ["tc_ofa_packet","approveOFA"]
}
