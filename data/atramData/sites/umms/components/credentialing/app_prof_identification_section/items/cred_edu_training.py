# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_edu_training = {
	"code": "cred_edu_training",
	"descr": "Education & Training",
	"header": "Education & Training",
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
	"successMsg": "Education & Training was saved",
	"className": "UberForm",
	"config": {
		"isFieldLevelRevisable":True,
		"fieldLevelRevisePermissions":['mss_task',"dept_task"],
		"disclosureGroup":{"code":"APP","descr":"Credentialing Application Items"},
		"printLabelColumnWidth":"400px",
		"questionGroupCode": "credEduTraining",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Education & Training saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Education & Training saved as draft",
		},

		"savedSetsEnabled": False,

	},
}
