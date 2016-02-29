# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

evpma_packet =  {
	"code": "evpma_packet",
	"descr": "View EVPMA Packet",
	"header": "View EVPMA Packet",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["evpma_auth"],
	"statusMsg": "",
	"className": "PacketDownload",
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"NEW APPOINTMENT RECOMMENDATION",
		"packet_code":"evpma_appt_packet",
		"secondaryApptItems":["sec_confirm_title1","sec_confirm_title2","sec_confirm_title3"],
	},
}
