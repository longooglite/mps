# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_ofa_review_app = {
	"code": "promo_ofa_review_app",
	"comment":"",
	"descr": '''Review Promotion Application''',
	"header": '''Review Promotion Application''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Review Promotion Application Complete",
	"className": "PacketDownload",
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"New Promotion Recommendation",
		"packet_code":"prelim_promo_app_casebook"
	},
}
