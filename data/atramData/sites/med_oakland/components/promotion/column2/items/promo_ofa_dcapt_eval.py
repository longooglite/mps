# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_ofa_dcapt_eval = {
	"code": "promo_ofa_dcapt_eval",
	"comment":"",
	"descr": '''View DCAPT Evaluation Form''',
	"header": '''View DCAPT Evaluation Form''',
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
	"successMsg":"View DCAPT Evaluation Form Complete",
	"className": "PacketDownload",
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"DCAPT Evaluation Form",
		"packet_code":"promo_ofa_dcapt_eval"
	},
}
