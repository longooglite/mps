# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_int_approval_section = {
	"code": "sec_int_approval_section",
	"descr": "OFA Approval",
	"header": "OFA Approval",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["submitOFA"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["sec_int_ofa_packet","approveOFA"]
}
