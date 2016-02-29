# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

umms_appoint_workflow = {
	"code": "umms_appoint_workflow",
	"descr": "Appointment",
	"header": "Appointment",
	"componentType": "Workflow",
	"affordanceType":"",
    "metaTrackCodes":["Faculty","Lecturer","Supplemental"],
    "jobActionType":"NEWAPPOINT",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["recruitment_container","appointment_container","appoint_approval_container"],
	"config": {
		"initItemCodes":["personalinfo","ari","cbc","npi"],
		"countdown_clock":{
			"offset_days":60,
			"warning_days":10,
			"completionContainer":"submitOFA"
		}
	},
}
