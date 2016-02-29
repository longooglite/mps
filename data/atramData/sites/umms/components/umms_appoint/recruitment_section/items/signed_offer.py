# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

signed_offer = {
	"code": "signed_offer",
	"descr": "Signed Offer Letter",
	"header": "Signed Offer Letter",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"overviewOnly":False,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["acceptoffer"],
	"containers": [],
    "statusMsg": "",
	"className": "FileUpload",
	"config": {
		"dashboardEvents": [{
			"code":"offeraccepted",
			"eventType":"remove",
		}],

		"min": "1",
		"max": "1",
	},

}
