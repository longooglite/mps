# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_status_sent_to_dept = {
	"code": "enroll_status_sent_to_dept",
	"comment":"",
	"descr": "Sent to Department",
	"header": "Sent to Department",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","enroll_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Status Saved",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Enrollment Packet Sent to Department Status",
		},
	},
}
