# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

assist_dean_packet =  {
	"code": "assist_dean_packet",
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
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"NEW APPOINTMENT RECOMMENDATION",
		"packet_code":"assist_dean_appt_packet"},
		"secondaryApptItems":["sec_confirm_title1","sec_confirm_title2","sec_confirm_title3"],
}
