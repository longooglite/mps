# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

provider_enroll_info = {
	"code": "provider_enroll_info",
	"comment":"",
	"descr": "Provider Enrollment Information",
	"header": "Provider Enrollment Information",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"accessPermissions": ["dept_task","ofa_task",'enroll_task'],
	"viewPermissions": ["dept_task","enroll_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
	"className": "PacketDownload",
	"config": {
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"",
		"omitTOC":True,
		"packet_code":"provider_enroll_info",
	},
}
