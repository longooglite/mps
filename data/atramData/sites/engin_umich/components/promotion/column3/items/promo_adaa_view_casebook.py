# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_adaa_view_casebook = {
	"code": "promo_adaa_view_casebook",
	"comment":"",
	"descr": '''View Promotion Casebook''',
	"header": '''View Promotion Casebook''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"View Promotion Casebook Complete",
	"className": "PacketDownload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "View Promotion Casebook",
		},
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"For consideration of promotion",
		"packet_code":"casebook"
	},
}
