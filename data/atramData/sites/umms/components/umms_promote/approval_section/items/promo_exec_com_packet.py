# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_exec_com_packet =  {
	"code": "promo_exec_com_packet",
	"descr": "View Executive Committee Packet",
	"header": "View Executive Committee Packet",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["approveOFA"],
	"statusMsg": "",
	"className": "PacketDownload",
	"config": {"add_num_pages_toc_specifier":False,
	           "add_last_page_toc_entry":False,
	           "title":"PROMOTION RECOMMENDATION",
	           "packet_code":"exec_com_appt_packet",
	           "secondaryPromoItem":"manage_joint_promotions"},
}
