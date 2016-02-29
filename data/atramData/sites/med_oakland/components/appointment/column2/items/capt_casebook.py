# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

capt_casebook = {
	"code": "capt_casebook",
	"comment":"",
	"descr": '''View Appointment Application Packet''',
	"header": '''View Appointment Application Packet''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"logEnabled": False,
	"freezable": False,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": ["mpp_prev_appt","cred_check"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"View Appointment Application Packet Complete",
	"className": "PacketDownload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "View Appointment Application Packet",
		},
		"add_num_pages_toc_specifier":False,
		"add_last_page_toc_entry":False,
		"title":"New Appointment Recommendation",
		"packet_code":"capt_casebook"
	},
}
