# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc_ofa_packet_section = {
	"code": "tc_ofa_packet_section",
	"descr": "Submit to OFA",
	"header": "Submit to OFA",
	"componentType": "Container",
	"affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["tc_appt_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["tc_view_packet","submitOFA"]
}
