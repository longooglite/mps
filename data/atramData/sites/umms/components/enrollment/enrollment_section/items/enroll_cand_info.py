# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_cand_info = {
	"code": "enroll_cand_info",
	"descr": "Candidate Info",
	"header": "Candidate Info",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task",'enroll_task'],
	"viewPermissions": ["dept_task","ofa_task",'enroll_task'],
	"blockers": [],
	"statusMsg": "",
	"successMsg": "Candidate Info was saved",
	"className": "UberForm",
	"config": {
		"isFieldLevelRevisable":False,
		"fieldLevelRevisePermissions":[],
		"questionGroupCode": "enroll_cand_info",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Candidate Info was saved",
		},

		"draftEnabled": False,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Licensure saved as draft",
		},

		"savedSetsEnabled": False,

	},
}
