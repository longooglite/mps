# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

vp_research_packet =  {
	"code": "vp_research_packet",
	"descr": "View Vice-President for Research Packet",
	"header": "View Vice-President for Research Packet",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["evpma_vote","promo_evpma_vote"],
	"statusMsg": "",
	"className": "PacketDownload",
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"NEW APPOINTMENT RECOMMENDATION",
		"packet_code":"vp_research_appt_packet",
		"secondaryApptItems":["sec_confirm_title1","sec_confirm_title2","sec_confirm_title3"]
	},
}
