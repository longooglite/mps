# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_personalinfo = {
	"code": "cred_personalinfo",
	"descr": "Personal Information",
	"header": "Personal Information",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["apptCandidate","dept_task"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate",'mss_task'],
	"blockers": [],
	"statusMsg": "",
	"successMsg": "Personal Information was saved",
	"className": "UberForm",
	"config": {
		"isFieldLevelRevisable":True,
		"fieldLevelRevisePermissions":['mss_task',"dept_task"],
		"disclosureGroup":{"code":"APP","descr":"Credentialing Application Items"},
		"printLabelColumnWidth":"400px",
		"questionGroupCode": "personalInfo",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Personal Information saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Personal Information saved as draft",
		},

		"savedSetsEnabled": False,

		"isPersonalInfo": True,
		"personalInfoCodes": ["first_name", "middle_name", "last_name", "suffix", "email"],
		"parentCode": "personalinfo",
	},
}
