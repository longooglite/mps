# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_int_assist_dean_section = {
	"code": "sec_int_assist_dean_section",
	"descr": "Assistant Dean",
	"header": "Assistant Dean",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["sec_int_approval_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["sec_int_assist_dean_packet","assist_dean_approval"]
}
