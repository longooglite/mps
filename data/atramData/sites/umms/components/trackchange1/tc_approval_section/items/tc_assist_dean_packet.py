# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc_assist_dean_packet =  {
	"code": "tc_assist_dean_packet",
	"descr": "View Assistant Dean Packet",
	"header": "View Assistant Dean Packet",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["ofa_task","assist_dean_task"],
	"viewPermissions": ["ofa_task","assist_dean_task"],
	"blockers": ["approveOFA"],
	"statusMsg": "",
	"className": "PacketDownload",
	"config": {"add_num_pages_toc_specifier":False,
	           "add_last_page_toc_entry":False,
	           "title":"TRACK CHANGE RECOMMENDATION",
	           "packet_code":"tc1_assist_dean_appt_packet",},
}
