# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

fa_packet_section = {
	"code": "fa_packet_section",
	"descr": "Submit to OFA",
	"header": "Submit to OFA",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": True,
	"enabled": True,
	"accessPermissions": ["ofa_task","dept_task"],
	"viewPermissions": ["ofa_task","dept_task"],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": ["fa_packet","submitOFA"]
}
