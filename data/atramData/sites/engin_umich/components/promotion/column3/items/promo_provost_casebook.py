# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_provost_casebook = {
	"code": "promo_provost_casebook",
	"comment":"",
	"descr": '''View Provost Casebook''',
	"header": '''View Provost Casebook''',
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
	"successMsg":"View Provost Casebook Complete",
	"className": "PacketDownload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "View Provost Casebook",
		},
		"add_num_pages_toc_specifier":True,
		"add_last_page_toc_entry":True,
		"title":"Promotion Recommendation",
		"packet_code":"casebook"
	},
}
