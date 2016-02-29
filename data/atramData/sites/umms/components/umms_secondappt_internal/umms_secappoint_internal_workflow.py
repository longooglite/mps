# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

umms_secappoint_internal_workflow = {
	"code": "umms_secappoint_internal_workflow",
	"descr": "Secondary Appointment (Internal to UMMS)",
	"header": "Secondary Appointment",
	"devnotes":"In this workflow, the initiating party is the secondary department. "
			   "The secondary department creates an RFP which is approved by the "
			   "candidate's primary department and then, finally, OFA.  ",
	"componentType": "Workflow",
	"affordanceType":"",
    "metaTrackCodes":["Faculty","Lecturer","Supplemental"],
    "jobActionType":"SECONDARYAPPTINSIDE",
	"optional": False,
	"enabled": False,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["sec_int_recruitment_container","sec_int_appointment_container","sec_int_approval_container"]
}
