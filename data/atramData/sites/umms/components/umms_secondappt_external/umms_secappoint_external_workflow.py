# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

umms_secappoint_external_workflow = {
	"code": "umms_secappoint_external_workflow",
	"descr": "Secondary Appointment (External to UMMS)",
	"header": "Secondary Appointment",
	"componentType": "Workflow",
	"affordanceType":"",
    "metaTrackCodes":["Faculty","Lecturer","Supplemental"],
    "jobActionType":"SECONDARYAPPTOUTSIDE",
	"optional": False,
	"enabled": False,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["sec_ext_recruitment_container","sec_ext_appointment_container","sec_ext_approval_container"]
}
