# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

tc_ofa_packet =  {
	"code": "tc_ofa_packet",
	"descr": "View Track Change Packet",
	"header": "View Track Change Packet",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": [],
	"statusMsg": "",
	"className": "PacketDownload",
	"config": {"add_num_pages_toc_specifier":False,
	           "add_last_page_toc_entry":False,
	           "title":"TRACK CHANGE RECOMMENDATION",
	           "packet_code":"ofa_appt_packet",},
}
