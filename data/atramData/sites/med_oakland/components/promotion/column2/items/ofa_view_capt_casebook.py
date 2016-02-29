# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

ofa_view_capt_casebook = {
	"code": "ofa_view_capt_casebook",
	"comment":"",
	"descr": '''View CAPT Promotion Casebook''',
	"header": '''View CAPT Promotion Casebook''',
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
	"successMsg":"View CAPT Promotion Casebook Complete",
	"className": "PacketDownload",
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"New Promotion Recommendation",
		"packet_code":"ofa_view_capt_casebook"
	},
}
