# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

provost_promo_packet =  {
	"code": "provost_promo_packet",
	"descr": "View Provost Packet",
	"header": "View Provost Packet",
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
	"config": {"add_num_pages_toc_specifier":True,
	           "add_last_page_toc_entry":True,
	           "title":"PROMOTION RECOMMENDATION",
	           "packet_code":"prov_promo_packet",
	           "secondaryPromoItem":"manage_joint_promotions"},
}
