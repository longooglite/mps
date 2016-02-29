# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

appointment_workflow = {
	"code": "appointment_workflow",
	"descr": "Appointment",
	"header": "Appointment",
	"componentType": "Workflow",
	"affordanceType":"",
	"metaTrackCodes":["Standard","Tenured","TenureTrack"],
	"jobActionType":"NEWAPPOINT",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["recruitment_tab","approvals_tab","finalize_tab"],
	"config": {
	},
}
