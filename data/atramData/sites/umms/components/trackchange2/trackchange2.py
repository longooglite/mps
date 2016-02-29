# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

trackchange2 = {
	"code": "trackchange2",
	"descr": "Track Change",
	"header": "Appointment",
	"componentType": "Workflow",
	"affordanceType":"",
    "metaTrackCodes":["Faculty","Lecturer","Supplemental"],
    "jobActionType":"TRACKCHANGE",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["track_change2_container","tc2_appt_container","tc2_approval_container"],
	"show_proposed_start_date":False,
}
