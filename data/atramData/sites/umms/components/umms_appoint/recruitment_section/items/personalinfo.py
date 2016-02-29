# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

personalinfo = {
	"code": "personalinfo",
	"descr": "Personal Info",
	"header": "Personal Info",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"blockers": ["startappointment"],
	"statusMsg": "",
	"successMsg": "Personal Information was saved",
	"className": "UberForm",
	"config": {
		"questionGroupCode": "personalInfo",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Personal Info saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Personal Info saved as draft",
		},

		"savedSetsEnabled": False,

		"isPersonalInfo": True,
		"personalInfoCodes": ["first_name", "middle_name", "last_name", "suffix", "email"],
		"parentCode": "personalinfo",
	},
}
