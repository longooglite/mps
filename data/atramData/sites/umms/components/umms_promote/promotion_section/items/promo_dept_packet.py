# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_dept_packet =  {
	"code": "promo_dept_packet",
	"descr": "View Promotion Packet",
	"header": "View Promotion Packet",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task"],
	"blockers": [],
	"statusMsg": "",
	"className": "PacketDownload",
	"config": {"add_num_pages_toc_specifier":False,
	           "add_last_page_toc_entry":False,
	           "title":"PROMOTION RECOMMENDATION",
	           "packet_code":"ofa_appt_packet",
	           "secondaryPromoItem":"manage_joint_promotions"},
}
